from fastapi import FastAPI
from pydantic import BaseModel
from llm_generator import generate_response
import traceback

app = FastAPI()

class ChatRequest(BaseModel):
    query: str
    persona: str = "Mutsumi"

@app.post("/generate")
def generate(req: ChatRequest):
    try:
        print(f"[RAG] Received query: {req.query}, persona: {req.persona}")
        reply, context = generate_response(req.query, req.persona)
        print("[RAG] Generation succeeded")
        return {"reply": reply, "context": context}
    except Exception as e:
        print("[RAG] Generation failed:", repr(e))
        traceback.print_exc()
        raise