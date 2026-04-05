import express from "express";
import cors from "cors";
import { chatRouter } from "./routes/chat";

const app = express();
const PORT = 3001;

app.use(cors({ origin: "http://localhost:5173" }));
app.use(express.json());

app.use("/api/chat", chatRouter);

app.listen(PORT, () => {
  console.log(`Backend running on http://localhost:${PORT}`);
});
