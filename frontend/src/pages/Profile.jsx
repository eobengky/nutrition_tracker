import { useState, useEffect } from "react";
import axios from "axios";
import api, { MEDIA_URL } from "../api";
import "../styles/Profile.css";
import { useNavigate } from "react-router-dom";
import LoadingIndicator from "../components/LoadingIndicator";

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [formData, setFormData] = useState({});
  const [fileName, setFileName] = useState("No file chosen");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const profileName = profile ? "Edit Profile" : "Create Profile";

  const profilePic =
    (profile?.profile_picture &&
      (profile.profile_picture.startsWith("http")
        ? `${profile.profile_picture}`
        : `${MEDIA_URL}/${profile.profile_picture}`)) ||
    `${MEDIA_URL}/profile_pics/default.jpg`;

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const response = await api.get("/api/user/profile/");

      setProfile(response.data);
      setFormData(response.data);
    } catch (err) {
      setError("Failed to load profile. You may need to create one.");
    } finally {
      setLoading(false);
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const formDataToSend = new FormData();
      Object.keys(formData).forEach((key) => {
        if (key === "profile_picture" && formData[key] instanceof File) {
          formDataToSend.append(key, formData[key]);
        } else {
          formDataToSend.append(key, formData[key] || "");
        }
      });

      let response;
      if (profile) {
        response = await api.put("/api/user/profile/update/", formDataToSend, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        alert("Profile updated successfully!");
      } else {
        response = await api.post("/api/user/profile/create/", formDataToSend, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        alert("Profile created successfully!");
      }
      fetchProfile();
    } catch (error) {
      setError("Profile update failed.");
    } finally {
      setLoading(false);
    }
  };

  // Handle input change
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle file input change
  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      const file = e.target.files[0];
      const allowedTypes = [
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/gif",
      ];

      if (!allowedTypes.includes(file.type)) {
        alert("Invalid file type! Please upload a PNG/JPG/JPEG/GIF file");
        return;
      }
      setFormData({
        ...formData,
        profile_picture: file,
      });
      setFileName(file.name);
    }
  };

  // Handle profile create
  const handleCreateProfile = async () => {
    setLoading(true);
    try {
      await axios.post("/api/user/profile/create/", formData);
      alert("Profile created successfully!");
      fetchProfile();
    } catch (err) {
      setError("Failed to create profile.");
    } finally {
      setLoading(false);
    }
  };

  // Update Profile
  const handleUpdateProfile = async () => {
    setLoading(true);
    try {
      await api.put("/api/user/profile/update/", formData);
      alert("Profile update successfully");
    } catch (err) {
      setError("Update failed.");
    } finally {
      setLoading(false);
    }
  };

  // Delete profile
  const handleDeleteProfile = async () => {
    if (window.confirm("Are you sure you want to delete your profile?")) {
      setLoading(true);
      try {
        await api.delete("/api/user/profile/delete/");
        alert("Profile deleted successfully");
        localStorage.removeItem("ACCESS_TOKEN");
        navigate("/login");
      } catch (err) {
        setError("Delete failed.");
      } finally {
        setLoading(false);
      }
    }
  };

  if (loading) return <LoadingIndicator />;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="profile-container">
      <h2> {profileName} </h2>
      <img src={profilePic} alt="Profile" className="profile-pic" />

      <form onSubmit={handleSubmit}>
        <label>Age: </label>
        <input
          type="number"
          name="age"
          value={formData.age || ""}
          onChange={handleChange}
        />

        <label> Weight (kg): </label>
        <input
          type="number"
          name="weight"
          value={formData.weight || ""}
          onChange={handleChange}
        />

        <label>Height (cm): </label>
        <input
          type="number"
          name="height"
          value={formData.height || ""}
          onChange={handleChange}
        />

        <label> Activity Level: </label>
        <select
          name="activity_level"
          value={formData.activity_level || ""}
          onChange={handleChange}
        >
          <option value="" disabled>
            {" "}
            Select your activity level{" "}
          </option>
          <option value="sedentary"> Sedentary </option>
          <option value="light"> Light Activity </option>
          <option value="moderate"> Moderate Activity </option>
          <option value="active"> Highly Active </option>
        </select>

        <label> Dietary Preferences: </label>
        <textarea
          name="dietary_preferences"
          value={formData.dietary_preferences || ""}
          onChange={handleChange}
          placeholder="E.g. Vegan, Keto, Gluten-Free"
        />

        <label> Allergies: </label>
        <textarea
          name="allergies"
          value={formData.allergies || ""}
          onChange={handleChange}
          placeholder="E.g. Peanuts, Dairy"
        />

        <label>Fitness Goal: </label>
        <select
          name="fitness_goal"
          value={formData.fitness_goal || ""}
          onChange={handleChange}
        >
          <option value="" disabled>
            {" "}
            Select your fitness goal{" "}
          </option>
          <option value="weight_loss"> Weight Loss</option>
          <option value="muscle_gain"> Muscle Gain </option>
          <option value="maintenance"> Maintenance </option>
        </select>

        <label>Profile Picture: </label>

        <label className="custom-file-upload">
          <input type="file" accept="image/*" onChange={handleFileChange} />
          Choose File
        </label>
        <span> {fileName} </span>
        <button type="submit">{profileName}</button>
      </form>

      {profile && (
        <button onClick={handleDeleteProfile} className="delete-btn">
          Delete Profile
        </button>
      )}
    </div>
  );
};

export default Profile;
