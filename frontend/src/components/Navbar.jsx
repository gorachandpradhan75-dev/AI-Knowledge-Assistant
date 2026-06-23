export default function Navbar() {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900 flex items-center justify-between px-6">
      <h2 className="text-lg font-semibold text-white">
        Dashboard
      </h2>

      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center font-bold">
          G
        </div>
      </div>
    </header>
  );
}