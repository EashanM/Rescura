import React from "react";

export default function LocationToggle({ enabled, setEnabled }) {
  return (
    <div style={{ marginBottom: 16 }}>
      <button
        onClick={() => setEnabled(!enabled)}
        style={{
          background: enabled ? "#007AFF" : "#ccc",
          color: "#fff",
          border: "none",
          borderRadius: 20,
          padding: "8px 20px",
          cursor: "pointer"
        }}
      >
        {enabled ? "Location Sharing: ON" : "Location Sharing: OFF"}
      </button>
    </div>
  );
}