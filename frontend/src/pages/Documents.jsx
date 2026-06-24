import { useEffect, useState } from "react";
import api from "../services/api";

export default function Documents() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [file, setFile] = useState(null);

  const fetchDocuments = async () => {
    try {
      const response = await api.get("/documents");
      setDocuments(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const uploadDocument = async () => {
    if (!file) {
      alert("Select a PDF first");
      return;
    }

    try {
      const formData = new FormData();

      formData.append("file", file);

      await api.post(
        "/documents/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      alert("Upload successful");

      setFile(null);

      fetchDocuments();
    } catch (error) {
      console.error(error);
      alert("Upload failed");
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">
        Documents
      </h1>

      <div className="bg-slate-900 rounded-2xl p-6">
        <div className="mb-6 flex gap-4 items-center">
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button
            onClick={uploadDocument}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
          >
            Upload PDF
          </button>
        </div>

        {loading ? (
          <p>Loading...</p>
        ) : documents.length === 0 ? (
          <p>No documents uploaded yet.</p>
        ) : (
          <div className="space-y-4">
            {documents.map((doc) => (
              <div
                key={doc.document_id}
                className="bg-slate-800 p-4 rounded-xl"
              >
                <h3 className="font-semibold text-lg">
                  {doc.filename}
                </h3>

                <p>Pages: {doc.page_count}</p>
                <p>Characters: {doc.char_count}</p>
                <p>Chunks: {doc.chunk_count}</p>
                <p>Status: {doc.status}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}