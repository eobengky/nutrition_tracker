import { Link } from "react-router-dom";
import "../styles/Header.css";
import Logo from "./Logo";
import react, { useState } from "react";

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="header">
      {/* Logo */}
      <div className="logo">
        <Link to="/" onClick={() => setMenuOpen(false)}>
          <Logo />
        </Link>
      </div>

      {/* Navigation */}
      <nav className={`nav-links ${menuOpen ? "open" : ""}`}>
        <ul>
          <li>
            <Link to="/" onClick={() => setMenuOpen(false)}>
              Home
            </Link>
          </li>
          <li>
            <Link to="/meal-plans" onClick={() => setMenuOpen(false)}>
              Meal Plans
            </Link>
          </li>
          <li>
            <Link to="/track-food" onClick={() => setMenuOpen(false)}>
              Track Food
            </Link>
          </li>
          <li>
            <Link to="/progress" onClick={() => setMenuOpen(false)}>
              Progress
            </Link>
          </li>
          <li>
            <Link to="/notifications" onClick={() => setMenuOpen(false)}>
              Notifications
            </Link>
          </li>
          <li>
            <Link to="/profile" onClick={() => setMenuOpen(false)}>
              Profile
            </Link>
          </li>
        </ul>
      </nav>

      <div
        className={`menu-icon ${menuOpen ? "open" : ""}`}
        onClick={() => setMenuOpen(!menuOpen)}
      >
        <div className="bar"></div>
        <div className="bar"></div>
        <div className="bar"></div>
      </div>
    </header>
  );
};

export default Header;
