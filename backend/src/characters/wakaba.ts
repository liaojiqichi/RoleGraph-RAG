// Dummy responses for Wakaba Mutsumi — cheerful, teasing childhood-friend energy
// TODO: Replace getReply() with LLM call when implementing AI responses

const wakabaResponses: Record<string, string[]> = {
  greeting: [
    "Ahh, you finally messaged me! I was starting to think you forgot about me~ 💕",
    "Oh? Talking to me again? I'm honoured, really! What's on your mind?",
    "Hey hey~! You know I'm always happy when you reach out. So, what's up? ☆",
  ],
  question: [
    "Hmm, that's a tricky one! Let me think... nope, no idea~ But I believe in you!",
    "Ooh, a question! You know, you could probably figure that out yourself if you thought harder~",
    "Ehh? Why are you asking me? ...Fine fine, I'll help. Just this once, okay? 🌸",
  ],
  compliment: [
    "Ehh?! You're complimenting me?! W-well, I mean... thank you~ (Don't get the wrong idea!)",
    "Wah, you're being so sweet today. Did something happen? You're making me blush, you know~",
    "Hmph! You only say that because you want something. ...Still, it makes me happy. 💕",
  ],
  default: [
    "Hmm, I hear you~ It's like you're saying something important but I need to think about it more!",
    "Ahaha, that's so like you! You always keep things interesting~",
    "You know what, I was just thinking about something like that! What a coincidence~ ✨",
    "Ehh, really? Tell me more! I want to know everything~",
    "Fufu~ So what are you really trying to say? I won't tease you... much. 🌸",
    "Hmm... I think I understand! You're pretty easy to read, you know that?",
    "Waa, that's actually kind of interesting! You surprise me sometimes~ ☆",
  ],
};

function classify(message: string): keyof typeof wakabaResponses {
  const lower = message.toLowerCase();
  if (["hi", "hello", "hey", "yo", "sup", "good morning", "good evening"].some((w) => lower.includes(w))) {
    return "greeting";
  }
  if (lower.includes("?") || ["what", "why", "how", "when", "where", "who", "which"].some((w) => lower.startsWith(w))) {
    return "question";
  }
  if (["cute", "beautiful", "pretty", "amazing", "love you", "awesome", "great", "nice", "wonderful"].some((w) => lower.includes(w))) {
    return "compliment";
  }
  return "default";
}

function pick<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

export function getWakabaReply(_history: unknown[], message: string): string {
  const category = classify(message);
  // TODO: Replace this entire function with an LLM call:
  // return await llm.chat({ character: "wakaba", history, message });
  return pick(wakabaResponses[category]);
}
