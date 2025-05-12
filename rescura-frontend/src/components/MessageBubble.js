import "./MessageBubble.css";

export default function MessageBubble({ sender, text }) {
  return (
    <div className={`bubble ${sender === "You" ? "bubble-user" : "bubble-bot"}`}>
      {text}
    </div>
  );
}