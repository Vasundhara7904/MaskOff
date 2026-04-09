import { NavLink } from "react-router-dom";
import logo from "../logo.png";

export default function Navbar() {
  return (
    <header className="site-nav">
      <div className="nav-inner">
        <NavLink to="/" className="brand-link">
          <img src={logo} alt="MaskOff" className="brand-logo" />
          <span className="brand-copy">
            <strong>MaskOff</strong>
            <span>Mask Detection Console</span>
          </span>
        </NavLink>
        <nav className="nav-links">
          <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`} end>
            Home
          </NavLink>
          <NavLink to="/detection" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
            Live
          </NavLink>
          <NavLink to="/upload" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
            Image
          </NavLink>
          <NavLink to="/video" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
            Video
          </NavLink>
          <NavLink to="/about" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
            About
          </NavLink>
        </nav>
        <div className="nav-chip">Local AI</div>
      </div>
    </header>
  );
}
