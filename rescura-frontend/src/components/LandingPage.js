import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import logo from "../assets/logo.png";
import cameraIcon from "../assets/camera.png";
import micIcon from "../assets/mic.png";
import background from "../assets/background.png";
import LocationToggle from "./LocationToggle";
import "./LandingPage.css";

export default function LandingPage() {
  const [input, setInput] = useState("");
  const [locationEnabled, setLocationEnabled] = useState(false);
  const navigate = useNavigate();

  const handleStart = async () => {
    sessionStorage.setItem("rescura_location_enabled", JSON.stringify(locationEnabled));
    let coords = null;
    if (locationEnabled && navigator.geolocation) {
      coords = await new Promise((resolve) => {
        navigator.geolocation.getCurrentPosition(
          pos => resolve({
            lat: pos.coords.latitude,
            lng: pos.coords.longitude
          }),
          () => resolve(null),
          { timeout: 5000 }
        );
      });
    }
    navigate("/chat", { state: { initialMessage: input, locationEnabled, coords } });
  };

  return (
    <div
      className="landing-root"
      style={{
        background: `url(${background}) no-repeat center center fixed`,
        backgroundSize: "cover",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center"
      }}
    >
      <div className="landing-center">
        <img src={logo} alt="Rescura Logo" className="landing-logo" />
        <div className="landing-tagline">
          SEIZE THE <span className="landing-tagline-orange">SECOND</span>, SAVE A <span className="landing-tagline-orange">LIFE</span>
        </div>
        <div className="landing-search-bar">
          <img src={cameraIcon} alt="camera" className="landing-icon" />
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="How may I assist you?"
            className="landing-search-input"
            onKeyDown={e => e.key === "Enter" && handleStart()}
          />
          <img src={micIcon} alt="mic" className="landing-icon" />
        </div>
        <LocationToggle enabled={locationEnabled} setEnabled={setLocationEnabled} />
        <button
          onClick={handleStart}
          className="landing-start-btn"
        >
          Start
        </button>
      </div>
      <nav className="landing-nav">
        <Link to="/chat" className="landing-nav-btn active">Chat</Link>
        <Link to="/manuals" className="landing-nav-btn">Manual</Link>
        <Link to="/map" className="landing-nav-btn">Map</Link>
        <Link to="/alerts" className="landing-nav-btn">Alerts</Link>
      </nav>
    </div>
  );
}