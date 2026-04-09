import { Link } from "react-router-dom";
import logo from "../logo.png";

const FEATURES = [
  { title: "Real-time stream", desc: "Webcam feed with smooth overlays and low-latency backend inference over WebSocket." },
  { title: "Image understanding", desc: "Upload a still image and receive annotated output, class counts, and confidence traces." },
  { title: "Clear visual language", desc: "Soft sand and teal tones designed for long monitoring sessions without eye fatigue." },
  { title: "Private by default", desc: "Frames and images stay on your machine. Nothing is sent to external providers." },
];

const STATS = [
  { num: "4", lbl: "DETECTION CLASSES" },
  { num: "LIVE", lbl: "WEBCAM PIPELINE" },
  { num: "LOCAL", lbl: "PROCESSING MODE" },
  { num: "FAST", lbl: "YOLO INFERENCE" },
];

export default function Home() {
  return (
    <>
      <video className="page-bg-video" autoPlay muted loop playsInline>
        <source src="/hero.mp4" type="video/mp4" />
      </video>
      <div className="page-bg-overlay" />

      <section className="page main-home">
        <section className="hero-content">
          <img src={logo} alt="MaskOff" className="hero-logo" />
          <p className="eyebrow">Mask detection dashboard</p>
          <h1>MaskOff: Neural-Powered Vision Intelligence</h1>
          <p className="hero-lead">
            Harness the power of YOLOv5 AI for real-time face covering analysis. Detect masked, unmasked, improper, and veil classifications across live streams and static images with zero cloud dependency.
          </p>
          <div className="hero-actions">
            <Link to="/detection" className="btn btn-primary">Start live detection</Link>
            <Link to="/upload" className="btn">Try image upload</Link>
            <Link to="/about" className="btn btn-soft">Explore system</Link>
          </div>
        </section>

      <section className="stats-strip">
        {STATS.map((item) => (
          <article className="stat-card" key={item.lbl}>
            <div className="stat-value">{item.num}</div>
            <div className="stat-label">{item.lbl}</div>
          </article>
        ))}
      </section>

      <section className="content-grid">
        <article className="panel">
          <p className="eyebrow">About MaskOff</p>
          <h2>AI-Powered Face Mask Detection</h2>
          <p>
            MaskOff is an advanced face mask detection platform built on YOLOv5, a state-of-the-art object detection model. 
            It performs real-time analysis on webcam streams and uploaded images to classify face coverings into four detection classes: masked, unmasked, improper, and veil. 
            All processing runs locally on your machine for complete privacy and low-latency performance.
          </p>
        </article>
        <article className="panel">
          <p className="eyebrow">Get started</p>
          <h2>Choose your workflow</h2>
          <div className="quick-actions">
            <Link to="/detection" className="pill-link">Open live mode</Link>
            <Link to="/upload" className="pill-link">Open image mode</Link>
          </div>
        </article>
      </section>

      <section className="feature-grid">
        {FEATURES.map((feature) => (
          <article className="feature-card" key={feature.title}>
            <h3>{feature.title}</h3>
            <p>{feature.desc}</p>
          </article>
        ))}
      </section>
      </section>
    </>
  );
}
