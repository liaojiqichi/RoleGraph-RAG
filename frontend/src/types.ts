export type CharacterId = "wakaba" | "character2";

export interface Character {
  id: CharacterId;
  name: string;
  description: string;
  available: boolean;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: number;
}

export const CHARACTERS: Character[] = [
  {
    id: "wakaba",
    name: "Wakaba Mutsumi",
    description: "Your cheerful childhood friend. Warm, playful, and just a little teasing~",
    available: true,
  },
  {
    id: "character2",
    name: "Character 2",
    description: "Coming soon...",
    available: false,
  },
];
