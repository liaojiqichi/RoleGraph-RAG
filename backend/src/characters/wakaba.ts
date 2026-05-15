import { ChatMessage } from "../types";

const RAG_API_URL =
  process.env.RAG_API_URL ||
  "http://nv-service-96c47261b3c5dcb26f6b012abc401924:8501";

export async function getWakabaReply(
  _history: ChatMessage[],
  message: string
): Promise<string> {
  const url = `${RAG_API_URL}/generate`;

  console.log("Calling RAG URL:", url);

  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: message,
      persona: "Mutsumi",
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(
      `RAG server error: ${response.status} ${response.statusText} - ${text}`
    );
  }

  const data = (await response.json()) as { reply: string };
  return data.reply;
}