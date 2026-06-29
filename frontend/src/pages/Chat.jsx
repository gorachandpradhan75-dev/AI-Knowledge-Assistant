import { useEffect, useState } from "react";
import api from "../services/api";

export default function Chat() {
const [documents, setDocuments] = useState([]);
const [selectedDocument, setSelectedDocument] = useState("");
const [question, setQuestion] = useState("");
const [loading, setLoading] = useState(false);
const [messages, setMessages] = useState([]);
const [chatMode, setChatMode] = useState("general");

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

const askGeneralAI = async () => {
if (!question.trim()) {
alert("Please enter a question");
return;
}


try {
  setLoading(true);

  const response = await api.post(
    "/voice/chat",
    {
      message: question,
      history: messages,
    }
  );

  setMessages([
    ...messages,
    {
      role: "user",
      content: question,
    },
    {
      role: "assistant",
      content: response.data.response,
    },
  ]);

  setQuestion("");

} catch (error) {
  console.error(error);
  alert("Failed to get AI response");
} finally {
  setLoading(false);
}

};

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

  setMessages([
    ...messages,
    {
      role: "user",
      content: question,
    },
    {
      role: "assistant",
      content: response.data.answer,
    },
  ]);

  setQuestion("");

} catch (error) {
  console.error(error);
  alert("Failed to get answer");
} finally {
  setLoading(false);
}


};

const clearChat = () => {
setMessages([]);
setQuestion("");
};

return ( <div> <h1 className="text-3xl font-bold mb-6">
AI Chat </h1>


  <div className="flex gap-4 mb-6">

    <button
      onClick={() => {
        setChatMode("general");
        setMessages([]);
      }}
      className={`px-5 py-3 rounded-lg ${
        chatMode === "general"
          ? "bg-blue-600"
          : "bg-slate-700"
      }`}
    >
      General AI Chat
    </button>

    <button
      onClick={() => {
        setChatMode("document");
        setMessages([]);
      }}
      className={`px-5 py-3 rounded-lg ${
        chatMode === "document"
          ? "bg-blue-600"
          : "bg-slate-700"
      }`}
    >
      Document Chat
    </button>

    <button
      onClick={clearChat}
      className="bg-red-600 hover:bg-red-700 px-5 py-3 rounded-lg"
    >
      Clear Chat
    </button>

  </div>

  <div className="bg-slate-900 rounded-2xl p-6">

    {chatMode === "document" && (
      <div className="mb-4">

        <label className="block mb-2">
          Select Document
        </label>

        <select
          value={selectedDocument}
          onChange={(e) =>
            setSelectedDocument(
              e.target.value
            )
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
    )}

    <div className="mb-4">

      <textarea
        value={question}
        onChange={(e) =>
          setQuestion(e.target.value)
        }
        placeholder={
          chatMode === "general"
            ? "Ask anything..."
            : "Ask a question about the document..."
        }
        className="w-full p-3 rounded-lg bg-slate-800 h-28"
      />

    </div>

    <button
      onClick={() =>
        chatMode === "general"
          ? askGeneralAI()
          : askQuestion()
      }
      disabled={loading}
      className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg"
    >
      {loading ? "Thinking..." : "Ask AI"}
    </button>

    <div className="mt-8 space-y-4">

      {messages.map((msg, index) => (

        <div
          key={index}
          className={
            msg.role === "user"
              ? "flex justify-end"
              : "flex justify-start"
          }
        >

          <div
            className={`max-w-2xl px-4 py-3 rounded-xl ${
              msg.role === "user"
                ? "bg-blue-600 text-white"
                : "bg-slate-800 text-slate-100"
            }`}
          >
            <p>{msg.content}</p>
          </div>

        </div>

      ))}

    </div>

  </div>
</div>

);
}
