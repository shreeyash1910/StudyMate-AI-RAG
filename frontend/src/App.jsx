import React, { useState } from "react";
import "./styles.css";

  const API_URL =
    import.meta.env.VITE_API_URL ||
    "https://studymate-ai-rag-backend.onrender.com";
function App() {
  // ==========================================
  // STATE
  // ==========================================

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  const [documentId, setDocumentId] = useState(null);
  const [documentName, setDocumentName] = useState("");
  const [documentPages, setDocumentPages] = useState(null);

  const [error, setError] = useState("");

  // ==========================================
  // UPLOAD PDF
  // ==========================================

  const handleUpload = async (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    if (file.type !== "application/pdf") {
      alert("Please select a PDF file.");
      return;
    }

    setUploading(true);
    setError("");

    try {
      const formData = new FormData();

      formData.append("file", file);

      console.log("Uploading:", file.name);

      const response = await fetch(
        `${API_URL}/documents/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response
        .json()
        .catch(() => ({}));

      console.log("UPLOAD STATUS:", response.status);
      console.log("UPLOAD RESPONSE:", data);

      if (!response.ok) {
        let errorMessage =
          `Upload failed: ${response.status}`;

        if (data.detail) {
          if (
            typeof data.detail === "string"
          ) {
            errorMessage = data.detail;
          } else {
            errorMessage = JSON.stringify(
              data.detail,
              null,
              2
            );
          }
        }

        throw new Error(errorMessage);
      }

      // Try different possible backend response formats
      const uploadedDocumentId =
        data.document_id ??
        data.id ??
        data.document?.id;

      if (!uploadedDocumentId) {
        console.error(
          "No document ID found:",
          data
        );

        throw new Error(
          "PDF uploaded, but the backend did not return a document ID."
        );
      }

      setDocumentId(
        Number(uploadedDocumentId)
      );

      setDocumentName(
        data.filename ||
          data.file_name ||
          data.document?.filename ||
          file.name
      );

      setDocumentPages(
        data.page_count ||
          data.pages ||
          data.document?.page_count ||
          null
      );

      // Clear previous conversation
      setMessages([]);

      console.log(
        "DOCUMENT ID:",
        uploadedDocumentId
      );

    } catch (err) {
      console.error(
        "UPLOAD ERROR:",
        err
      );

      const realError =
        err?.message ||
        "Unable to upload PDF.";

      setError(realError);

      alert(realError);

    } finally {
      setUploading(false);

      // Allow selecting the same file again
      event.target.value = "";
    }
  };

  // ==========================================
  // CHAT
  // ==========================================

  const sendMessage = async (
    text = question
  ) => {
    const cleanQuestion =
      text.trim();

    if (!cleanQuestion) {
      return;
    }

    if (!documentId) {
      alert(
        "Please upload a PDF first."
      );
      return;
    }

    if (loading) {
      return;
    }

    // Clear previous error
    setError("");

    // Add user message immediately
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: cleanQuestion,
      },
    ]);

    // Clear input
    setQuestion("");

    // Start loading
    setLoading(true);

    try {
      const requestBody = {
  user_id: 1,
  question: cleanQuestion,
  document_id: Number(documentId),
  top_k: 5,
};

      console.log(
        "================================"
      );

      console.log(
        "SENDING CHAT REQUEST"
      );

      console.log(
        "URL:",
        `${API_URL}/chat/`
      );

      console.log(
        "BODY:",
        requestBody
      );

      console.log(
        "DOCUMENT ID:",
        documentId
      );

      console.log(
        "================================"
      );

      const response = await fetch(
        `${API_URL}/chat/`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify(
            requestBody
          ),
        }
      );

      console.log(
        "CHAT STATUS:",
        response.status
      );

      // Try to read JSON response
      const data = await response
        .json()
        .catch(() => ({}));

      console.log(
        "CHAT RESPONSE:",
        data
      );

      // ==========================================
      // HANDLE BACKEND ERROR
      // ==========================================

      if (!response.ok) {
        let errorMessage =
          `Server error: ${response.status}`;

        if (data.detail) {
          if (
            typeof data.detail ===
            "string"
          ) {
            errorMessage =
              data.detail;
          } else {
            errorMessage =
              JSON.stringify(
                data.detail,
                null,
                2
              );
          }
        } else if (data.message) {
          if (
            typeof data.message ===
            "string"
          ) {
            errorMessage =
              data.message;
          } else {
            errorMessage =
              JSON.stringify(
                data.message,
                null,
                2
              );
          }
        }

        throw new Error(
          errorMessage
        );
      }

      // ==========================================
      // SUCCESS
      // ==========================================

      const answer =
        data.answer ||
        "No answer was returned by the AI.";

      const sources =
        Array.isArray(data.sources)
          ? data.sources
          : [];

      // Add AI answer
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: answer,
          sources: sources,
        },
      ]);

    } catch (err) {
      // ==========================================
      // REAL ERROR
      // ==========================================

      console.error(
        "CHAT ERROR:",
        err
      );

      let realError =
        "Unknown error";

      if (err?.message) {
        realError = err.message;
      } else if (
        typeof err === "string"
      ) {
        realError = err;
      } else {
        try {
          realError =
            JSON.stringify(
              err,
              null,
              2
            );
        } catch {
          realError =
            "Unknown error";
        }
      }

      console.error(
        "REAL CHAT ERROR:",
        realError
      );

      setError(
        `Chat request failed: ${realError}`
      );

      // Show error inside chat
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            `Chat request failed:\n${realError}`,
          isError: true,
        },
      ]);

    } finally {
      setLoading(false);
    }
  };

  // ==========================================
  // ENTER KEY
  // ==========================================

  const handleKeyDown = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      sendMessage();
    }
  };

  // ==========================================
  // NEW CHAT
  // ==========================================

  const handleNewChat = () => {
    setMessages([]);
    setQuestion("");
    setError("");
  };

  // ==========================================
  // SUGGESTED QUESTIONS
  // ==========================================

  const handleSuggestion = (text) => {
    sendMessage(text);
  };

  // ==========================================
  // UI
  // ==========================================

  return (
    <div className="app">

      {/* ======================================
          SIDEBAR
      ====================================== */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            📚
          </div>

          <div>
            <h1>
              StudyMate AI
            </h1>

            <p>
              Learn smarter with your notes
            </p>
          </div>

        </div>

        {/* NEW CHAT */}

        <button
          className="new-chat-btn"
          onClick={
            handleNewChat
          }
        >
          <span>＋</span>

          New Chat
        </button>

        {/* DOCUMENT */}

        <div className="document-section">

          <div className="section-title">
            DOCUMENT
          </div>

          {documentId ? (
            <div className="document-card">

              <div className="document-icon">
                📄
              </div>

              <div className="document-info">

                <strong>
                  {documentName ||
                    "Study Material.pdf"}
                </strong>

                <span>
                  {documentPages
                    ? `${documentPages} pages`
                    : "PDF document"}
                </span>

              </div>

              <div className="success-icon">
                ✓
              </div>

            </div>
          ) : (
            <div className="empty-document">
              No PDF uploaded
            </div>
          )}

          {/* UPLOAD */}

          <label className="upload-btn">

            <span>＋</span>

            {uploading
              ? "Uploading..."
              : "Upload PDF"}

            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={
                handleUpload
              }
              disabled={
                uploading
              }
              hidden
            />

          </label>

        </div>

        {/* BACKEND STATUS */}

        <div className="backend-status">

          <span className="status-dot"></span>

          Backend Connected

        </div>

      </aside>

      {/* ======================================
          MAIN
      ====================================== */}

      <main className="main">

        {/* HEADER */}

        <header className="chat-header">

          <div>

            <h2>
              Chat with your
              study material
            </h2>

            <p>
              Ask questions and get
              answers directly from
              your uploaded PDF.
            </p>

          </div>

          <div className="rag-badge">
            ✨ RAG AI
          </div>

        </header>

        {/* ====================================
            CHAT AREA
        ==================================== */}

        <section className="chat-area">

          {/* WELCOME */}

          {messages.length === 0 && (
            <div className="welcome">

              <div className="robot-icon">
                🤖
              </div>

              <h2>
                {documentId
                  ? "Ask anything about your PDF"
                  : "Upload a PDF to get started"}
              </h2>

              <p>
                {documentId
                  ? "I'll find relevant information from your study material."
                  : "Upload your study material and start asking questions."}
              </p>

              {documentId && (
                <div className="suggestions">

                  <button
                    onClick={() =>
                      handleSuggestion(
                        "Summarize this document"
                      )
                    }
                  >
                    Summarize this document
                  </button>

                  <button
                    onClick={() =>
                      handleSuggestion(
                        "What are the main topics?"
                      )
                    }
                  >
                    What are the main topics?
                  </button>

                  <button
                    onClick={() =>
                      handleSuggestion(
                        "Explain the important concepts"
                      )
                    }
                  >
                    Explain important concepts
                  </button>

                </div>
              )}

            </div>
          )}

          {/* MESSAGES */}

          {messages.map(
            (
              message,
              index
            ) => (

              <div
                key={index}
                className={`message-row ${
                  message.role ===
                  "user"
                    ? "user-row"
                    : "assistant-row"
                }`}
              >

                {/* AI AVATAR */}

                {message.role ===
                  "assistant" && (
                  <div className="avatar">
                    🤖
                  </div>
                )}

                <div className="message-content">

                  <div className="message-name">

                    {message.role ===
                    "user"
                      ? "You"
                      : "StudyMate AI"}

                  </div>

                  <div
                    className={`message-bubble ${
                      message.role ===
                      "user"
                        ? "user-message"
                        : message.isError
                        ? "assistant-message error-chat"
                        : "assistant-message"
                    }`}
                  >
                    {message.content}
                  </div>

                  {/* SOURCES */}

                  {message.sources &&
                    message.sources.length >
                      0 && (

                    <div className="sources">

                      <strong>
                        Sources:
                      </strong>

                      {message.sources.map(
                        (
                          source,
                          sourceIndex
                        ) => (

                          <span
                            key={
                              sourceIndex
                            }
                            className="source-tag"
                          >
                            Page{" "}
                            {
                              source.page_number
                            }
                          </span>

                        )
                      )}

                    </div>

                  )}

                </div>

              </div>

            )
          )}

          {/* LOADING */}

          {loading && (
            <div className="message-row assistant-row">

              <div className="avatar">
                🤖
              </div>

              <div className="message-content">

                <div className="message-name">
                  StudyMate AI
                </div>

                <div className="message-bubble assistant-message">

                  <div className="typing">

                    <span></span>
                    <span></span>
                    <span></span>

                  </div>

                  Thinking...

                </div>

              </div>

            </div>
          )}

        </section>

       {/* ====================================
    BEAUTIFUL CHAT INPUT
==================================== */}

<div className="input-section">

  {/* ERROR */}

  {error && (
    <div className="error-message">
      {error}
    </div>
  )}

  {/* INPUT BOX */}

  <div className="input-box">

    <textarea
      value={question}

      onChange={(event) => {
        setQuestion(event.target.value);

        // Automatically expand while typing
        event.target.style.height = "auto";

        event.target.style.height =
          Math.min(
            event.target.scrollHeight,
            160
          ) + "px";
      }}

      onKeyDown={handleKeyDown}

      placeholder={
        documentId
          ? "Ask anything about your PDF..."
          : "Upload a PDF first..."
      }

      disabled={
        !documentId ||
        loading
      }

      rows={1}
    />

    <button
      className="send-btn"

      onClick={() => sendMessage()}

      disabled={
        !documentId ||
        !question.trim() ||
        loading
      }

      title="Send message"
    >

      {loading ? (
        <span className="chat-loading">
          <span></span>
          <span></span>
          <span></span>
        </span>
      ) : (
        <span className="send-icon">
          ➤
        </span>
      )}

    </button>

  </div>


        </div>
    </main>

    </div>
  );
}

export default App;