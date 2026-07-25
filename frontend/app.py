import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="MultiRAG Assistant",
    page_icon="📄"
)


st.title("📄 MultiRAG PDF Assistant")

st.write(
    "Ask questions from your uploaded PDF"
)


# ==========================
# Upload PDF
# ==========================

st.subheader("Upload PDF")


uploaded_file = st.file_uploader(
    "Choose PDF file",
    type=["pdf"]
)


if uploaded_file:

    if st.button("Upload"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }


        response = requests.post(
            f"{API_URL}/upload",
            files=files
        )


        if response.status_code == 200:

            st.success(
                "PDF uploaded successfully"
            )

        else:

            st.error(
                response.text
            )


# ==========================
# Ask Question
# ==========================

st.divider()


st.subheader("Ask Question")


question = st.text_input(
    "Enter your question"
)


if st.button("Ask"):

    if question:

        response = requests.post(
            f"{API_URL}/ask",
            json={
                "question": question
            }
        )


        if response.status_code == 200:

            data = response.json()


            st.subheader(
                "Answer"
            )

            st.write(
                data["answer"]
            )


            st.subheader(
                "Sources"
            )


            for source in data["sources"]:

                st.write(
                    f"📄 Page: {source['page']} | Type: {source['type']}"
                )


        else:

            st.error(
                response.text
            )