import { CharacterId, ChatMessage } from "./types";

export async function sendMessage(
  characterId: CharacterId,
  message: string,
  history: ChatMessage[]
): Promise<string> {
  const response = await fetch("/api/chat", {
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
