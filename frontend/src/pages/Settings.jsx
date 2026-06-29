export default function Settings() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">
        Settings
      </h1>

      <div className="bg-slate-900 rounded-2xl p-6">
        <h2 className="text-xl font-semibold mb-4">
          Application Settings
        </h2>

        <div className="space-y-4">

          <div>
            <label className="block mb-2">
              AI Model
            </label>

            <select className="bg-slate-800 p-3 rounded-lg">
              <option>llama3</option>
              <option>mistral</option>
            </select>
          </div>

          <div>
            <label className="block mb-2">
              Default Language
            </label>

            <select className="bg-slate-800 p-3 rounded-lg">
              <option>English</option>
              <option>Hindi</option>
              <option>Bengali</option>
            </select>
          </div>

          <div>
            <label className="block mb-2">
              Voice Speed
            </label>

            <input
              type="range"
              min="0.5"
              max="2"
              step="0.1"
              defaultValue="1"
              className="w-full"
            />
          </div>

          <button className="bg-blue-600 hover:bg-blue-700 px-5 py-3 rounded-lg">
            Save Settings
          </button>

        </div>
      </div>
    </div>
  );
}