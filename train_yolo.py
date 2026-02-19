from ultralytics import YOLO

# Load pretrained model
model = YOLO("yolov8n.pt")

# Train
model.train(
    data="data.yaml",
    epochs=30,
    imgsz=224,
    batch=16,
    device="cpu"   # change to 0 if you have GPU
)

print("✅ Training complete!")
