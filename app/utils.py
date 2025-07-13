from transformers import pipeline
import re

qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
summarizer = pipeline("summarization")

def summarize(text):
    return summarizer(text[:1000], max_length=150, min_length=40, do_sample=False)[0]['summary_text']

def answer_question(context, question):
    result = qa_pipeline(question=question, context=context[:4000])
    return {
        "answer": result['answer'],
        "score": result['score'],
        "justification": f"This answer is based on the context from the first part of the document."
    }

def generate_questions(context):
    sentences = re.split(r'[.!?]', context)
    questions = []
    for i, s in enumerate(sentences):
        if len(s.strip().split()) > 6 and len(questions) < 3:
            questions.append(f"What is the implication of: \"{s.strip()}\"?")
    return questions

def evaluate_answers(context, questions, answers):
    feedback = []
    for q, a in zip(questions, answers):
        score = qa_pipeline(question=q, context=context[:4000])
        is_correct = a.lower() in score['answer'].lower()
        feedback.append({
            "question": q,
            "your_answer": a,
            "expected": score['answer'],
            "result": "Correct" if is_correct else "Incorrect",
            "justification": "Checked using question-answering pipeline."
        })
    return feedback
