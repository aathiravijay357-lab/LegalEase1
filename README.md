# LegalEase

AI-assisted legal document drafting application based on the supplied project specification.

## Features

- Streamlit frontend
- FastAPI backend
- Gemini API integration using the current `google-genai` SDK
- User inputs for document type, parties, terms, and effective date
- Editable generated document
- TXT export
- DOCX export
- PDF export
- Optional logo support in `assets/logo.png`
- Health-check endpoint

## 1. Create virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

## 2. Install packages

```bash
pip install -r requirements.txt
```

## 3. Configure Gemini

Copy `.env.example` to `.env` and put your Gemini API key into:

```text
GEMINI_API_KEY=YOUR_KEY_HERE
GEMINI_MODEL=gemini-3.8-flash
BACKEND_URL=http://127.0.0.1:8000
```

## 4. Start backend

From the project root:

```bash
uvicorn backend.main:app --reload --port 8000
```

## 5. Start frontend

Open another terminal in the same project folder, activate the virtual environment, then:

```bash
streamlit run frontend/app.py
```

## 6. Test

Open the Streamlit URL shown in the terminal, normally:

http://localhost:8501

Backend health check:

http://127.0.0.1:8000/health

## Optional logo

Put a PNG logo at:

`assets/logo.png`

It will be included in DOCX and PDF exports.
