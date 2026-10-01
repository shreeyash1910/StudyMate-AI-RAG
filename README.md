# 📚 StudyMate AI — Chat With Your Study Material

> An AI-powered RAG application that lets students upload PDF study material and ask questions about it using natural language.

🌐 **Live Demo:** https://studymate-ai-rag-frontend.onrender.com  
⚡ **Backend API:** https://studymate-ai-rag-backend.onrender.com  
📖 **API Documentation:** https://studymate-ai-rag-backend.onrender.com/docs

---

## 🎯 Overview

Students often spend a lot of time searching through large PDF documents to find specific information.

**StudyMate AI** solves this problem by allowing users to upload their study material and ask questions directly.

The application uses **Retrieval-Augmented Generation (RAG)** to find relevant information from the uploaded document and then uses an LLM to generate an answer based on that information.

---

## ✨ Features

- 📄 Upload PDF study material
- 🤖 AI-powered question answering
- 🔎 Semantic search using embeddings
- ⚡ Fast similarity search with FAISS
- 🧠 Retrieval-Augmented Generation (RAG)
- 📚 Shows relevant source pages
- 💬 Interactive chat interface
- 🗄️ PostgreSQL database integration
- 🔌 REST API using FastAPI
- 🌐 Deployed frontend and backend

---

## 🧠 How It Works

```text
Upload PDF
    ↓
Extract Text
    ↓
Split Text into Chunks
    ↓
Generate Embeddings
    ↓
Store Embeddings in FAISS
    ↓
User Asks a Question
    ↓
Convert Question into Embedding
    ↓
Find Relevant Chunks
    ↓
Send Context to LLM
    ↓
Generate Answer
    ↓
Display Answer + Sources
