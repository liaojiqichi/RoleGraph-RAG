from fastapi import FastAPI
from pydantic import BaseModel
from rag.llm_generator import generate_response 

app = FastAPI()

class ChatRequest(BaseModel):
    query: str
    persona: str = "Mutsumi"

@app.post("/generate")
def generate(req: ChatRequest):
    reply, context = generate_response(req.query, req.persona)
    return {"reply": reply, "context": context}