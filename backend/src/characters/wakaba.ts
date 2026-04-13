import { ChatMessage } from "../types";

export async function getWakabaReply(
  _history: ChatMessage[],
  message: string
): Promise<string> {
  const response = await fetch("http://localhost:8000/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: message, persona: "Mutsumi" }),
  });

  if (!response.ok) throw new Error("RAG server error");
  const data = await response.json() as { reply: string };
  return data.reply;
}