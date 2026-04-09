import { Link } from "react-router-dom";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="site-footer">
      <div className="footer-inner">
        <div className="footer-content">
          <p className="footer-text">
            © {currentYear} <strong>MaskOff</strong> — Advanced Face Mask Detection Platform
          </p>
          <p className="footer-text footer-muted">
            Built with precision. Powered by YOLOv8 & modern web technologies.
          </p>
        </div>
        <div className="footer-links">
          <Link to="/privacy" className="footer-link">Privacy Policy</Link>
          <span className="footer-divider">•</span>
          <Link to="/terms" className="footer-link">Terms of Service</Link>
          <span className="footer-divider">•</span>
          <Link to="/contact" className="footer-link">Contact</Link>
        </div>
      </div>
    </footer>
  );
}
