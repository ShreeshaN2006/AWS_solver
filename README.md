# AWS Academy Course Copilot

Full-stack MVP for an AI-powered assistant for **AWS Academy Cloud Foundations** (Canvas course ID 183194).

## What is implemented

- **Backend (FastAPI + Python)**
  - Course-aware APIs for dashboard, modules, tutor chat, practice, labs, progress, and study plan.
  - Canvas HTML export parser (/api/canvas/parse).
  - Document text cleaning, chunking, provider-backed embeddings, and module-filtered similarity retrieval.
  - Real OpenAI Chat Completions and embeddings integration.
  - Real Amazon Bedrock Converse and Titan Text Embeddings V2 integration.
  - Source-aware tutor responses that pass retrieved course excerpts to the configured model.
- **Frontend (React + TypeScript + Tailwind)**
  - Responsive learning dashboard shell with all requested page entries.
  - Dashboard metrics + module listing from backend.
  - AI Tutor chat connected to backend.
- **Data & config**
  - Sample course data for all 10 modules and extra course sections.
  - .env.example for local configuration.

## Repository layout

- /backend – FastAPI app and tests
- /frontend – React app (Vite)
- /data/examples/course_data.json – example imported course content

## Backend setup

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --app-dir backend --reload
~~~

Set one AI provider in .env.

### OpenAI

~~~env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
~~~

### Amazon Bedrock

~~~env
LLM_PROVIDER=bedrock
BEDROCK_REGION=us-east-1
BEDROCK_MODEL_ID=amazon.nova-micro-v1:0
BEDROCK_EMBEDDING_MODEL_ID=amazon.titan-embed-text-v2:0
BEDROCK_EMBEDDING_DIMENSIONS=1024
~~~

For Bedrock, configure AWS credentials using the normal AWS SDK credential chain and grant the application permission to invoke the selected foundation models. The app does not store AWS credentials.

Backend base URL: http://localhost:8000

## Frontend setup

~~~bash
cd frontend
npm install
npm run dev
~~~

Frontend URL: http://localhost:5173

Set VITE_API_BASE_URL if backend runs elsewhere (default: http://localhost:8000/api).

## Document ingestion and retrieval

Use POST /api/documents/ingest to submit extracted text with its module and source metadata. The service chunks the text, creates semantic embeddings with the selected provider, and keeps the chunks in the current application process for module-filtered retrieval.

**Important MVP limitation:** indexed chunks and learner progress are still held in memory, not persisted in MongoDB. Restarting the backend clears the indexed chunks. MongoDB connection settings exist, but persistent document/vector storage is a later implementation step.

Use the same provider and embedding model for ingestion and tutor search. If switching providers or embedding models, re-ingest the documents so all stored vectors are in the same embedding space.

## Testing

Run backend tests:

~~~bash
pytest backend/tests -c backend/pytest.ini
~~~

The retrieval tests mock embedding functions, so they do not need API keys. The real tutor and ingestion requests do require configured OpenAI or Bedrock access.

## Security and reliability notes

- Never commit .env, Canvas tokens, or credentials.
- Canvas integration is read-only in this MVP.
- Lab assistant only provides guidance; it does not create or modify AWS resources.
- Official graded Canvas assessments remain user-controlled.
