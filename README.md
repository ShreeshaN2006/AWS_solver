# AWS Academy Course Copilot

Full-stack MVP for an AI-powered assistant for **AWS Academy Cloud Foundations** (Canvas course ID `183194`).

## What is implemented

- **Backend (FastAPI + Python)**
  - Course-aware APIs for dashboard, modules, tutor chat, practice, labs, progress, and study plan.
  - Canvas HTML export parser (`/api/canvas/parse`).
  - Document ingestion pipeline (cleaning/chunking/embedding) and retrieval with module filtering.
  - LLM provider abstraction (`openai` or `bedrock`) selected via env variable.
  - Source citation-ready tutor responses.
- **Frontend (React + TypeScript + Tailwind)**
  - Responsive learning dashboard shell with all requested page entries.
  - Dashboard metrics + module listing from backend.
  - AI Tutor chat connected to backend.
- **Data & config**
  - Sample course data for all 10 modules and extra course sections.
  - `.env.example` for local configuration.

## Repository layout

- `/backend` – FastAPI app and tests
- `/frontend` – React app (Vite)
- `/data/examples/course_data.json` – example imported course content

## Backend setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --app-dir backend --reload
```

Backend base URL: `http://localhost:8000`

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

Set `VITE_API_BASE_URL` if backend runs elsewhere (default: `http://localhost:8000/api`).

## Testing

Run focused backend tests:

```bash
pytest backend/tests -c backend/pytest.ini
```

## Security and reliability notes

- Never commit `.env`, Canvas tokens, or credentials.
- Canvas integration is read-only in this MVP.
- Lab assistant only provides guidance; it does not create/modify AWS resources.
- Official graded Canvas assessments remain user-controlled.

## MongoDB

Environment variables are provided for MongoDB integration (`MONGODB_URI`, `MONGODB_DB`).
This MVP keeps local in-memory state for development and tests while preserving modular service boundaries for switching to persistent MongoDB collections.
