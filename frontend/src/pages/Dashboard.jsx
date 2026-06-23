export default function Dashboard() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">
        Dashboard Overview
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        <div className="bg-slate-900 rounded-2xl p-6">
          <p className="text-slate-400">Documents</p>
          <h2 className="text-4xl font-bold mt-2">24</h2>
        </div>

        <div className="bg-slate-900 rounded-2xl p-6">
          <p className="text-slate-400">Chats</p>
          <h2 className="text-4xl font-bold mt-2">152</h2>
        </div>

        <div className="bg-slate-900 rounded-2xl p-6">
          <p className="text-slate-400">Resumes</p>
          <h2 className="text-4xl font-bold mt-2">8</h2>
        </div>

        <div className="bg-slate-900 rounded-2xl p-6">
          <p className="text-slate-400">Languages</p>
          <h2 className="text-4xl font-bold mt-2">15</h2>
        </div>
      </div>

      <div className="mt-8 bg-slate-900 rounded-2xl p-6">
        <h3 className="text-xl font-semibold mb-4">
          Recent Activity
        </h3>

        <ul className="space-y-3 text-slate-300">
          <li>📄 Resume uploaded</li>
          <li>💬 New AI chat created</li>
          <li>🌐 Translation completed</li>
          <li>📚 PDF indexed into FAISS</li>
        </ul>
      </div>
    </div>
  );
}