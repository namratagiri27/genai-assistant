import streamlit as st
import requests

st.title("📄 GenAI Smart Assistant")

backend_url = "http://localhost:8000"

uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
if uploaded_file:
    with st.spinner("Uploading and summarizing..."):
        files = {"file": uploaded_file.getvalue()}
        res = requests.post(f"{backend_url}/upload", files={"file": uploaded_file})
        if res.ok:
            data = res.json()
            st.session_state.doc_id = data["document_id"]
            st.subheader("🔍 Summary:")
            st.write(data["summary"])
        else:
            st.error("Upload failed.")

if "doc_id" in st.session_state:
    mode = st.radio("Select Mode", ["Ask Anything", "Challenge Me"])

    if mode == "Ask Anything":
        question = st.text_input("Type your question:")
        if question:
            res = requests.post(f"{backend_url}/ask", json={
                "question": question,
                "document_id": st.session_state.doc_id
            })
            ans = res.json()
            st.write(f"**Answer:** {ans['answer']}")
            st.caption(ans['justification'])

    if mode == "Challenge Me":
        if st.button("Generate Questions"):
            res = requests.post(f"{backend_url}/challenge", params={"document_id": st.session_state.doc_id})
            st.session_state.questions = res.json()["questions"]

        if "questions" in st.session_state:
            answers = []
            for q in st.session_state.questions:
                answers.append(st.text_input(f"{q}", key=q))

            if st.button("Submit Answers"):
                res = requests.post(f"{backend_url}/evaluate", json={
                    "document_id": st.session_state.doc_id,
                    "answers": answers
                })
                for feedback in res.json()["feedback"]:
                    st.markdown(f"**Q:** {feedback['question']}")
                    st.write(f"✅ Your Answer: {feedback['your_answer']}")
                    st.write(f"📌 Expected: {feedback['expected']}")
                    st.write(f"💡 Result: {feedback['result']}")
                    st.caption(feedback['justification'])
