import { Link } from "react-router-dom";
import "../styles/Header.css";
import Logo from "./Logo";
import react, { useState, useEffect } from "react";
import { fetchProfile } from "../pages/Profile";
import { MEDIA_URL } from "../api";

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);
  const [profile, setProfile] = useState(null);

  const profilePic =
    (profile?.profile_picture &&
      (profile.profile_picture.startsWith("http")
        ? `${profile.profile_picture}`
        : `${MEDIA_URL}/${profile.profile_picture}`)) ||
    `${MEDIA_URL}/profile_pics/default.jpg`;

  const handleClickOutside = (event) => {
    if (!event.target.closest(".user-menu")) {
      setProfileMenuOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener("click", handleClickOutside);

    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  useEffect(() => {
    const getProfile = async () => {
      try {
        const data = await fetchProfile();
        setProfile(data);
      } catch (error) {
        console.error("Error fetching profile: ", error);
      }
    };
    getProfile();
  }, []);

  return (
    <header className="header">
      <div className="logo">
        <Link to="/" onClick={() => setMenuOpen(false)}>
          <Logo />
        </Link>
      </div>

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
        </ul>
      </nav>

      <div className="user-menu relative">
        <button
          className="profile-btn"
          onClick={() => setProfileMenuOpen(!profileMenuOpen)}
        >
          {/* Insert Profile picture */}
          <img src={profilePic} alt="Profile" />
        </button>

        {profileMenuOpen && (
          <div className="profile-dropdown">
            <ul>
              <li className="profile-link">
                <Link to="/profile" onClick={() => setMenuOpen(false)}>
                  Profile
                </Link>
              </li>
              <li className="change-password-link">
                <Link to="/change_password" onClick={() => setMenuOpen(false)}>
                  Change password
                </Link>
              </li>
              <li className="logout-link">
                <Link to="/logout" onClick={() => setMenuOpen(false)}>
                  Logout
                </Link>
              </li>
            </ul>
          </div>
        )}
      </div>

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
