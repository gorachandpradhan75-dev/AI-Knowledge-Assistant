import { useState } from "react";
import api from "../services/api";

export default function VoiceAssistant() {
  const [transcript, setTranscript] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [aiResponse, setAiResponse] = useState("");
  const [messages, setMessages] = useState([]);
  const askAI = async (message) => {
    try {
      const response = await api.post(
  "/voice/chat",
  {
    message: message,
    history: messages,
  }
);

      const answer =
        response.data.response;

      setAiResponse(answer);
setMessages([
  ...messages,
  {
    role: "user",
    content: message,
  },
  {
    role: "assistant",
    content: answer,
  },
]);
      const speech =
        new SpeechSynthesisUtterance(
          answer
        );

      window.speechSynthesis.speak(
        speech
      );

    } catch (error) {
      console.error(error);

      setAiResponse(
        "AI response failed."
      );
    }
  };

  const startRecording = () => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert(
        "Speech Recognition is not supported in this browser."
      );
      return;
    }

    const recognition =
      new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    setIsListening(true);

    recognition.start();

    recognition.onresult = (event) => {
      const speechText =
        event.results[0][0].transcript;

      setTranscript(speechText);

      askAI(speechText);
    };

    recognition.onerror = (event) => {
      console.error(event.error);

      setIsListening(false);

      alert(
        "Microphone error: " +
          event.error
      );
    };

    recognition.onend = () => {
      setIsListening(false);
    };
  };

  const clearTranscript = () => {
    setTranscript("");
    setAiResponse("");
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-2">
        Voice Assistant
      </h1>

      <p className="text-slate-400 mb-6">
        Speak with AI using your microphone.
      </p>

      <div className="bg-slate-900 rounded-2xl p-6">

        <div className="flex gap-4 mb-6">

          <button
            onClick={startRecording}
            disabled={isListening}
            className="bg-blue-600 hover:bg-blue-700 px-5 py-3 rounded-lg disabled:bg-slate-700"
          >
            {isListening
              ? "🎤 Listening..."
              : "🎤 Start Recording"}
          </button>

          <button
            onClick={clearTranscript}
            className="bg-red-600 hover:bg-red-700 px-5 py-3 rounded-lg"
          >
            Clear
          </button>

        </div>

        <div className="bg-slate-800 p-5 rounded-xl">
          <h3 className="font-bold text-lg mb-3">
            Transcript
          </h3>

          <p className="text-slate-300">
            {transcript ||
              "No speech detected yet."}
          </p>
        </div>

        {aiResponse && (
          <div className="bg-slate-800 p-5 rounded-xl mt-4">
            <h3 className="font-bold text-lg mb-3">
              AI Response
            </h3>

            <p className="text-slate-300">
              {aiResponse}
            </p>
          </div>
        )}

      </div>
    </div>
  );
}