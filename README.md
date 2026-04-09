<div align="center">

<pre>
███╗   ███╗ █████╗ ███████╗██╗  ██╗ ██████╗ ███████╗███████╗
████╗ ████║██╔══██╗██╔════╝██║ ██╔╝██╔═══██╗██╔════╝██╔════╝
██╔████╔██║███████║███████╗█████╔╝ ██║   ██║█████╗  █████╗  
██║╚██╔╝██║██╔══██║╚════██║██╔═██╗ ██║   ██║██╔══╝  ██╔══╝  
██║ ╚═╝ ██║██║  ██║███████║██║  ██╗╚██████╔╝██║     ██║     
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝    
</pre>

<br/>

<b>Real-Time Face Mask Detection & Security Alert System</b>

<br/><br/>

<a href="https://python.org">
<img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</a>

<a href="https://ultralytics.com">
<img src="https://img.shields.io/badge/YOLOv8-Ultralytics-FF6B35?style=for-the-badge&logo=pytorch&logoColor=white" />
</a>

<a href="https://react.dev">
<img src="https://img.shields.io/badge/React-18.x-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
</a>

<a href="https://fastapi.tiangolo.com">
<img src="https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
</a>

<a href="https://opencv.org">
<img src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
</a>

<a href="LICENSE">
<img src="https://img.shields.io/badge/License-MIT-00D4AA?style=for-the-badge" />
</a>

<br/><br/>

<i>A dark, luxury HUD-style dashboard that detects mask states in real time — so checkpoints stay smart.</i>

