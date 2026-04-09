from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import numpy as np
import cv2
import base64
import io
import time
import json
from PIL import Image
from ultralytics import YOLO
import asyncio
from typing import Optional
import threading

app = FastAPI(title="FaceGuard Detection API", version="1.0.0")

infer_lock = threading.Lock()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLO model
model = YOLO("best.pt")
print(f"✅ Model loaded successfully!")
print(f"Model classes: {model.model.names if hasattr(model.model, 'names') else 'Unknown'}")

LABELS = ['masked', 'unmasked', 'improper', 'veil']

LABEL_CONFIG = {
    'masked':   {"color": (0, 255, 180),   "alert": False, "hex": "#00FFB4"},
    'unmasked': {"color": (255, 80, 80),    "alert": False, "hex": "#FF5050"},
    'improper': {"color": (255, 200, 0),    "alert": True,  "hex": "#FFC800"},
    'veil':    {"color": (100, 180, 255),  "alert": True,  "hex": "#64B4FF"},
}


def draw_detections(frame: np.ndarray, results) -> np.ndarray:
    """Draw standard bounding boxes on the frame."""
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = LABELS[cls_id] if cls_id < len(LABELS) else "unknown"
            color = LABEL_CONFIG.get(label, {"color": (255, 255, 255)})["color"]

            # Standard solid rectangle
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # Label text above the box
            label_text = f"{label} {conf:.0%}"
            (tw, th), baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
            cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 6, y1), color, -1)
            cv2.putText(frame, label_text, (x1 + 3, y1 - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 1, cv2.LINE_AA)

    return frame


def process_frame(frame: np.ndarray, conf_thresh: float = 0.25):
    """Run YOLO inference and return detections list."""
    with infer_lock:
        results = model(frame, conf=conf_thresh, verbose=False)
    detections = []

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = LABELS[cls_id] if cls_id < len(LABELS) else "unknown"
            x1, y1, x2, y2 = map(float, box.xyxy[0])
            detections.append({
                "label": label,
                "confidence": round(conf, 3),
                "bbox": [x1, y1, x2, y2],
                "alert": LABEL_CONFIG.get(label, {}).get("alert", False),
                "color": LABEL_CONFIG.get(label, {}).get("hex", "#fff"),
            })
    
    # Log class distribution for debugging
    if detections:
        class_counts = {}
        for d in detections:
            class_counts[d["label"]] = class_counts.get(d["label"], 0) + 1
        print(f"  Classes detected: {class_counts}")

    return detections


@app.get("/")
async def root():
    return {"status": "online", "model": "FaceGuard YOLO", "labels": LABELS}


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": time.time(), "model_loaded": model is not None}


@app.get("/test-detection")
async def test_detection():
    """Test if YOLO model is working correctly."""
    try:
        # Create a test frame (640x480 black image)
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Try to run detection
        detections = process_frame(test_frame, conf_thresh=0.5)
        
        return {
            "status": "ok",
            "model_loaded": True,
            "test_detections": len(detections),
            "message": "Model is working correctly"
        }
    except Exception as e:
        return {
            "status": "error",
            "model_loaded": False,
            "error": str(e)
        }


@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    """Detect faces in an uploaded image."""
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is None:
        return JSONResponse(status_code=400, content={"error": "Invalid image"})

    start = time.time()
    detections = process_frame(frame, conf_thresh=0.5)  # Use 0.5 threshold for better accuracy
    latency = round((time.time() - start) * 1000, 1)

    # Encode raw frame (or manually drawn) to base64
    # Re-running inference is inefficient, so let's just draw boxes using `detections` to return an annotated image
    for d in detections:
        x1, y1, x2, y2 = map(int, d["bbox"])
        color_hex = d["color"].lstrip("#")
        if len(color_hex) == 6:
            r = int(color_hex[0:2], 16)
            g = int(color_hex[2:4], 16)
            b = int(color_hex[4:6], 16)
            color_bgr = (b, g, r)
        else:
            color_bgr = (255, 255, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color_bgr, 2)
        cv2.putText(
            frame,
            f'{d["label"]} {int(d["confidence"] * 100)}%',
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color_bgr,
            2,
        )

    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    img_b64 = base64.b64encode(buffer).decode('utf-8')

    counts = {label: 0 for label in LABELS}
    for d in detections:
        counts[d["label"]] = counts.get(d["label"], 0) + 1

    return {
        "detections": detections,
        "counts": counts,
        "total": len(detections),
        "latency_ms": latency,
        "annotated_image": img_b64,
        "alerts": [d for d in detections if d["alert"]],
    }


@app.post("/detect/video")
async def detect_video(file: UploadFile = File(...)):
    """Detect faces in an uploaded video file."""
    import tempfile
    import os
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name
    
    try:
        cap = cv2.VideoCapture(tmp_path)
        if not cap.isOpened():
            return JSONResponse(status_code=400, content={"error": "Invalid video file"})
        
        frame_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        all_detections = []
        sample_frames = []
        start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Process every Nth frame to speed up (N=5 means every 5th frame)
            if frame_count % 5 == 0 or frame_count <= 3:  # Always process first 3 frames
                detections = process_frame(frame, conf_thresh=0.5)  # Use 0.5 threshold
                all_detections.extend(detections)
                
                # Save annotated frame
                annotated = frame.copy()
                for d in detections:
                    x1, y1, x2, y2 = map(int, d["bbox"])
                    color_hex = d["color"].lstrip("#")
                    if len(color_hex) == 6:
                        r = int(color_hex[0:2], 16)
                        g = int(color_hex[2:4], 16)
                        b = int(color_hex[4:6], 16)
                        color_bgr = (b, g, r)
                    else:
                        color_bgr = (255, 255, 255)
                    cv2.rectangle(annotated, (x1, y1), (x2, y2), color_bgr, 2)
                    cv2.putText(
                        annotated,
                        f'{d["label"]} {int(d["confidence"] * 100)}%',
                        (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        color_bgr,
                        2,
                    )
                
                # Store sample frame screenshots
                if len(sample_frames) < 5:
                    _, buffer = cv2.imencode('.jpg', annotated, [cv2.IMWRITE_JPEG_QUALITY, 85])
                    img_b64 = base64.b64encode(buffer).decode('utf-8')
                    sample_frames.append(img_b64)
        
        cap.release()
        
        # Calculate counts and latency
        counts = {label: 0 for label in LABELS}
        for d in all_detections:
            counts[d["label"]] = counts.get(d["label"], 0) + 1
        
        latency = round((time.time() - start_time) * 1000, 1)
        
        return {
            "detections": all_detections[:100],  # Return top 100 detections
            "counts": counts,
            "total": len(all_detections),
            "frames_processed": frame_count,
            "total_frames": total_frames,
            "latency_ms": latency,
            "sample_frames": sample_frames,
            "alerts": [d for d in all_detections if d["alert"]][:10],
        }
    
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    """WebSocket endpoint for real-time video stream detection."""
    try:
        await websocket.accept()
        print("✅ Client connected to WebSocket")
    except Exception as e:
        print(f"❌ Failed to accept WebSocket connection: {e}")
        return
    
    frame_count = 0
    start_time = time.time()
    try:
        while True:
            try:
                data = await websocket.receive_text()
            except Exception as e:
                print(f"❌ Error receiving frame: {e}")
                continue
            
            try:
                payload = json.loads(data)
            except json.JSONDecodeError:
                print("❌ Invalid JSON received")
                continue

            # Decode base64 frame
            try:
                img_data = base64.b64decode(payload["frame"])
            except Exception as e:
                print(f"❌ Error decoding base64: {e}")
                await websocket.send_json({"error": "Invalid frame", "detections": [], "fps": 0, "latency_ms": 0})
                continue
            
            nparr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is None:
                print("❌ Invalid frame received")
                await websocket.send_json({"error": "Invalid frame", "detections": [], "fps": 0, "latency_ms": 0})
                continue

            frame_count += 1
            conf_thresh = float(payload.get("conf", 0.3))
            infer_start = time.time()
            
            # Run YOLO in a thread pool to keep the async event loop unblocked
            loop = asyncio.get_event_loop()
            detections = await loop.run_in_executor(
                None, process_frame, frame, conf_thresh
            )
            latency = round((time.time() - infer_start) * 1000, 1)

            # Calculate FPS
            elapsed = time.time() - start_time
            fps = round(frame_count / elapsed) if elapsed > 0 else 0

            counts = {label: 0 for label in LABELS}
            for d in detections:
                counts[d["label"]] = counts.get(d["label"], 0) + 1

            # Log periodically
            if frame_count % 10 == 0:
                print(f"Frame {frame_count}: {len(detections)} detections, {latency}ms, {fps} FPS")
            
            await websocket.send_json({
                "detections": detections,
                "counts": counts,
                "total": len(detections),
                "latency_ms": latency,
                "fps": fps,
                "frame_count": frame_count,
                "alerts": [d for d in detections if d["alert"]],
            })

    except WebSocketDisconnect:
        print(f"❌ Client disconnected after {frame_count} frames")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
