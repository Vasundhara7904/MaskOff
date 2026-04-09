import { useState, useRef, useCallback } from "react";

const API_BASE = "http://localhost:8000";

export default function ImageUpload() {
  const [previewSrc, setPreviewSrc] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const handleFile = useCallback(async (file) => {
    if (!file) return;
    setLoading(true);
    setResult(null);
    setError("");
    const reader = new FileReader();
    reader.onload = (e) => setPreviewSrc(e.target.result);
    reader.readAsDataURL(file);
    const fd = new FormData();
    fd.append("file", file);
    try {
      const res = await fetch(`${API_BASE}/detect/image`, { method: "POST", body: fd });
      if (!res.ok) {
        throw new Error(`Server returned ${res.status}`);
      }
      const data = await res.json();
      setResult(data);
      if (data.annotated_image) setPreviewSrc(`data:image/jpeg;base64,${data.annotated_image}`);
    } catch (e) {
      console.error(e);
      setError("Could not complete image detection. Please check backend status and try again.");
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
          <p className="eyebrow">Image mode</p>
          <h1>Upload and detect</h1>
          <p className="muted">Upload one image and get classification counts, confidence, and an annotated output.</p>

          <div className="upload-drop" onClick={() => fileInputRef.current?.click()}>
            {previewSrc ? <img src={previewSrc} alt="Detection preview" className="upload-preview" /> : <p>Select an image file</p>}
            <input ref={fileInputRef} type="file" accept="image/*" className="hidden" onChange={(e) => handleFile(e.target.files[0])} />
          </div>
          <div className="actions-row">
            <button className="btn btn-primary" onClick={() => fileInputRef.current?.click()} disabled={loading}>
              {loading ? "Detecting..." : "Choose image"}
            </button>
            <button className="btn btn-soft" onClick={() => { setPreviewSrc(null); setResult(null); setError(""); }}>
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
          <div className="det-list">
            {detections.length ? detections.map((det, index) => (
              <div className="det-row" key={`${det.label}-${index}`}>
                <span>{det.label.toUpperCase()}</span>
                <strong>{(det.confidence * 100).toFixed(1)}%</strong>
              </div>
            )) : <p className="muted">No detections yet</p>}
          </div>
          {result?.annotated_image ? (
            <a className="btn btn-primary full" href={`data:image/jpeg;base64,${result.annotated_image}`} download="faceguard_result.jpg">
              Download annotated image
            </a>
          ) : null}
        </aside>
      </section>
    </section>
  );
}
