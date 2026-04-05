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

## 📂 Project Structure
```text
Open-RoleGraph/

├── Truth about Wakaba Mutsumi.txt  # Raw lore text (Self-curated from Wiki)
├── kg_optimized.json               # Extracted structured Graph data
├── build_knowledge_bases.py        # Script to build ChromaDB & NetworkX
├── retriever.py                    # Custom Hybrid Retriever engine
├── triples_extraction.py           #To extract structured Graph data
└── README.md
