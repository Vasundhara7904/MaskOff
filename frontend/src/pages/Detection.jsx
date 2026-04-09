import { useState, useRef, useEffect, useCallback } from "react";

const WS_BASE = "ws://localhost:8000";

const LABELS = {
  masked: { color: "#d97a4f", label: "MASKED" },
  unmasked: { color: "#7f9b73", label: "UNMASKED" },
  improper: { color: "#cc9f47", label: "IMPROPER" },
  veil: { color: "#9c7a5b", label: "VEIL" },
};

// Draw box logic moved within Component to access canvas boundary correctly
export default function Detection() {
  const [streaming, setStreaming] = useState(false);
  const [result, setResult] = useState(null);
  const [frameCount, setFrameCount] = useState(0);
  const [fps, setFps] = useState(0);
  const [latency, setLatency] = useState(0);
  const [error, setError] = useState("");
  const [alertType, setAlertType] = useState(null);

  const videoRef = useRef(null);
  const inferCanvasRef = useRef(null);
  const displayCanvasRef = useRef(null);
  const wsRef = useRef(null);
  const streamRef = useRef(null);
  const rafRef = useRef(null);
  const sendIntervalRef = useRef(null);
  const latestDetsRef = useRef([]);
  const fpsCountRef = useRef(0);
  const fpsTimerRef = useRef(null);
  const lastAudioTimeRef = useRef(0);

  const playAlertSound = useCallback(() => {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.type = "sine";
      osc.frequency.setValueAtTime(900, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(300, ctx.currentTime + 0.3);
      gain.gain.setValueAtTime(0.2, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
      osc.start();
      osc.stop(ctx.currentTime + 0.3);
    } catch (e) {
      console.warn("Audio playback issue:", e);
    }
  }, []);

  const stopRender = useCallback(() => {
    if (rafRef.current) cancelAnimationFrame(rafRef.current);
    rafRef.current = null;
  }, []);

  const stopFeed = useCallback(() => {
    clearInterval(sendIntervalRef.current);
    stopRender();
    wsRef.current?.close();
    streamRef.current?.getTracks().forEach((t) => t.stop());
    latestDetsRef.current = [];
    setStreaming(false);
    setResult(null);
    setFrameCount(0);
    setAlertType(null);
  }, [stopRender]);

  useEffect(() => {
    fpsTimerRef.current = setInterval(() => {
      setFps(fpsCountRef.current);
      fpsCountRef.current = 0;
    }, 1000);
    return () => {
      clearInterval(fpsTimerRef.current);
      stopFeed();
    };
  }, [stopFeed]);

  const startRender = useCallback(() => {
    const video = videoRef.current;
    const canvas = displayCanvasRef.current;
    if (!canvas || !video) return;
    const ctx = canvas.getContext("2d");

    const loop = () => {
      if (canvas.width !== canvas.offsetWidth) canvas.width = canvas.offsetWidth;
      if (canvas.height !== canvas.offsetHeight) canvas.height = canvas.offsetHeight;
      
      const width = canvas.width;
      const height = canvas.height;

      if (video.readyState >= 2 && width > 0 && height > 0) {
        ctx.clearRect(0, 0, width, height);

        const scaleX = width / 320;
        const scaleY = height / 240;

        latestDetsRef.current.forEach((det) => {
          const [x1, y1, x2, y2] = det.bbox;
          const color = LABELS[det.label]?.color || "#28C76F";
          const bx1 = x1 * scaleX;
          const by1 = y1 * scaleY;
          const bx2 = x2 * scaleX;
          const by2 = y2 * scaleY;
          
          ctx.strokeStyle = color;
          ctx.lineWidth = 3;
          ctx.strokeRect(bx1, by1, bx2 - bx1, by2 - by1);
          
          ctx.font = "600 13px Inter, sans-serif";
          const label_text = `${det.label.toUpperCase()} ${(det.confidence * 100).toFixed(0)}%`;
          const textWidth = ctx.measureText(label_text).width;
          
          ctx.fillStyle = color;
          ctx.fillRect(bx1, by1 - 22, textWidth + 12, 22);
          ctx.fillStyle = "#ffffff";
          ctx.fillText(label_text, bx1 + 6, by1 - 6);
        });
      }
      rafRef.current = requestAnimationFrame(loop);
    };
    rafRef.current = requestAnimationFrame(loop);
  }, []);

  const startFeed = useCallback(async () => {
    try {
      setError("");
      const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 1280, height: 720 } });
      streamRef.current = stream;
      const video = videoRef.current;
      if (video) {
        video.srcObject = stream;
        await new Promise((resolve) => {
          video.onloadedmetadata = resolve;
        });
        await video.play();
      }

      setStreaming(true);
      const ws = new WebSocket(`${WS_BASE}/ws/stream`);
      wsRef.current = ws;

      const sendNextFrame = () => {
        if (wsRef.current?.readyState !== WebSocket.OPEN) return;
        const inferCanvas = inferCanvasRef.current;
        const v = videoRef.current;
        const canvas = displayCanvasRef.current;
        
        // If elements aren't ready, try again shortly
        if (!inferCanvas || !v || v.readyState < 2 || !canvas) {
          requestAnimationFrame(sendNextFrame);
          return;
        }

        const width = canvas.offsetWidth;
        const height = canvas.offsetHeight;
        const videoRatio = v.videoWidth / v.videoHeight;
        const canvasRatio = width / height;
        let sWidth = v.videoWidth;
        let sHeight = v.videoHeight;
        let sX = 0;
        let sY = 0;

        if (canvasRatio > videoRatio) {
          sHeight = v.videoWidth / canvasRatio;
          sY = (v.videoHeight - sHeight) / 2;
        } else {
          sWidth = v.videoHeight * canvasRatio;
          sX = (v.videoWidth - sWidth) / 2;
        }

        inferCanvas.getContext("2d").drawImage(v, sX, sY, sWidth, sHeight, 0, 0, inferCanvas.width, inferCanvas.height);
        wsRef.current.send(JSON.stringify({ 
          frame: inferCanvas.toDataURL("image/jpeg", 0.65).split(",")[1],
          conf: 0.25 
        }));
      };

      ws.onopen = () => {
        requestAnimationFrame(startRender);
        // Kick off loop
        requestAnimationFrame(sendNextFrame);
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const dets = data.detections || [];
        latestDetsRef.current = dets;
        setResult(data);
        setLatency(data.latency_ms || 0);
        setFrameCount(data.frame_count || 0);
        fpsCountRef.current += 1;

        let wantsSound = false;
        let wantsVisual = false;

        for (let i = 0; i < dets.length; i++) {
          const l = dets[i].label.toLowerCase();
          // Based strictly on your requested logic:
          if (l === "masked" || l === "improper") {
            wantsSound = true;
            wantsVisual = true;
          } else if (l === "veil") {
            wantsVisual = true;
          }
        }

        if (wantsSound) {
          const now = Date.now();
          if (now - lastAudioTimeRef.current > 1500) {
            playAlertSound();
            lastAudioTimeRef.current = now;
          }
        }

        setAlertType(wantsSound ? 'sound' : (wantsVisual ? 'visual' : null));
        
        // As soon as we receive a response, send the next frame (zero queue delay)
        requestAnimationFrame(sendNextFrame);
      };

      ws.onerror = () => {
        setError("Stream connection error.");
        stopFeed();
      };
    } catch (err) {
      setError("Unable to access camera or connect to backend.");
      console.error(err);
    }
  }, [startRender, stopFeed]);

  const counts = result?.counts || {};
  const detections = result?.detections || [];
  const total = result?.total || 0;

  return (
    <section className="page">
      <section className="live-layout">
        <article className={`panel live-stage ${alertType ? "alert-active" : ""}`} style={{ borderColor: alertType ? "#FF5050" : undefined, boxShadow: alertType ? "0 0 40px rgba(255, 80, 80, 0.4)" : undefined, transition: "all 0.2s ease" }}>
          <div className="live-toolbar">
            <div>
              <p className="eyebrow" style={{ color: alertType ? "#FF5050" : undefined }}>Live detection</p>
              <h2>Camera stream analysis</h2>
            </div>
            <button className={`btn ${streaming ? "btn-soft" : "btn-primary"}`} onClick={streaming ? stopFeed : startFeed}>
              {streaming ? "Stop stream" : "Start stream"}
            </button>
          </div>

          {alertType ? (() => {
            const rules = ['masked', 'improper', 'veil'];
            const activeLabels = [...new Set(detections.filter(d => rules.includes(d.label.toLowerCase())).map(d => d.label.toUpperCase()))];
            
            if (activeLabels.length === 0) return null;
            
            return (
              <div style={{
                background: "#FF5050",
                color: "#ffffff",
                padding: "12px 20px",
                borderRadius: "10px",
                marginBottom: "16px",
                fontWeight: "600",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: "10px",
                letterSpacing: "0.5px",
                boxShadow: "0 4px 12px rgba(255, 80, 80, 0.4)",
              }}>
                <span style={{ fontSize: "18px" }}>⚠️</span>
                <span>SECURITY ALERT: {activeLabels.join(', ')} DETECTED</span>
              </div>
            );
          })() : null}

          <div className="camera-box" style={{ position: "relative" }}>
            <video 
              ref={videoRef} 
              playsInline 
              muted 
              style={{
                display: streaming ? "block" : "none",
                width: "100%",
                height: "100%",
                objectFit: "cover",
              }} 
            />
            <canvas ref={inferCanvasRef} width={320} height={240} className="hidden" />
            {streaming ? (
              <canvas 
                ref={displayCanvasRef} 
                style={{
                  position: "absolute",
                  top: 0,
                  left: 0,
                  width: "100%",
                  height: "100%",
                  pointerEvents: "none",
                }} 
              />
            ) : (
              <div className="camera-placeholder">Start stream to begin detection</div>
            )}
          </div>
          {error ? <p className="error-line">{error}</p> : null}
        </article>

        <aside className="panel live-aside">
          <p className="eyebrow">Telemetry</p>
          <div className="telemetry-grid">
            <div><span>FPS</span><strong>{fps}</strong></div>
            <div><span>Latency</span><strong>{latency}ms</strong></div>
            <div><span>Frames</span><strong>{frameCount}</strong></div>
            <div><span>Total</span><strong>{total}</strong></div>
          </div>
          <div className="counts-grid">
            {Object.keys(LABELS).map((key) => (
              <div className="count-pill" key={key}>
                <span>{LABELS[key].label}</span>
                <strong>{counts[key] || 0}</strong>
              </div>
            ))}
          </div>
          <div className="det-list">
            {detections.length ? detections.map((det, index) => (
              <div className="det-row" key={`${det.label}-${index}`}>
                <span>{det.label.toUpperCase()}</span>
                <strong>{(det.confidence * 100).toFixed(1)}%</strong>
              </div>
            )) : <p className="muted">No active detections</p>}
          </div>
        </aside>
      </section>
    </section>
  );
}
