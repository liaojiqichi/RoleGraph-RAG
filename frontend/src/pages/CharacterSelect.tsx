import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Character, CharacterId, CHARACTERS } from "../types";
import "./CharacterSelect.css";

const SAKURA_PETALS = Array.from({ length: 12 }, (_, i) => i);

export default function CharacterSelect() {
  const [selected, setSelected] = useState<CharacterId | null>(null);
  const navigate = useNavigate();

  const handleStart = () => {
    if (selected) {
      navigate(`/chat/${selected}`);
    }
  };

  return (
    <div className="select-page">
      {/* Floating petals */}
      <div className="petals-container" aria-hidden="true">
        {SAKURA_PETALS.map((i) => (
          <div key={i} className={`petal petal-${i}`} />
        ))}
      </div>

      <div className="select-content">
        <div className="select-header">
          <div className="header-deco">✿</div>
          <h1 className="select-title">Who would you like<br />to talk with?</h1>
          <p className="select-subtitle">Choose a character and begin your conversation</p>
        </div>

        <div className="character-grid">
          {CHARACTERS.map((char: Character) => (
            <button
              key={char.id}
              className={`character-card ${selected === char.id ? "selected" : ""} ${!char.available ? "unavailable" : ""}`}
              onClick={() => char.available && setSelected(char.id)}
              disabled={!char.available}
              aria-pressed={selected === char.id}
            >
              <div className="card-inner">
                <div className="avatar-ring">
                  <div className="avatar">
                    {char.id === "wakaba" ? (
                      <WakabaAvatar />
                    ) : (
                      <PlaceholderAvatar />
                    )}
                  </div>
                </div>

                <div className="card-info">
                  <h2 className="char-name">{char.name}</h2>
                  <p className="char-desc">{char.description}</p>
                </div>

                {!char.available && (
                  <div className="coming-soon-badge">Coming Soon</div>
                )}

                {selected === char.id && (
                  <div className="selected-indicator">✓</div>
                )}
              </div>
            </button>
          ))}
        </div>

        <div className="start-area">
          <button
            className={`start-btn ${selected ? "active" : ""}`}
            onClick={handleStart}
            disabled={!selected}
          >
            <span className="btn-deco">✿</span>
            Start Chat
            <span className="btn-arrow">→</span>
          </button>
          {!selected && (
            <p className="hint-text">Select a character above to continue</p>
          )}
        </div>
      </div>
    </div>
  );
}

function WakabaAvatar() {
  return (
    <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg" className="avatar-svg">
      {/* Hair */}
      <ellipse cx="40" cy="28" rx="22" ry="20" fill="#c8854a" />
      <ellipse cx="40" cy="20" rx="19" ry="14" fill="#d9935a" />
      {/* Side hair */}
      <ellipse cx="18" cy="38" rx="7" ry="16" fill="#c8854a" />
      <ellipse cx="62" cy="38" rx="7" ry="16" fill="#c8854a" />
      {/* Face */}
      <ellipse cx="40" cy="38" rx="17" ry="18" fill="#fde8d8" />
      {/* Hair bang */}
      <path d="M24 24 Q30 14 40 16 Q50 14 56 24" fill="#d9935a" />
      <ellipse cx="33" cy="22" rx="4" ry="6" fill="#c8854a" />
      <ellipse cx="47" cy="22" rx="4" ry="6" fill="#c8854a" />
      {/* Eyes */}
      <ellipse cx="33" cy="37" rx="4" ry="4.5" fill="#3a2010" />
      <ellipse cx="47" cy="37" rx="4" ry="4.5" fill="#3a2010" />
      <circle cx="34.5" cy="35.5" r="1.2" fill="white" />
      <circle cx="48.5" cy="35.5" r="1.2" fill="white" />
      {/* Blush */}
      <ellipse cx="27" cy="43" rx="4" ry="2.5" fill="#f8a0b0" opacity="0.6" />
      <ellipse cx="53" cy="43" rx="4" ry="2.5" fill="#f8a0b0" opacity="0.6" />
      {/* Mouth */}
      <path d="M35 47 Q40 51 45 47" stroke="#c06080" strokeWidth="1.5" fill="none" strokeLinecap="round" />
      {/* Ribbon/bow */}
      <path d="M28 25 L22 18 L32 22 Z" fill="#ff85a8" />
      <path d="M28 25 L20 22 L25 28 Z" fill="#ff85a8" />
      <circle cx="28" cy="25" r="3" fill="#e8507a" />
    </svg>
  );
}

function PlaceholderAvatar() {
  return (
    <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg" className="avatar-svg">
      <circle cx="40" cy="40" r="30" fill="#e0d0e8" />
      <text x="40" y="46" textAnchor="middle" fontSize="24" fill="#a080b0">?</text>
    </svg>
  );
}
