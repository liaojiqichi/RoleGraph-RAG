# Character Chat App

A React + TypeScript chat app with an Express backend. Currently uses dummy responses — built to be extended with an LLM later.

## Requirements

- Node.js 18+
- npm

## Getting Started

You need two terminals running at the same time.

**Terminal 1 — Backend**
```bash
cd chat-app/backend
npm install
npm run dev
```
The backend starts on `http://localhost:3001`.

**Terminal 2 — Frontend**
```bash
cd chat-app/frontend
npm install
npm run dev
```
Then open `http://localhost:5173` in your browser.

## Project Structure

```
chat-app/
├── backend/
│   └── src/
│       ├── index.ts              # Express server entry point
│       ├── types.ts              # Shared types
│       ├── routes/chat.ts        # POST /api/chat endpoint
│       └── characters/
│           ├── wakaba.ts         # Wakaba's dummy responses (swap for LLM here)
│           └── character2.ts     # Placeholder for Character 2
├── frontend/
│   └── src/
│       ├── App.tsx               # Routes: / and /chat/:characterId
│       ├── api.ts                # sendMessage() — calls the backend
│       ├── types.ts              # Character definitions
│       └── pages/
│           ├── CharacterSelect   # Page 1: pick a character
│           └── ChatPage          # Page 2: the chat UI
└── rag/                          # RAG pipeline (to be implemented)
```

## API

`POST /api/chat`
```json
{
  "characterId": "wakaba",
  "message": "Hello!",
  "history": []
}
```
Returns:
```json
{
  "reply": "Ahh, you finally messaged me!",
  "characterId": "wakaba"
}
```

## Adding the LLM

Open `backend/src/characters/wakaba.ts` and replace the body of `getWakabaReply()` with your LLM call. The full message history is already passed in as a parameter.

```ts
export async function getWakabaReply(history: ChatMessage[], message: string): Promise<string> {
  // Replace this with your LLM call, e.g.:
  // return await openai.chat({ system: WAKABA_SYSTEM_PROMPT, history, message });
}
```

## Adding Character 2

1. Add the persona logic in `backend/src/characters/character2.ts`
2. Set `available: true` for Character 2 in `frontend/src/types.ts`
3. Update the placeholder description and name to match the character
