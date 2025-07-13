from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import fitz  # PyMuPDF for PDF parsing

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

documents = {}

class QARequest(BaseModel):
    question: str
    document_id: str

class ChallengeResponse(BaseModel):
    document_id: str
    answers: List[str]

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
     print(f"📂 Received file: {file.filename}")  
    ext = file.filename.split('.')[-1].lower()
    content = await file.read()
    if ext == 'pdf':
        text = ""
        with fitz.open(stream=content, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    elif ext == 'txt':
        text = content.decode('utf-8')
    else:
        return {"error": "Unsupported file format"}

    doc_id = str(hash(file.filename + text[:100]))
    documents[doc_id] = text
    from utils import summarize
    summary = summarize(text)
    return {"document_id": doc_id, "summary": summary}

@app.post("/ask")
def ask_question(req: QARequest):
    from utils import answer_question
    text = documents.get(req.document_id, "")
    if not text:
        return {"error": "Document not found"}
    response = answer_question(text, req.question)
    return response

@app.post("/challenge")
def challenge_user(document_id: str):
    from utils import generate_questions
    text = documents.get(document_id, "")
    if not text:
        return {"error": "Document not found"}
    questions = generate_questions(text)
    return {"questions": questions}

@app.post("/evaluate")
def evaluate_challenge(req: ChallengeResponse):
    from utils import generate_questions, evaluate_answers
    text = documents.get(req.document_id, "")
    if not text:
        return {"error": "Document not found"}
    questions = generate_questions(text)
    feedback = evaluate_answers(text, questions, req.answers)
    return {"feedback": feedback}
