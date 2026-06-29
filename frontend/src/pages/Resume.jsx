import { useState } from "react";
import api from "../services/api";

export default function Resume() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeResume = async () => {
    if (!file) {
      alert("Select a resume PDF first");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post(
        "/resume/analyze",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Resume analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">
        Resume Analyzer
      </h1>

      <div className="bg-slate-900 rounded-2xl p-6">

        <div className="flex gap-4 items-center mb-6">
          <input
            type="file"
            accept=".pdf"
            onChange={(e) =>
              setFile(e.target.files[0])
            }
          />

          <button
            onClick={analyzeResume}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
          >
            Analyze Resume
          </button>
        </div>

        {loading && (
          <p>Analyzing Resume...</p>
        )}

        {result && (
          <div className="bg-slate-800 p-6 rounded-xl">

            <h2 className="text-xl font-bold mb-4">
              {result.filename}
            </h2>

            <p className="mb-3">
              Resume Score: {result.score}/100
            </p>

            <div className="mb-4">
              <h3 className="font-semibold">
                Skills
              </h3>

              <ul>
                {result.skills.map((skill) => (
                  <li key={skill}>
                    • {skill}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="font-semibold">
                Suggestions
              </h3>

              <ul>
                {result.suggestions.map((item) => (
                  <li key={item}>
                    • {item}
                  </li>
                ))}
              </ul>
            </div>

          </div>
        )}

      </div>
    </div>
  );
}