import { useState, useEffect, useRef, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { CharacterId, ChatMessage, CHARACTERS } from "../types";
import { sendMessage } from "../api";
import "./ChatPage.css";

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

const WAKABA_INTRO: ChatMessage = {
  id: "intro",
  role: "assistant",
  content: "Ahh, you actually came to talk to me! I'm so happy~ Don't hold back, okay? You can tell me anything ✿",
  timestamp: Date.now(),
};

export default function ChatPage() {
  const { characterId } = useParams<{ characterId: string }>();
  const navigate = useNavigate();
  const [messages, setMessages] = useState<ChatMessage[]>([WAKABA_INTRO]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const character = CHARACTERS.find((c) => c.id === characterId);

  useEffect(() => {
    if (!character || !character.available) {
      navigate("/");
    }
  }, [character, navigate]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = useCallback(async () => {
    const text = input.trim();
    if (!text || isTyping || !characterId) return;

    const userMessage: ChatMessage = {
      id: generateId(),
      role: "user",
      content: text,
      timestamp: Date.now(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);
    setError(null);

    try {
      const reply = await sendMessage(
        characterId as CharacterId,
        text,
        messages
      );

      const assistantMessage: ChatMessage = {
        id: generateId(),
        role: "assistant",
        content: reply,
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch {
      setError("Couldn't reach the server. Is the backend running?");
    } finally {
      setIsTyping(false);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [input, isTyping, characterId, messages]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    // Auto-resize
    e.target.style.height = "auto";
    e.target.style.height = Math.min(e.target.scrollHeight, 120) + "px";
  };

  if (!character) return null;

  return (
    <div className="chat-page">
      {/* Header */}
      <header className="chat-header">
        <button className="back-btn" onClick={() => navigate("/")} aria-label="Go back">
          ← Back
        </button>

        <div className="header-character">
          <div className="header-avatar">
            <WakabaAvatarSmall />
          </div>
          <div className="header-info">
            <span className="header-name">{character.name}</span>
            <span className="header-status">
              <span className="status-dot" />
              Online
            </span>
          </div>
        </div>

        <div className="header-deco">✿</div>
      </header>

      {/* Messages area */}
      <main className="messages-area">
        <div className="messages-inner">
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} characterName={character.name} />
          ))}

          {isTyping && <TypingIndicator name={character.name} />}

          {error && (
            <div className="error-notice">
              <span>⚠ {error}</span>
              <button onClick={() => setError(null)}>✕</button>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input area */}
      <footer className="chat-footer">
        <div className="input-container">
          <textarea
            ref={inputRef}
            className="chat-input"
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Say something to Wakaba~"
            rows={1}
            disabled={isTyping}
            autoFocus
          />
          <button
            className={`send-btn ${input.trim() && !isTyping ? "ready" : ""}`}
            onClick={handleSend}
            disabled={!input.trim() || isTyping}
            aria-label="Send message"
          >
            <SendIcon />
          </button>
        </div>
        <p className="footer-hint">Enter to send · Shift+Enter for new line</p>
      </footer>
    </div>
  );
}

function MessageBubble({ message, characterName }: { message: ChatMessage; characterName: string }) {
  const isUser = message.role === "user";
  return (
    <div className={`message-row ${isUser ? "user-row" : "assistant-row"}`}>
      {!isUser && (
        <div className="bubble-avatar">
          <WakabaAvatarSmall />
        </div>
      )}
      <div className={`bubble ${isUser ? "user-bubble" : "assistant-bubble"}`}>
        {!isUser && <span className="bubble-sender">{characterName}</span>}
        <p className="bubble-text">{message.content}</p>
        <span className="bubble-time">
          {new Date(message.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </span>
      </div>
    </div>
  );
}

function TypingIndicator({ name }: { name: string }) {
  return (
    <div className="message-row assistant-row">
      <div className="bubble-avatar">
        <WakabaAvatarSmall />
      </div>
      <div className="bubble assistant-bubble typing-bubble">
        <span className="bubble-sender">{name}</span>
        <div className="typing-dots">
          <span /><span /><span />
        </div>
      </div>
    </div>
  );
}

function WakabaAvatarSmall() {
  return (
    <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="40" cy="28" rx="22" ry="20" fill="#c8854a" />
      <ellipse cx="40" cy="20" rx="19" ry="14" fill="#d9935a" />
      <ellipse cx="18" cy="38" rx="7" ry="16" fill="#c8854a" />
      <ellipse cx="62" cy="38" rx="7" ry="16" fill="#c8854a" />
      <ellipse cx="40" cy="38" rx="17" ry="18" fill="#fde8d8" />
      <path d="M24 24 Q30 14 40 16 Q50 14 56 24" fill="#d9935a" />
      <ellipse cx="33" cy="22" rx="4" ry="6" fill="#c8854a" />
      <ellipse cx="47" cy="22" rx="4" ry="6" fill="#c8854a" />
      <ellipse cx="33" cy="37" rx="4" ry="4.5" fill="#3a2010" />
      <ellipse cx="47" cy="37" rx="4" ry="4.5" fill="#3a2010" />
      <circle cx="34.5" cy="35.5" r="1.2" fill="white" />
      <circle cx="48.5" cy="35.5" r="1.2" fill="white" />
      <ellipse cx="27" cy="43" rx="4" ry="2.5" fill="#f8a0b0" opacity="0.6" />
      <ellipse cx="53" cy="43" rx="4" ry="2.5" fill="#f8a0b0" opacity="0.6" />
      <path d="M35 47 Q40 51 45 47" stroke="#c06080" strokeWidth="1.5" fill="none" strokeLinecap="round" />
      <path d="M28 25 L22 18 L32 22 Z" fill="#ff85a8" />
      <path d="M28 25 L20 22 L25 28 Z" fill="#ff85a8" />
      <circle cx="28" cy="25" r="3" fill="#e8507a" />
    </svg>
  );
}

function SendIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <line x1="22" y1="2" x2="11" y2="13" />
      <polygon points="22 2 15 22 11 13 2 9 22 2" />
    </svg>
  );
}
