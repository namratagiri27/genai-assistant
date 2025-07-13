# 📄 GenAI Smart Assistant

This app lets users upload documents (PDF/TXT) and:

- Ask questions and get document-based answers with justifications
- Be challenged with logic/comprehension questions
- Get evaluated with feedback

## ⚙️ Tech Stack
- **Backend**: FastAPI, Transformers
- **Frontend**: Streamlit
- **NLP Models**: `distilbert-base-uncased-distilled-squad`

## 🚀 Run Locally

### 1. Clone & Install
```bash
pip install -r app/requirements.txt
```

### 2. Run Backend
```bash
uvicorn app.main:app --reload
```

### 3. Run Frontend
```bash
cd frontend
streamlit run app.py
```

## 🏁 Features

- ✅ Upload PDF/TXT
- ✅ Auto Summary
- ✅ Q&A with justification
- ✅ Logic Questions + Evaluation
