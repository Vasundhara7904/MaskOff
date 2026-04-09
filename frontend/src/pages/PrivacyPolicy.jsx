export default function PrivacyPolicy() {
  return (
    <section className="page">
      <article className="policy-layout">
        <h1>Privacy Policy</h1>
        <p className="last-updated">Last updated: {new Date().toLocaleDateString()}</p>

        <section className="policy-section">
          <h2>Local Processing</h2>
          <p>
            All video frames and images are processed locally on your device. No data is transmitted to external servers.
          </p>
        </section>

        <section className="policy-section">
          <h2>What We Collect</h2>
          <p>
            Video frames, uploaded images, detection results, and basic device information (browser, OS). Data is encrypted using TLS/SSL.
          </p>
        </section>

        <section className="policy-section">
          <h2>Your Rights</h2>
          <p>
            You can access, delete, or request information about your data. Contact us at 
            <a href="mailto:privacy@maskoff.local"> privacy@maskoff.local</a>
          </p>
        </section>

        <section className="policy-section">
          <h2>Technologies</h2>
          <p>
            We use YOLOv8, FastAPI, and React. All processing stays local with complete data control.
          </p>
        </section>
      </article>
    </section>
  );
}
