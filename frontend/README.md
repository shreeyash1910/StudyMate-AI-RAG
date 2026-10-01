# StudyMate AI Frontend

A polished React + Vite frontend for the **Chat With Your Study Material** FastAPI/RAG backend.

## Requirements

- Python/FastAPI backend running at `http://127.0.0.1:8000`
- Node.js 18+ recommended
- npm

## Run

```bash
npm install
npm run dev
```

Then open the URL printed by Vite, normally:

`http://localhost:5173`

## Backend URL

Create `.env` in this folder:

```env
VITE_API_URL=http://127.0.0.1:8000
```

If the backend uses another port, change it there.

## Current API integration

The UI connects to:

- `POST /documents/upload`
- `POST /chat/`
- `GET /conversations/`
- `POST /conversations/`

The frontend is intentionally compatible with the RAG response structure you already tested in Swagger.

## Important

Your FastAPI backend must allow the frontend origin through CORS. Add the CORS middleware shown in the setup instructions from ChatGPT before running the frontend.

## Build

```bash
npm run build
```

The production files are generated in `dist/`.
