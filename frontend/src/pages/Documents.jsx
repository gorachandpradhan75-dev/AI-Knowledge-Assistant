import { useEffect, useState } from "react";
import api from "../services/api";

export default function Documents() {
const [documents, setDocuments] = useState([]);
const [loading, setLoading] = useState(true);
const [file, setFile] = useState(null);
const [summaries, setSummaries] = useState({});
const [summaryLength, setSummaryLength] = useState("medium");
const [searchTerm, setSearchTerm] = useState("");

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
        "Content-Type":
          "multipart/form-data",
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

const generateSummary = async (
documentId
) => {
try {


  const response = await api.post(
    `/documents/${documentId}/summary`,
    {
      language: "en",
      length: summaryLength,
    }
  );

  setSummaries((prev) => ({
    ...prev,
    [documentId]:
      response.data.summary,
  }));

} catch (error) {

  console.error(error);

  alert(
    "Summary generation failed"
  );
}


};

const deleteDocument = async (
documentId
) => {


const confirmDelete =
  window.confirm(
    "Are you sure you want to delete this document?"
  );

if (!confirmDelete) return;

try {

  await api.delete(
    `/documents/${documentId}`
  );

  setDocuments(
    documents.filter(
      (doc) =>
        doc.document_id !== documentId
    )
  );

  alert(
    "Document deleted successfully"
  );

} catch (error) {

  console.error(error);

  alert(
    "Failed to delete document"
  );
}


};

useEffect(() => {
fetchDocuments();
}, []);

const filteredDocuments =
documents.filter((doc) =>
doc.filename
.toLowerCase()
.includes(
searchTerm.toLowerCase()
)
);

return ( <div>


  <h1 className="text-3xl font-bold mb-6">
    Documents
  </h1>

  <div className="bg-slate-900 rounded-2xl p-6">

    <div className="mb-6 flex gap-4 items-center">

      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setFile(
            e.target.files[0]
          )
        }
      />

      <button
        onClick={uploadDocument}
        className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
      >
        Upload PDF
      </button>

    </div>

    <input
      type="text"
      placeholder="Search documents..."
      value={searchTerm}
      onChange={(e) =>
        setSearchTerm(
          e.target.value
        )
      }
      className="w-full bg-slate-800 p-3 rounded-lg mb-6"
    />

    {loading ? (
      <p>Loading...</p>
    ) : filteredDocuments.length === 0 ? (
      <p>No documents found.</p>
    ) : (
      <div className="space-y-4">

        {filteredDocuments.map(
          (doc) => (
            <div
              key={
                doc.document_id
              }
              className="bg-slate-800 p-5 rounded-xl"
            >

              <h3 className="font-semibold text-lg">
                {doc.filename}
              </h3>

              <p>
                Pages:
                {" "}
                {doc.page_count}
              </p>

              <p>
                Characters:
                {" "}
                {doc.char_count}
              </p>

              <p>
                Chunks:
                {" "}
                {doc.chunk_count}
              </p>

              <p>
                Status:
                {" "}
                {doc.status}
              </p>

              <div className="mt-4 flex gap-3 items-center">

                <select
                  value={
                    summaryLength
                  }
                  onChange={(e) =>
                    setSummaryLength(
                      e.target.value
                    )
                  }
                  className="bg-slate-700 p-2 rounded"
                >
                  <option value="short">
                    Short
                  </option>

                  <option value="medium">
                    Medium
                  </option>

                  <option value="long">
                    Long
                  </option>
                </select>

                <button
                  onClick={() =>
                    generateSummary(
                      doc.document_id
                    )
                  }
                  className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg"
                >
                  Generate Summary
                </button>

                <button
                  onClick={() =>
                    deleteDocument(
                      doc.document_id
                    )
                  }
                  className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg"
                >
                  Delete PDF
                </button>

              </div>

              {summaries[
                doc.document_id
              ] && (
                <div className="mt-4 bg-slate-900 p-4 rounded-lg">

                  <h4 className="font-semibold mb-2">
                    Summary
                  </h4>

                  <p>
                    {
                      summaries[
                        doc.document_id
                      ]
                    }
                  </p>

                </div>
              )}

            </div>
          )
        )}

      </div>
    )}

  </div>

</div>

);
}
