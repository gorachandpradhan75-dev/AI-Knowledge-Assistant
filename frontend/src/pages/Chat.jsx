import { useEffect, useState } from "react";
import api from "../services/api";

export default function Chat() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchDocuments = async () => {
    try {
      const response = await api.get("/documents");
      setDocuments(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const askQuestion = async () => {
    if (!selectedDocument) {
      alert("Please select a document");
      return;
    }

    if (!question.trim()) {
      alert("Please enter a question");
      return;
    }

    try {
      setLoading(true);

      const response = await api.post(
        `/documents/${selectedDocument}/ask`,
        {
          question,
          language: "en",
        }
      );

      setAnswer(response.data.answer);
    } catch (error) {
      console.error(error);
      alert("Failed to get answer");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">
        AI Chat
      </h1>

      <div className="bg-slate-900 rounded-2xl p-6">

        <div className="mb-4">
          <label className="block mb-2">
            Select Document
          </label>

          <select
            value={selectedDocument}
            onChange={(e) =>
              setSelectedDocument(e.target.value)
            }
            className="w-full p-3 rounded-lg bg-slate-800"
          >
            <option value="">
              Choose a document
            </option>

            {documents.map((doc) => (
              <option
                key={doc.document_id}
                value={doc.document_id}
              >
                {doc.filename}
              </option>
            ))}
          </select>
        </div>

        <div className="mb-4">
          <textarea
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
            placeholder="Ask a question about the document..."
            className="w-full p-3 rounded-lg bg-slate-800 h-32"
          />
        </div>

        <button
          onClick={askQuestion}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg"
        >
          {loading ? "Thinking..." : "Ask AI"}
        </button>

        {answer && (
          <div className="mt-6 bg-slate-800 p-4 rounded-xl">
            <h3 className="font-semibold mb-2">
              AI Answer
            </h3>

            <p>{answer}</p>
          </div>
        )}

      </div>
    </div>
  );
}