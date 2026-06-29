import { useState } from "react";
import api from "../services/api";

export default function Translation() {
  const [text, setText] = useState("");
  const [language, setLanguage] = useState("Hindi");
  const [translatedText, setTranslatedText] = useState("");
  const [loading, setLoading] = useState(false);

  const translate = async () => {
    if (!text.trim()) {
      alert("Enter text first");
      return;
    }

    try {
      setLoading(true);

      const response = await api.post(
        "/translation/translate",
        {
          text: text,
          target_language: language,
        }
      );

      setTranslatedText(
        response.data.translated_text
      );
    } catch (error) {
      console.error(error);
      alert("Translation failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-2">
  AI Translation Assistant
</h1>

<p className="text-slate-400 mb-6">
  Translate text into multiple languages using AI.
</p>
	
      <div className="bg-slate-900 rounded-2xl p-6">

        <textarea
          rows="6"
          placeholder="Enter text..."
          value={text}
          onChange={(e) =>
            setText(e.target.value)
          }
          className="w-full bg-slate-800 p-4 rounded-lg mb-4"
        />
	<p className="text-slate-400 mb-4">
  	Characters: {text.length}
	</p>
        <div className="flex gap-4 mb-4">

          <select
            value={language}
            onChange={(e) =>
              setLanguage(e.target.value)
            }
            className="bg-slate-800 p-3 rounded-lg"
          >
        <option value="Hindi">🇮🇳 Hindi</option>
	<option value="Bengali">🇮🇳 Bengali</option>
	<option value="Tamil">🇮🇳 Tamil</option>
	<option value="Telugu">🇮🇳 Telugu</option>
	<option value="Marathi">🇮🇳 Marathi</option>
	<option value="English">🇺🇸 English</option>
          </select>

          <button
            onClick={translate}
            className="bg-blue-600 hover:bg-blue-700 px-5 py-3 rounded-lg"
          >
            Translate
          </button>
	<button
  onClick={() => {
    setText("");
    setTranslatedText("");
  }}
  className="bg-red-600 hover:bg-red-700 px-5 py-3 rounded-lg"
>
  Clear
</button>


        </div>

        {loading && (
          <p>Translating...</p>
        )}

        {translatedText && (
          <div className="bg-slate-800 p-4 rounded-lg mt-4">
            <h3 className="font-bold mb-2">
              Translated Text
            </h3>

            <p>{translatedText}</p>

<button
  onClick={() =>
    navigator.clipboard.writeText(
      translatedText
    )
  }
  className="mt-3 bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg"
>
  Copy Translation
</button>
          </div>
        )}

      </div>
    </div>
  );
}