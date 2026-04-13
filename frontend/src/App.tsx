import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import CharacterSelect from "./pages/CharacterSelect";
import ChatPage from "./pages/ChatPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CharacterSelect />} />
        <Route path="/chat/:characterId" element={<ChatPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
