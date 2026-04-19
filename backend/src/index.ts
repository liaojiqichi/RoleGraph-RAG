import "dotenv/config";
import express from "express";
import cors from "cors";
import { chatRouter } from "./routes/chat";

const app = express();

const PORT = 8500;
const FRONTEND_URL = process.env.FRONTEND_URL || "http://localhost:5173";

console.log("PORT:", PORT);
console.log("FRONTEND_URL:", FRONTEND_URL);

app.use(cors());
app.use(express.json());

app.get("/health", (_req, res) => {
  res.json({
    status: "ok",
    message: "Backend is alive",
  });
});

app.use("/api/chat", chatRouter);

app.listen(Number(PORT), "0.0.0.0", () => {
  console.log(`Backend running on port ${PORT}`);
});