# AI-Powered Proposal Review Assistant

An end-to-end full-stack web application designed to help review, edit, and improve proposal drafts using AI. It leverages a Retrieval-Augmented Generation (RAG) architecture to provide context-aware feedback based on a library of past successful proposals.

##  Features
- **Knowledge Base (RAG):** Upload past `.txt` proposals into a searchable vector database using FAISS.
- **AI Feedback Engine:** Uses LangChain to evaluate drafts for clarity, completeness, and missing sections by comparing them against the past proposals context.
- **Premium Dashboard:** A modern, glassmorphic UI built with React, Tailwind CSS, and TypeScript.
- **Collaborative Editor:** Split-pane interface allowing real-time edits while referencing AI-generated feedback.

##  Technology Stack
- **Frontend:** React, TypeScript, Vite, Tailwind CSS, Lucide Icons, Axios.
- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic.
- **AI & ML:** LangChain, FAISS (Vector Store).
- **Database:** SQLite (local).

##  Running Locally

### 1. Start the Backend
```bash
cd backend
python -m venv venv
# On Windows: .\venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
*API available at `http://localhost:8000/docs`*

### 2. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```
*Dashboard available at `http://localhost:5173`*
