import React, { useState, useEffect, useRef } from "react";
import { useLocation, Link } from "react-router-dom";
import cameraIcon from "../assets/camera.png";
import searchIcon from "../assets/search.png";
import micIcon from "../assets/mic.png";
import "./ChatPage.css";
import "./LandingPage.css";

// Helper to format assessment messages
function formatAssessment(data) {
  return (
    <div>
      <div style={{ fontWeight: 700, fontSize: "1.1em", marginBottom: 8 }}>Possible Condition:</div>
      <div style={{ marginBottom: 12 }}>{data.diagnosis}</div>
      <div style={{ fontWeight: 700 }}>Severity Level:</div>
      <div style={{ marginBottom: 12 }}>{data.severity}/5</div>
      <div style={{ fontWeight: 700 }}>Reasoning:</div>
      <div style={{ marginBottom: 12 }}>{data.rationale}</div>
      <div style={{ fontWeight: 700 }}>Immediate Actions:</div>
      <ul>
        {(data.immediate_actions && data.immediate_actions.length > 0)
          ? data.immediate_actions.map((a, i) => <li key={i}>{a}</li>)
          : <li>None</li>}
      </ul>
      <div style={{ fontWeight: 700, marginTop: 12 }}>Recommended Treatment Steps:</div>
      {Array.isArray(data.treatment_plan) ? (
        <ul>
          {data.treatment_plan.map((step, i) => <li key={i}>{step}</li>)}
        </ul>
      ) : (
        <div style={{ marginBottom: 12, whiteSpace: "pre-line" }}>{data.treatment_plan}</div>
      )}
      {data.emergency_info && (
        <>
          <div style={{ fontWeight: 700 }}>Emergency Info:</div>
          <div style={{ marginBottom: 12 }}>{data.emergency_info}</div>
        </>
      )}
      {data.hospitals && (
        <>
          <div style={{ fontWeight: 700 }}>Nearby Medical Facilities:</div>
          <div style={{ marginBottom: 12 }}>{data.hospitals}</div>
        </>
      )}
      {data.emergency_number && (
        <>
          <div style={{ fontWeight: 700 }}>Local Emergency Services Number:</div>
          <div>{data.emergency_number}</div>
        </>
      )}
    </div>
  );
}

export default function ChatPage() {
  const location = useLocation();
  const initialMessage = location.state?.initialMessage || "";
  let locationEnabled = location.state?.locationEnabled;
  if (locationEnabled === undefined) {
    locationEnabled = JSON.parse(sessionStorage.getItem("rescura_location_enabled") || "false");
  }
  // Accept coordinates passed from LandingPage, if any
  const [userLocation, setUserLocation] = useState(location.state?.coords || null);
  const [messages, setMessages] = useState([
    { sender: "Rescura", text: "Describe the emergency situation to begin.", type: "message" }
  ]);
  const [input, setInput] = useState(""); // Start with empty input
  const [loading, setLoading] = useState(false);
  const initialSent = useRef(false); // Track if initial message was sent

  // Send initial message ONCE, with location, and clear input
  useEffect(() => {
    if (
      initialMessage &&
      messages.length === 1 &&
      !initialSent.current
    ) {
      initialSent.current = true;
      (async () => {
        await sendMessage(initialMessage, true);
        setInput(""); // Clear input after sending initial message
      })();
    }
    // eslint-disable-next-line
  }, [initialMessage, messages.length]);

  // Main sendMessage logic
  const sendMessage = async (msg = input, isInitial = false) => {
    if (!msg.trim()) return;
    setMessages(msgs => [...msgs, { sender: "You", text: msg, type: "message" }]);
    setLoading(true);

    // Use location from state if available, otherwise fetch
    let fetchedLocation = userLocation;
    if (!fetchedLocation && locationEnabled && navigator.geolocation) {
      try {
        fetchedLocation = await new Promise((resolve) => {
          navigator.geolocation.getCurrentPosition(
            pos => resolve({
              lat: pos.coords.latitude,
              lng: pos.coords.longitude
            }),
            () => resolve(null),
            { timeout: 5000 }
          );
        });
      } catch {
        fetchedLocation = null;
      }
      setUserLocation(fetchedLocation);
    }
    console.log("Location being sent to backend:", fetchedLocation);

    try {
      const res = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: msg,
          location: fetchedLocation // always included, even if null
        })
      });
      const data = await res.json();
      if (data.type === "assessment") {
        setMessages(msgs => [...msgs, { sender: "Rescura", type: "assessment", data }]);
      } else {
        let botText = "";
        if (data.type === "follow_up") {
          botText = data.message;
        } else if (data.type === "error") {
          botText = "Error: " + data.message;
        } else if (data.type === "message") {
          botText = data.message;
        }
        setMessages(msgs => [...msgs, { sender: "Rescura", text: botText, type: data.type }]);
      }
    } catch (e) {
      setMessages(msgs => [...msgs, { sender: "Rescura", text: "Error connecting to backend.", type: "error" }]);
    }
    if (!isInitial) setInput("");
    setLoading(false);
  };

  return (
    <div className="chat-container">
      {/* Show location sharing status */}
      <div style={{ textAlign: "center", color: "#888", fontSize: "0.95em", margin: "8px 0" }}>
        Location sharing: <b>{locationEnabled ? "ON" : "OFF"}</b>
      </div>
      {locationEnabled && (
        <div style={{ textAlign: "center", color: "#888", fontSize: "0.95em" }}>
          (Location to send: {userLocation ? `${userLocation.lat}, ${userLocation.lng}` : "none"})
        </div>
      )}
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`bubble-wrapper ${msg.sender === "You" ? "bubble-user-wrap" : "bubble-bot-wrap"}`}>
            <div className="bubble-sender">{msg.sender}</div>
            <div className={`bubble ${msg.sender === "You" ? "bubble-user" : "bubble-bot"}`}>
              {msg.type === "assessment"
                ? formatAssessment(msg.data)
                : msg.text}
            </div>
          </div>
        ))}
        {loading && (
          <div className="bubble-wrapper bubble-bot-wrap">
            <div className="bubble-sender">Rescura</div>
            <div className="bubble bubble-bot"><i>Rescura is typing...</i></div>
          </div>
        )}
      </div>
      <div className="chat-input-bar">
        <img src={cameraIcon} alt="camera" className="chat-icon" />
        <img src={searchIcon} alt="search" className="chat-icon" />
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && sendMessage()}
          placeholder="Type your message..."
          disabled={loading}
          className="chat-input"
        />
        <img src={micIcon} alt="mic" className="chat-icon" />
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