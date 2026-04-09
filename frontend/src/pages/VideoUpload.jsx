import { useState, useRef, useCallback } from "react";

const API_BASE = "http://localhost:8000";

export default function VideoUpload() {
  const [previewSrc, setPreviewSrc] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [videoName, setVideoName] = useState("");
  const fileInputRef = useRef(null);

  const handleFile = useCallback(async (file) => {
    if (!file) return;
    setLoading(true);
    setResult(null);
    setError("");
    setVideoName(file.name);
    
    // Create preview URL for video
    const videoUrl = URL.createObjectURL(file);
    setPreviewSrc(videoUrl);
    
    const fd = new FormData();
    fd.append("file", file);
    try {
      const res = await fetch(`${API_BASE}/detect/video`, { method: "POST", body: fd });
      if (!res.ok) {
        throw new Error(`Server returned ${res.status}`);
      }
      const data = await res.json();
      setResult(data);
      if (data.annotated_video) {
        setPreviewSrc(`data:video/mp4;base64,${data.annotated_video}`);
      }
    } catch (e) {
      console.error(e);
      setError("Could not complete video detection. Please check backend status and try again.");
    } finally {
      setLoading(false);
    }
  }, []);

  const counts = result?.counts || {};
  const detections = result?.detections || [];

  return (
    <section className="page">
      <section className="upload-layout">
        <article className="panel">
          <p className="eyebrow">Video mode</p>
          <h1>Upload and detect</h1>
          <p className="muted">Upload a video file and get frame-by-frame classification counts, confidence, and an annotated output.</p>

          <div className="upload-drop" onClick={() => fileInputRef.current?.click()}>
            {previewSrc ? (
              <video src={previewSrc} className="upload-preview" controls muted />
            ) : (
              <p>Select a video file</p>
            )}
            <input ref={fileInputRef} type="file" accept="video/*" className="hidden" onChange={(e) => handleFile(e.target.files[0])} />
          </div>
          <div className="actions-row">
            <button className="btn btn-primary" onClick={() => fileInputRef.current?.click()} disabled={loading}>
              {loading ? "Processing..." : "Choose video"}
            </button>
            <button className="btn btn-soft" onClick={() => { setPreviewSrc(null); setResult(null); setError(""); setVideoName(""); }}>
              Clear
            </button>
          </div>
          {error ? <p className="error-line">{error}</p> : null}
        </article>

        <aside className="panel upload-side">
          <p className="eyebrow">Results</p>
          <div className="telemetry-grid">
            <div><span>Total</span><strong>{result?.total || 0}</strong></div>
            <div><span>Latency</span><strong>{result?.latency_ms || 0}ms</strong></div>
            <div><span>Masked</span><strong>{counts.masked || 0}</strong></div>
            <div><span>Unmasked</span><strong>{counts.unmasked || 0}</strong></div>
          </div>
          <div className="counts-grid">
            <div className="count-pill">
              <span>Improper</span>
              <strong>{counts.improper || 0}</strong>
            </div>
            <div className="count-pill">
              <span>Veil</span>
              <strong>{counts.veil || 0}</strong>
            </div>
          </div>
          {result?.annotated_video ? (
            <a className="btn btn-primary full" href={`data:video/mp4;base64,${result.annotated_video}`} download="maskoff_video_result.mp4">
              Download annotated video
            </a>
          ) : null}
        </aside>
      </section>
    </section>
  );
}
