import logo from "../logo.png";

const LABEL_INFO = [
  { key: "masked", name: "Masked", desc: "Mask correctly worn and detected with confidence." },
  { key: "unmasked", name: "Unmasked", desc: "No face covering detected in the bounding box." },
  { key: "improper", name: "Improper", desc: "Mask present but not covering correctly." },
  { key: "veil", name: "Veil", desc: "Full face veil state requiring manual verification." },
];

const TECH = ["YOLOv8", "FastAPI", "React", "WebSocket", "OpenCV", "Ultralytics"];

export default function About() {
  return (
    <section className="page">
      <section className="about-layout">
        <article className="panel about-hero">
          <img src={logo} alt="MaskOff" className="about-logo" />
          <p className="eyebrow">About the platform</p>
          <h1>Built for practical checkpoint workflows</h1>
          <p>
            MaskOff combines live camera detection and still-image analysis to identify mask states quickly,
            with a clean, minimal interface focused on confidence and traceability.
          </p>
        </article>

        <article className="panel">
          <p className="eyebrow">Detection classes</p>
          <h2>Model output states</h2>
          <div className="label-list">
            {LABEL_INFO.map((item) => (
              <div className="label-row" key={item.key}>
                <div className="dot" />
                <div>
                  <h3>{item.name}</h3>
                  <p>{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <p className="eyebrow">Tech stack</p>
          <h2>Core components</h2>
          <div className="chip-wrap">
            {TECH.map((item) => (
              <span className="chip" key={item}>{item}</span>
            ))}
          </div>
        </article>

        <article className="panel">
          <p className="eyebrow">Usage note</p>
          <h2>Human-in-the-loop decisions</h2>
          <p>
            MaskOff is a detection support tool. Final decisions should be made by trained personnel, especially in
            edge conditions (low light, occlusion, unusual camera angles).
          </p>
        </article>
      </section>
    </section>
  );
}
