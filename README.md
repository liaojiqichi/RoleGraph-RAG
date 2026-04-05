# 🎸 RoleGraph-RAG

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![NetworkX](https://img.shields.io/badge/Graph-NetworkX-green)
![ChromaDB](https://img.shields.io/badge/Vector-ChromaDB-orange)
![LLM](https://img.shields.io/badge/LLM-Qwen%20%7C%20Llama3-purple)

**RoleGraph-RAG** is a lightweight, open-source Graph-RAG (Retrieval-Augmented Generation) system built entirely from scratch. It is designed for immersive character role-playing by strictly decoupling Factual Memory (Objective Graph) from Persona (Subjective System Prompt).

## 📂 Project Structure
```text
Open-RoleGraph/

├── Truth about Wakaba Mutsumi.txt  # Raw lore text (Self-curated from Wiki)
├── kg_optimized.json               # Extracted structured Graph data
├── build_knowledge_bases.py        # Script to build ChromaDB & NetworkX
├── retriever.py                    # Custom Hybrid Retriever engine
├── triples_extraction.py           #To extract structured Graph data
└── README.md
