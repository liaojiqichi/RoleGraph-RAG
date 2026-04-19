# Quick Start

## Backend
```bash
conda activate be-node
npm install
npm run dev
```

## Frontend
```bash
conda activate fe-node
npm install
npm run build
npm run preview
```

## RAG
```bash
conda activate rag311
python3 -m uvicorn server:app --host 0.0.0.0 --port 8501
```
