import {
  LayoutDashboard,
  MessageSquare,
  FileText,
  FileSearch,
  Languages,
  Mic,
  Settings,
} from "lucide-react";

import { NavLink } from "react-router-dom";

const menuItems = [
  {
    icon: LayoutDashboard,
    label: "Dashboard",
    path: "/",
  },
  {
    icon: MessageSquare,
    label: "Chat",
    path: "/chat",
  },
  {
    icon: FileText,
    label: "Documents",
    path: "/documents",
  },
  {
    icon: FileSearch,
    label: "Resume Analyzer",
    path: "/resume",
  },
  {
    icon: Languages,
    label: "Translation",
    path: "/translation",
  },
  {
    icon: Mic,
    label: "Voice Assistant",
    path: "/voice",
  },
  {
    icon: Settings,
    label: "Settings",
    path: "/settings",
  },
];

export default function Sidebar() {
  return (
    <aside className="w-72 bg-slate-900 border-r border-slate-800 flex flex-col">
      
      {/* Logo Area */}
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-2xl font-bold text-white">
          AI Knowledge Assistant
        </h1>

        <p className="text-slate-400 text-sm mt-1">
          Enterprise AI Platform
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.label}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl transition ${
                  isActive
                    ? "bg-blue-600 text-white"
                    : "text-slate-300 hover:bg-slate-800 hover:text-white"
                }`
              }
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* User Card */}
      <div className="p-4 border-t border-slate-800">
        <div className="bg-slate-800 rounded-xl p-4">
          <h3 className="font-semibold text-white">
            Gorachand
          </h3>

          <p className="text-sm text-slate-400">
            MCA Student
          </p>
        </div>
      </div>

    </aside>
  );
}