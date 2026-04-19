import { CharacterId, ChatMessage } from "./types";

export async function sendMessage(
  characterId: CharacterId,
  message: string,
  history: ChatMessage[]
): Promise<string> {
  const response = await fetch("/proxy/5173/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      characterId,
      message,
      history,
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Server error: ${response.status} - ${text}`);
  }

  const data = (await response.json()) as { reply: string };
  return data.reply;
}