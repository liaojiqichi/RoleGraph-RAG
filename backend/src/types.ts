export type CharacterId = "wakaba" | "character2";

export interface Character {
  id: CharacterId;
  name: string;
  description: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: number;
}

export interface ChatRequest {
  characterId: CharacterId;
  message: string;
  history: ChatMessage[];
}

export interface ChatResponse {
  reply: string;
  characterId: CharacterId;
}
