import { ChatMessage } from "../types";

const RAG_API_URL = process.env.RAG_API_URL || "http://localhost:8000";

export async function getWakabaReply(
  _history: ChatMessage[],
  message: string
): Promise<string> {
  const response = await fetch(`${RAG_API_URL}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: message, persona: "Mutsumi" }),
  });

  if (!response.ok) {
    throw new Error(`RAG server error: ${response.status} ${response.statusText}`);
  }

  const data = (await response.json()) as { reply: string };
  return data.reply;
}