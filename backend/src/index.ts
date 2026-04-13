import "dotenv/config";
import express from "express";
import cors from "cors";
import { chatRouter } from "./routes/chat";

const app = express();

const PORT = process.env.PORT || 3001;
const FRONTEND_URL = process.env.FRONTEND_URL || "http://localhost:5173";

app.use(
  cors({
    origin: FRONTEND_URL,
    credentials: true,
  })
);

app.use(express.json());

app.use("/api/chat", chatRouter);

app.listen(Number(PORT), "0.0.0.0", () => {
  console.log(`Backend running on port ${PORT}`);
});