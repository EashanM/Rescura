/* import React, { useState } from "react";

function App() {
  const [messages, setMessages] = useState([
    { sender: "Rescura", text: "Describe the emergency situation to begin." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages(msgs => [...msgs, { sender: "You", text: input }]);
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
      });
      const data = await res.json();
      let botText = "";
      if (data.type === "follow_up") {
        botText = data.message;
      } else if (data.type === "assessment") {
        botText = `Possible Condition: ${data.diagnosis}\nSeverity Level: ${data.severity}/5\nReasoning: ${data.rationale}\nImmediate Actions: ${data.immediate_actions?.join(", ") || "None"}\nRecommended Treatment Steps: ${data.treatment_plan}\n${data.emergency_info}\n${data.hospitals ? "Nearby Medical Facilities: " + data.hospitals : ""}\n${data.emergency_number ? "Local Emergency Services Number: " + data.emergency_number : ""}`;
      } else if (data.type === "error") {
        botText = "Error: " + data.message;
      } else if (data.type === "message") {
        botText = data.message;
      }
      setMessages(msgs => [...msgs, { sender: "Rescura", text: botText }]);
    } catch (e) {
      setMessages(msgs => [...msgs, { sender: "Rescura", text: "Error connecting to backend." }]);
    }
    setInput("");
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Rescura Emergency Triage Chatbot</h2>
      <div style={{ border: "1px solid #ccc", padding: 16, minHeight: 300, marginBottom: 8, background: "#f9f9f9" }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ margin: "8px 0" }}>
            <b>{msg.sender}:</b> <span style={{ whiteSpace: "pre-line" }}>{msg.text}</span>
          </div>
        ))}
        {loading && <div><i>Rescura is typing...</i></div>}
      </div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === "Enter" && sendMessage()}
        style={{ width: "80%", marginRight: 8 }}
        placeholder="Type your message..."
        disabled={loading}
      />
      <button onClick={sendMessage} disabled={loading || !input.trim()}>Send</button>
    </div>
  );
}

export default App; */

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./components/LandingPage";
import ChatPage from "./components/ChatPage";
import ManualsPage from "./components/ManualsPage";
import AlertsPage from "./components/AlertsPage";
import MapPage from "./components/MapPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/manuals" element={<ManualsPage />} />
        <Route path="/alerts" element={<AlertsPage />} />
        <Route path="/map" element={<MapPage />} />
      </Routes>
    </Router>
  );
}

export default App;