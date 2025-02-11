import { Link } from "react-router-dom";
import "../styles/Header.css";
import Logo from "./Logo";

function Header() {
  return (
    <header className="header">
      <div className="logo">
        <Logo />
      </div>

      <nav>
        <ul className="nav-links">
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/dashboard">Dashboard</Link>
          </li>
          <li>
            <Link to="/meal-planner">Meal Planner</Link>
          </li>
          <li>
            <Link to="/logout">Logout</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
