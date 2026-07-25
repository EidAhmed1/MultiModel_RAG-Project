from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

import os
import shutil

from rag.retriever import search_documents
from rag.generator import build_context
from rag.llm import generate_answer


app = FastAPI(
    title="MultiRAG API",
    version="1.0.0"
)


UPLOAD_FOLDER = "uploads/pdfs"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@app.get("/")
def root():

    return {
        "message": "MultiRAG API is running"
    }



@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):

        return {
            "error": "Only PDF files are allowed"
        }


    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )


    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    return {
        "message": "PDF uploaded successfully",
        "filename": file.filename
    }




# =====================
# Ask RAG
# =====================

class QuestionRequest(BaseModel):

    question: str



@app.post("/ask")
def ask_question(request: QuestionRequest):

    # Retrieve relevant documents
    results = search_documents(
        request.question
    )

    # Build context
    context = build_context(
        results
    )

    # Generate answer
    answer = generate_answer(
        request.question,
        context
    )

    return {
    "answer": answer,
    "sources": [
        {
            "page": doc["page"],
            "type": doc["type"]
        }
        for doc in results
    ]
}