<br/>

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Demo & Screenshots](#-demo--screenshots)
- [Features](#-features)
- [Detection Classes](#-detection-classes)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Configuration](#-configuration)
- [Known Limitations](#-known-limitations)
- [Future Roadmap](#-future-roadmap)
- [License](#-license)

---

## 😷 Overview

**MaskOff** is a real-time face mask detection system powered by a custom-trained **YOLOv8** model that classifies **4 mask states** from a live webcam stream or uploaded still images.

Frames are streamed from the React frontend to a FastAPI backend over **WebSocket**, annotated with bounding boxes and confidence labels, and returned for live canvas overlay — all inside a sleek, dark gold HUD dashboard.

```
[ Webcam / Uploaded Image ]
         │
         ▼
   React Frontend  ──► Canvas frame capture (320×240 JPEG)
         │
         ▼
   WebSocket / REST  ──► FastAPI Backend
         │
         ▼
   YOLOv8 Inference  ──► Bounding Box Annotation
         │
         ▼
   Mask Classification
         │
    ┌────┴──────────┐
    │               │
 Masked /        Unmasked /
 Improper        Niqab
    │               │
    ▼               ▼
 ⚡ Audio Alert   👁 Visual Alert Banner
    │
    ▼
 Detection cards · Confidence list · Telemetry strip
```

---

## 🎬 Demo & Screenshots

> **Two-panel HUD layout** — live annotated feed on the left, telemetry and detection cards on the right.

| Panel | Description |
|-------|-------------|
| 📹 **Left** | Annotated webcam feed with bounding boxes · Start / Stop stream control · Alert banner |
| 📊 **Right** | FPS · Latency · Frame count · Per-class counters · Live detection rows |

---

## ✨ Features

### 🔴 Real-Time Webcam Detection
- Streams webcam frames to the backend via **WebSocket** at near-native frame rates
- Each frame is captured from a hidden 320×240 canvas, JPEG-encoded, and sent as base64 JSON
- Colour-coded bounding boxes overlaid on a transparent display canvas
- Zero-queue send loop — next frame dispatches immediately upon server response

### 🖼️ Image Upload Mode
- Upload a still image and receive an annotated JPEG, class counts, and confidence traces
- Annotated result replaces the preview inline
- **Download annotated image** button for saving results

### ⚡ Security Alert System
- Full-width flashing **red alert banner** fires on `masked`, `improper`, or `niqab` detections
- **Audio beep** generated via Web Audio API — descending sine sweep, max one beep per 1.5 seconds
- Alert border glow on the camera panel syncs with the banner state
- Banner lists all active alert labels in real time

### 📊 Live Telemetry Panel
- FPS counter updated every second from a client-side frame accumulator
- Latency, total frame count, and total detection count streamed from backend payload
- Per-class counters (Masked / Unmasked / Improper / Niqab) rebuild on every detection change
- Individual detection rows show label + confidence %, sorted by most recent inference

### 🎛️ Three-Page Navigation
- **Home** — hero landing with stats strip, feature grid, and quick-action links
- **Live** — full webcam detection mode with real-time telemetry
- **Upload** — single-image inference with annotated output and download
- **About** — model classes, tech stack, and usage notes

---

## 🏷️ Detection Classes

The model is trained on **4 classes**:

| Category | Class | Alert Type |
|----------|-------|------------|
| 😷 Properly Masked | `masked` | 🔊 Audio + Visual banner |
| 😶 No Mask | `unmasked` | — (counted only) |
| 🫤 Worn Incorrectly | `improper` | 🔊 Audio + Visual banner |
| 🧕 Full Face Veil | `niqab` | 👁 Visual banner only |

> **Total: 4 classes** — covering the full spectrum of real-world face covering states at checkpoints

---

## 🛠️ Tech Stack

| Layer | Technology | Role |
|-------|-----------|------|
| **AI / ML** | `ultralytics` YOLOv8 | Object detection, custom-trained weights (`best.pt`) |
| **Computer Vision** | `OpenCV (cv2)` | Frame decoding, bounding box annotation, JPEG encoding |
| **Backend** | `FastAPI` + `uvicorn` | REST endpoint (`/detect/image`) + WebSocket stream (`/ws/stream`) |
| **Frontend** | `React 18` + `React Router` | SPA with four pages, canvas overlay, WebSocket client |
| **Build Tool** | `Vite` | Fast dev server and production bundler |
| **Numerical** | `NumPy` | Image array manipulation |
| **Audio** | Web Audio API | In-browser descending beep alert |
| **Fonts** | Google Fonts | Cormorant Garamond · DM Sans |
| **Runtime** | Python 3.8+ | Core backend application |

---

## 📁 Project Structure

```
maskoff/
│
├── backend/
│   ├── main.py                     # FastAPI app — REST + WebSocket inference
│   ├── best.pt                     # YOLOv8 trained model weights
│   └── requirements.txt            # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Router shell with Navbar + page routes
│   │   ├── main.jsx                # React DOM entry point
│   │   ├── index.css               # Full HUD theme — colours, typography, layout
│   │   ├── App.css                 # App-level overrides
│   │   ├── logo.png                # Brand logo asset
│   │   ├── components/
│   │   │   └── Navbar.jsx          # Fixed top nav with active-link highlighting
│   │   └── pages/
│   │       ├── Home.jsx            # Landing page — hero, stats, features
│   │       ├── Detection.jsx       # Live webcam stream + WebSocket detection
│   │       ├── ImageUpload.jsx     # Upload image, run inference, download result
│   │       └── About.jsx           # Model info, tech stack, usage notes
│   ├── index.html                  # Vite HTML entry point
│   ├── package.json                # Node dependencies
│   └── vite.config.js              # Vite configuration
│
└── README.md                       # This file
```

---

## ⚙️ Installation

### Prerequisites

- Python **3.8 or higher**
- Node.js **16 or higher** + npm
- A webcam (for live detection mode)
- *(Optional)* NVIDIA GPU + CUDA for faster YOLOv8 inference

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/maskoff.git
cd maskoff
```

### 2. Set Up the Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**`requirements.txt`** should contain:

```
fastapi>=0.100.0
uvicorn>=0.23.0
ultralytics>=8.0.0
opencv-python>=4.8.0
numpy>=1.24.0
python-multipart>=0.0.6
```

### 3. Add Your Model Weights

Place your trained `best.pt` file inside the `backend/` directory:

```
backend/
└── best.pt   ← your trained YOLOv8 weights go here
```

Update the model path in `main.py` if needed:

```python
# main.py
MODEL_PATH = "best.pt"   # relative to backend/ directory
```

### 4. Set Up the Frontend

```bash
cd ../frontend

# Install Node dependencies
npm install
```

### 5. Run the App

**Terminal 1 — Backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

The app will open at `http://localhost:5173`. The backend API runs at `http://localhost:8000`.

---

## 🚀 Usage

### Live Detection Mode
1. Navigate to **Live** in the top navbar
2. Click **Start stream**
3. Point your webcam at faces with / without masks
4. Watch bounding boxes and confidence scores update in real time
5. Monitor the telemetry panel (FPS, latency, per-class counts) on the right
6. Click **Stop stream** when done

### Image Upload Mode
1. Navigate to **Upload** in the top navbar
2. Click the drop zone or **Choose image** to upload a `.jpg`, `.png`, `.webp`, or `.bmp` file
3. Detection runs automatically — annotated result is shown inline
4. View per-class counts and individual detection rows in the results panel
5. Click **Download annotated image** to save the output
6. Click **Clear** to reset

### Navigation
| Page | Path | Description |
|------|------|-------------|
| **Home** | `/` | Project overview, stats, and quick-launch links |
| **Live** | `/detection` | Real-time webcam detection with WebSocket stream |
| **Upload** | `/upload` | Single-image inference and annotated download |
| **About** | `/about` | Detection classes, tech stack, and usage notes |

---

## 🔍 How It Works

### Live Detection Pipeline

```
Webcam frame
    │
    ▼
Hidden <canvas> (320×240)
    │  — drawImage() crops to canvas aspect ratio
    │  — toDataURL("image/jpeg", 0.65) → base64 string
    │
    ▼
WebSocket send  →  { frame: "<base64>", conf: 0.25 }
    │
    ▼
FastAPI /ws/stream
    │  — base64 decode → NumPy array
    │  — YOLOv8 inference with conf threshold
    │  — draw_boxes() adds fills + labels to frame
    │  — re-encode to base64 JPEG
    │
    ▼
WebSocket response  →  { detections, counts, total, latency_ms, frame_count }
    │
    ▼
React onmessage handler
    │  — latestDetsRef.current = detections
    │  — requestAnimationFrame render loop draws boxes on display canvas
    │  — alert logic checks labels → fires audio / banner
    │  — immediately sends next frame (zero-queue loop)
    ▼
Display canvas overlay
```

### Image Upload Pipeline

```
File input  →  FormData POST /detect/image
    │
    ▼
FastAPI reads file bytes  →  NumPy decode
    │  — YOLOv8 inference
    │  — draw_boxes() annotation
    │  — JPEG encode → base64
    │
    ▼
JSON response  →  { detections, counts, total, latency_ms, annotated_image }
    │
    ▼
React sets previewSrc = "data:image/jpeg;base64,..."
```

### Alert Logic (Key Design)

Alert state is computed **fresh on every WebSocket message** from the raw detection list — never cached between frames. This ensures:

- New detection → banner fires **immediately** on the same message
- Detection clears → banner disappears **immediately** without waiting for a timeout
- Audio beep is rate-limited to one per **1.5 seconds** using `lastAudioTimeRef`

| Detected Label | Audio Beep | Visual Banner |
|---------------|-----------|--------------|
| `masked` | ✅ Yes | ✅ Yes |
| `improper` | ✅ Yes | ✅ Yes |
| `niqab` | ❌ No | ✅ Yes |
| `unmasked` | ❌ No | ❌ No |

---

## 🔧 Configuration

Key constants in `backend/main.py`:

```python
# Path to your trained model
MODEL_PATH = "best.pt"

# All detectable class names (must match model training order)
CLASS_NAMES = ["masked", "unmasked", "improper", "niqab"]

# Bounding box colours per class (BGR)
BOX_COLORS = {
    "masked":   (212, 175, 55),   # gold
    "unmasked": (80,  80,  255),  # red-blue
    "improper": (0,   140, 255),  # amber
    "niqab":    (140, 120, 90),   # warm brown
}
```

Key constants in `frontend/src/pages/Detection.jsx`:

```javascript
const WS_BASE = "ws://localhost:8000";   // WebSocket server URL

const LABELS = {
  masked:   { color: "#d97a4f", label: "MASKED" },
  unmasked: { color: "#7f9b73", label: "UNMASKED" },
  improper: { color: "#cc9f47", label: "IMPROPER" },
  niqab:    { color: "#9c7a5b", label: "NIQAB" },
};
```

Key constants in `frontend/src/pages/ImageUpload.jsx`:

```javascript
const API_BASE = "http://localhost:8000";  // REST API base URL
```

---

## ⚠️ Known Limitations

| Limitation | Details |
|-----------|---------|
| **Synchronous webcam loop** | Frame sending is driven by `requestAnimationFrame` — effective FPS depends on backend inference speed and network latency |
| **Local-only deployment** | `WS_BASE` and `API_BASE` are hardcoded to `localhost` — update for remote or Docker deployment |
| **No authentication** | The WebSocket and REST endpoints have no access control — add middleware before public deployment |
| **No event logging** | Detections are not persisted to disk; all state resets on page refresh |
| **Single camera only** | One webcam stream per browser session; no multi-feed support |
| **Windows model path** | `MODEL_PATH` may need adjusting for macOS / Linux environments |

---

## 🗺️ Future Roadmap

- [ ] **Multi-camera support** — simultaneous feeds from multiple entry points
- [ ] **Detection event log** — timestamped CSV / JSON export of all detections and alert events
- [ ] **User authentication** — role-based access for operators vs. admins
- [ ] **Docker deployment** — containerised full-stack build for production use
- [ ] **Expanded model** — hard hat detection, vest detection, additional PPE classes
- [ ] **Mobile companion app** — use phone camera as a remote stream source
- [ ] **Night mode / low-light preprocessing** — CLAHE enhancement for poor visibility
- [ ] **Dashboard analytics** — daily detection trends, class distribution charts, heatmaps

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ using YOLOv8 + FastAPI + React**

*MaskOff · Mask Detection Console · v1.0*

</div>
