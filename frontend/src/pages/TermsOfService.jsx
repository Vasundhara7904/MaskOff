export default function TermsOfService() {
  return (
    <section className="page">
      <article className="policy-layout">
        <h1>Terms of Service</h1>
        <p className="last-updated">Last updated: {new Date().toLocaleDateString()}</p>

        <section className="policy-section">
          <h2>Acceptance</h2>
          <p>
            By using MaskOff, you agree to these terms. Personal, non-commercial use only. No modification, copying, or redistribution allowed.
          </p>
        </section>

        <section className="policy-section">
          <h2>Disclaimer & Liability</h2>
          <p>
            MaskOff is provided "as is" without warranties. We are not liable for any damages or decisions based on detection output. 
            Use at your own risk.
          </p>
        </section>

        <section className="policy-section">
          <h2>Critical: Detection Tool Only</h2>
          <p>
            MaskOff is a support tool. Final decisions must be made by trained personnel. We are not liable for outcomes based solely on our detection results.
          </p>
        </section>

        <section className="policy-section">
          <h2>Questions?</h2>
          <p>
            Contact us at <a href="mailto:support@maskoff.local">support@maskoff.local</a>
          </p>
        </section>
      </article>
    </section>
  );
}
