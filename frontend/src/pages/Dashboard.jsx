import {
  FileText,
  MessageSquare,
  FileSearch,
  Languages,
  Mic,
} from "lucide-react";
import { useEffect, useState } from "react";
import api from "../services/api";
export default function Dashboard() {
const [dashboardStats, setDashboardStats] =
  useState({
    documents: 0,
    chats: 0,
    resumes: 0,
    translations: 0,
  });
const fetchStats = async () => {
  try {

    const response =
      await api.get(
        "/dashboard/stats"
      );

    setDashboardStats(
      response.data
    );

  } catch (error) {

    console.error(error);

  }
};

useEffect(() => {
  fetchStats();
}, []);
  
const stats = [
  {
    title: "Documents",
    value: dashboardStats.documents,
    icon: <FileText size={28} />,
  },
  {
    title: "Chats",
    value: dashboardStats.chats,
    icon: <MessageSquare size={28} />,
  },
  {
    title: "Resume Analyses",
    value: dashboardStats.resumes,
    icon: <FileSearch size={28} />,
  },
  {
    title: "Translations",
    value: dashboardStats.translations,
    icon: <Languages size={28} />,
  },
];
  return (
    <div>
      <h1 className="text-4xl font-bold mb-2">
        Dashboard
      </h1>

      <p className="text-slate-400 mb-8">
        Welcome to your AI Knowledge Assistant.
      </p>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

        {stats.map((item) => (
          <div
            key={item.title}
            className="bg-slate-900 rounded-2xl p-6 border border-slate-800 hover:border-blue-500 transition"
          >
            <div className="flex justify-between items-center">
              <div>
                <p className="text-slate-400">
                  {item.title}
                </p>

                <h2 className="text-4xl font-bold mt-2">
                  {item.value}
                </h2>
              </div>

              <div className="text-blue-500">
                {item.icon}
              </div>
            </div>
          </div>
        ))}

      </div>

      {/* Quick Stats */}
      <div className="grid md:grid-cols-2 gap-6 mt-8">

        <div className="bg-slate-900 rounded-2xl p-6">
          <h3 className="text-xl font-semibold mb-4">
            AI Usage Summary
          </h3>

          <div className="space-y-3 text-slate-300">
            <p>📄 Documents Processed: 24</p>
            <p>💬 AI Conversations: 152</p>
            <p>📑 Resume Analyses: 8</p>
            <p>🌐 Translations: 15</p>
            <p>🎤 Voice Queries: 37</p>
          </div>
        </div>

        <div className="bg-slate-900 rounded-2xl p-6">
          <h3 className="text-xl font-semibold mb-4">
            System Status
          </h3>

          <div className="space-y-3">
            <p className="text-green-400">
              ● Ollama Connected
            </p>

            <p className="text-green-400">
              ● MongoDB Connected
            </p>

            <p className="text-green-400">
              ● FAISS Active
            </p>

            <p className="text-green-400">
              ● API Running
            </p>
          </div>
        </div>

      </div>

      {/* Recent Activity */}
      <div className="mt-8 bg-slate-900 rounded-2xl p-6">
        <h3 className="text-xl font-semibold mb-4">
          Recent Activity
        </h3>

        <ul className="space-y-3 text-slate-300">
          <li>📄 Resume uploaded and analyzed</li>
          <li>💬 New AI chat session started</li>
          <li>🌐 Translation completed</li>
          <li>📚 PDF indexed into FAISS</li>
          <li>🎤 Voice Assistant conversation completed</li>
        </ul>
      </div>
    </div>
  );
}