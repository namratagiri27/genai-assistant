# 📄 GenAI Smart Assistant

This app lets users upload documents (PDF/TXT) and:

- Ask questions and get document-based answers with justifications
- Be challenged with logic/comprehension questions
- Get evaluated with feedback

## ⚙️ Tech Stack
Python, FastAPI, Transformers, Streamlit, Git, Machine Learning (Hugging Face Models)
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

## 🧪 Postman API Collection

Postman tests for all API endpoints are included in the repo under the `/postman` folder.

[Download Collection](postman/GenAI%20Assistant%20API.postman_collection.json)


## 🏁 Features

- ✅ Upload PDF/TXT
- ✅ Auto Summary
- ✅ Q&A with justification
- ✅ Logic Questions + Evaluation
