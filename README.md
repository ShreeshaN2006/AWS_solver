# AWS Academy Course Copilot

> **An Intelligent, Course-Aware AI Agent & Study Assistant for AWS Academy Cloud Foundations (Course ID: 183194)**

![AWS Academy Course Copilot](https://img.shields.io/badge/Course-AWS%20Academy%20Cloud%20Foundations-FF9900?logo=amazon-aws)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)
![React](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-61DAFB?logo=react)
![MongoDB](https://img.shields.io/badge/Database-MongoDB%207.0-47A248?logo=mongodb)
![Tests](https://img.shields.io/badge/Pytest-Passing-brightgreen)

---

## 1. Project Overview

**AWS Academy Course Copilot** is a course-aware AI educational companion designed to help students comprehend, study, practice, and successfully complete the **AWS Academy Cloud Foundations** curriculum hosted on Canvas LMS.

Unlike simple question-and-answer chatbots, the Course Copilot operates as a full learning agent with direct access to official course materials, semantic vector retrieval (RAG), hands-on laboratory guidance, assessment practice, and adaptive study scheduling.

### Official Course Structure (Canvas LMS ID: 183194)
- **Course Canvas URL:** `https://awsacademy.instructure.com/courses/183194/modules`
- **10 Core Curriculum Modules:**
  1. **Module 1** - Cloud Concepts Overview
  2. **Module 2** - Cloud Economics and Billing
  3. **Module 3** - AWS Global Infrastructure Overview
  4. **Module 4** - AWS Cloud Security
  5. **Module 5** - Networking and Content Delivery
  6. **Module 6** - Compute
  7. **Module 7** - Storage
  8. **Module 8** - Databases
  9. **Module 9** - Cloud Architecture
  10. **Module 10** - Auto Scaling and Monitoring
- **Additional Sections Supported:** Course Introduction, Final Course Assessment, AWS Academy Learner Lab Sandbox, Certification Resources (CLF-C02), Feedback & Surveys, Digital Badges & Completion Certificates, and Terms & Conditions.
- **6 Supported Practical Hands-On Labs:**
  1. *Introduction to AWS IAM*
  2. *Build your VPC and Launch a Web Server*
  3. *Introduction to Amazon EC2*
  4. *Working with EBS*
  5. *Build a Database Server (RDS Multi-AZ)*
  6. *Scale and Load Balance your Architecture (ALB + ASG)*

---

## 2. Technology Stack & Architecture

- **Frontend:** React 18, TypeScript, Tailwind CSS, Lucide Icons, Vite.
- **Backend:** Python 3.11, FastAPI, Motor (Async MongoDB Driver), Pydantic v2.
- **Database:** MongoDB 7.0 (with real connection `mongodb://localhost:27017` and indexing across courses, modules, chunks, chats, practice attempts, labs, and study plans).
- **AI & RAG Engine:**
  - **Provider Abstraction:** Dynamic switching between `local_mock` (zero API key offline heuristic provider), `openai` (GPT-4o-mini + text-embedding-3-small), and `bedrock` (Claude 3 + Titan Embeddings).
  - **Semantic Retrieval (RAG):** Dense vector index with cosine similarity, chunk-level metadata (Course ID, Module ID, Module Title, Document Name, Page Number, Timestamp, Source URL).
- **Document Processing:** PyMuPDF (`pymupdf`) for PDF extraction, BeautifulSoup4 for Canvas HTML module parsing, text chunker with sliding sentence-boundary overlap.

---

## 3. Directory Layout

```
AWS_solver/
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI application lifecycle and routers
│   │   ├── config.py             # Pydantic v2 Settings & environment variables
│   │   ├── database.py           # MongoDB async connection & index manager
│   │   ├── models/               # Pydantic schemas (course, document, chat, practice, lab, progress, planner)
│   │   ├── services/
│   │   │   ├── llm_provider.py   # BaseLLMProvider, OpenAI, Bedrock, LocalMock
│   │   │   ├── vector_store.py   # Vector similarity retrieval & MongoDB persistence
│   │   │   ├── ingestion.py      # Canvas HTML parser & PyMuPDF extractor
│   │   │   ├── agent.py          # 12 Modular Tools and Copilot Agent
│   │   │   ├── lab_service.py    # 6 AWS Guided Labs & Troubleshooter
│   │   │   ├── planner_service.py# Adaptive study scheduling & progress analytics
│   │   │   └── canvas_api.py     # Read-only Canvas LMS integration
│   │   ├── seed_data/            # Seed data for 10 modules, 6 labs, practice questions
│   │   └── api/                  # RESTful API route endpoints
│   ├── tests/                    # Pytest test suite (RAG, Agent tools, Ingestion, End-to-End API)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/           # Navbar, Sidebar, UI widgets
│   │   ├── context/              # CourseContext (shared state & navigation)
│   │   ├── pages/                # 10 dedicated views (Dashboard, Modules, Workspace, Chat, etc.)
│   │   ├── services/api.ts       # Typed REST API client
│   │   └── types/index.ts        # TypeScript data models
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── nginx.conf
├── sample_data/
│   └── aws_academy_canvas_export.html # Pre-configured Canvas LMS course export
├── docker-compose.yml
└── README.md
```

---

## 4. Installation & Local Setup

### Prerequisites
1. **Python 3.11+** installed.
2. **Node.js 18+** & **npm** installed.
3. **MongoDB** service running on `localhost:27017` (or MongoDB Atlas URI).

### Step 1: Clone and Set Up Virtual Environment

```bash
git clone <repository_url>
cd AWS_solver

# Create Python virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# (Or Linux / macOS)
# source venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

### Step 2: Configure Environment Variables

```bash
cp backend/.env.example backend/.env
```
*(The default configuration uses `LLM_PROVIDER=local_mock` and `MONGODB_URI=mongodb://localhost:27017`, allowing the application to run completely out of the box with zero external API keys!)*

### Step 3: Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

---

## 5. Running the Application

### Option A: Local Development (Recommended)

1. **Start the Backend API Server:**
   ```powershell
   .\venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
   ```
   *The backend will automatically connect to MongoDB, verify indexes, and seed the complete 10 modules, 6 labs, practice question bank, and textbook knowledge chunks.*
   - Interactive Swagger API Documentation: `http://127.0.0.1:8000/docs`
   - Health Check: `http://127.0.0.1:8000/api/health`

2. **Start the Frontend Development Server (in a second terminal):**
   ```powershell
   cd frontend
   npm run dev
   ```
   - Open your browser to: `http://localhost:3000` (or `http://localhost:5173`)

### Option B: Docker Compose

```bash
docker-compose up --build
```
- Frontend UI: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- MongoDB: `localhost:27017`

---

## 6. Running Automated Tests

To run the complete backend test suite:
```powershell
$env:PYTHONPATH="backend"
.\venv\Scripts\pytest backend\tests -v
```

To verify the frontend TypeScript and production build:
```powershell
cd frontend
npm run build
```

---

## 7. Key Features & How to Use Them

### 1. Main Dashboard
- High-level KPIs: Overall Study Progress, Total Modules, Completed, In Progress, Remaining, and Study Time.
- Recommended Next Activity with one-click launch.
- Organised list of all 10 core modules with direct links to Study Workspace, Practice, and Labs.
- Active weak topics and upcoming tasks.

### 2. Course Modules
- Complete catalog of all 10 core modules and extra sections (Introduction, Assessment, Sandbox, Certification, Badges).
- Filter by All, 10 Core Modules, Hands-on Labs, or Extra Sections.
- Search by AWS service (e.g. `S3`, `VPC`, `RDS`) or keyword.
- Expandable resource checklists with estimated completion time.

### 3. Module Learning Workspace
- **Split-View Layout:** Read module notes and syllabus topics on the left; interact with the embedded AI Copilot on the right.
- Mark learning resources as completed locally.
- Instant topic explanations and lesson summaries with one click.

### 4. AI Tutor Chat
- Full conversation interface with multi-session history.
- Grounded in official AWS Academy course materials using vector embeddings (RAG).
- Verified course citations display document name, page number, and relevant excerpt.
- Context selector: restrict search to an individual module or across the full curriculum.

### 5. Knowledge Check Practice
- Original practice questions covering Multiple Choice, True/False, Scenario-based, Conceptual, and Difficult questions.
- Practice single modules or take a full 15-question Comprehensive Mock Exam.
- Immediate feedback mode or exam submission mode.
- Post-session diagnostic report: Score percentage, weak concepts detection, recommended revision topics, and full rubric explanations.

### 6. AWS Lab Assistant
- Full walkthroughs for all 6 practical labs:
  1. *Introduction to AWS IAM*
  2. *Build your VPC and Launch a Web Server*
  3. *Introduction to Amazon EC2*
  4. *Working with EBS*
  5. *Build a Database Server*
  6. *Scale and Load Balance your Architecture*
- AWS Console navigation paths, sequential steps, expected results, and common student pitfalls.
- Stage confirmation checkboxes to ensure intentional progress tracking.
- Interactive Troubleshooter: paste console error messages (e.g. `UnauthorizedOperation`, `Timed Out`) to get diagnostic analysis and console checks.

### 7. Progress Analytics
- Visual tracking of status states: *Not Started*, *In Progress*, *Needs Revision*, *Ready for Assessment*, *Completed*.
- Concept mastery breakdown: Understood Topics vs Topics Requiring Revision.
- Clear distinction between locally tracked progress and official Canvas LMS grading.

### 8. Personal Study Planner
- Configurable study parameters: weekly available hours slider, daily study target dropdown, and completion deadline picker.
- Synthesizes a prioritized 7-day schedule focusing on weak topics and unfinished labs.
- Interactive day-by-day checklist with toggleable task completion.

### 9. Document Library & Ingestion
- Upload Canvas LMS course modules export (`.html`) to extract modules, items, and external tools.
- Upload course student guides (`.pdf`) or video transcripts (`.txt`) with automatic PyMuPDF extraction, semantic chunking, and vector indexing.
- Vector Chunks Inspector to inspect indexed chunks with source URLs and similarity scores.

### 10. Settings & Integrations
- Switch AI Provider between **Local AI / Offline Mock**, **OpenAI API**, and **Amazon Bedrock**.
- Test Canvas LMS connection and trigger read-only course module synchronization.
- MongoDB connection and database status monitor.

---

## 8. Academic Integrity & Safety Safeguards

1. **Student Assessment Independence:** The Course Copilot generates original practice quizzes for study and never automatically solves, selects, or submits official live graded Canvas LMS quizzes or assignments.
2. **Read-Only LMS Queries:** The Canvas integration uses read-only REST API requests. It never alters grades or modifies student records.
3. **No Direct Account Mutation:** The AWS Lab Assistant provides console guidance and troubleshooting analysis. It will never create, modify, or terminate AWS resources in a student's personal account or sandbox.
4. **Credential Security:** Password credentials and API tokens are never requested or stored in plaintext. Retrieved course materials are treated as untrusted data that cannot override system security guardrails.

---

## 9. License

Developed for AWS Academy educational instruction and certification preparation.
