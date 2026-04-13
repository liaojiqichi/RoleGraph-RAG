import { CharacterId, ChatMessage } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function sendMessage(
  characterId: CharacterId,
  message: string,
  history: ChatMessage[]
): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ characterId, message, history }),
  });

  if (!response.ok) {
    throw new Error(`Server error: ${response.status}`);
  }

  const data = await response.json();
  return data.reply as string;
}