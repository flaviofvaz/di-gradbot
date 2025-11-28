import { BrowserRouter, Routes, Route } from "react-router-dom";
import ChatPage from "./ChatPage";
import FileUploadPage from "./FileUploadPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/upload" element={<FileUploadPage />} />
      </Routes>
    </BrowserRouter>
  );
}
