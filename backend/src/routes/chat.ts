import { Router, Request, Response } from "express";
import { ChatRequest, ChatResponse } from "../types";
import { getWakabaReply } from "../characters/wakaba";
import { getCharacter2Reply } from "../characters/character2";

export const chatRouter = Router();

chatRouter.post("/", (req: Request, res: Response) => {
  const body = req.body as ChatRequest;
  const { characterId, message, history } = body;

  if (!characterId || !message) {
    res.status(400).json({ error: "Missing characterId or message" });
    return;
  }

  // Simulate a small delay to feel more natural
  const delay = 600 + Math.random() * 800;

  setTimeout(() => {
    let reply: string;

    if (characterId === "wakaba") {
      reply = getWakabaReply(history, message);
    } else if (characterId === "character2") {
      reply = getCharacter2Reply(history, message);
    } else {
      res.status(400).json({ error: "Unknown characterId" });
      return;
    }

    const response: ChatResponse = { reply, characterId };
    res.json(response);
  }, delay);
});

chatRouter.get("/characters", (_req: Request, res: Response) => {
  res.json([
    {
      id: "wakaba",
      name: "Wakaba Mutsumi",
      description: "A cheerful, teasing childhood friend with a warm heart.",
    },
    {
      id: "character2",
      name: "Character 2",
      description: "Coming soon...",
    },
  ]);
});
