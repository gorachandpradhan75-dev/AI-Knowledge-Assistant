import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Dashboard from "./pages/Dashboard";
import Chat from "./pages/Chat";
import Documents from "./pages/Documents";
import Resume from "./pages/Resume";
import Translation from "./pages/Translation";
import VoiceAssistant from "./pages/VoiceAssistant";
import Settings from "./pages/Settings";
import Login from "./pages/Login";
import Register from "./pages/Register";
function AppLayout() {
  return (
    <MainLayout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/documents" element={<Documents />} />
        <Route path="/resume" element={<Resume />} />
        <Route path="/translation" element={<Translation />} />
        <Route path="/voice" element={<VoiceAssistant />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </MainLayout>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
  	<Route path="/register" element={<Register />} />
        <Route path="/*" element={<AppLayout />} />
      </Routes>
    </BrowserRouter>
  );
}