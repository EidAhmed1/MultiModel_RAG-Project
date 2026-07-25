import chromadb
from sentence_transformers import SentenceTransformer

from rag.reranker import rerank_documents


# =========================
# Embedding Model
# =========================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =========================
# ChromaDB Connection
# =========================

client = chromadb.PersistentClient(
    path="vector_db/chroma"
)


collection = client.get_collection(
    name="pdf_documents"
)



# =========================
# Remove Duplicates
# =========================

def clean_text(text):

    text = text.replace("|", " ")
    text = text.replace("\n", " ")

    # إزالة المسافات الزائدة
    text = " ".join(text.split())

    return text.lower()



def remove_duplicates(documents):

    unique = []

    seen = set()


    for doc in documents:

        cleaned = clean_text(
            doc["content"]
        )


        # نأخذ أول 200 حرف كـ fingerprint
        fingerprint = cleaned[:200]


        if fingerprint not in seen:

            seen.add(fingerprint)

            unique.append(doc)


    return unique


# =========================
# Retrieval Function
# =========================

def search_documents(
    question,
    top_k=10
):

    # Convert question to embedding

    query_embedding = model.encode(
        question
    )


    # Search in ChromaDB

    results = collection.query(

        query_embeddings=[
            query_embedding.tolist()
        ],

        n_results=top_k
    )


    retrieved_documents = []


    documents = results["documents"][0]

    metadatas = results["metadatas"][0]


    for doc, meta in zip(
        documents,
        metadatas
    ):

        retrieved_documents.append({

            "content": doc,

            "page": meta.get(
                "page",
                "unknown"
            ),

            "type": meta.get(
                "type",
                "unknown"
            ),

            "source": meta.get(
                "source",
                "unknown"
            )
        })



    # Remove duplicate chunks

    retrieved_documents = remove_duplicates(
    retrieved_documents
)


# حذف الـ chunks القصيرة مثل Table of Contents

    retrieved_documents = [
        doc 
        for doc in retrieved_documents
        if len(clean_text(doc["content"])) > 200
    ]



    # Rerank documents

    retrieved_documents = rerank_documents(

        question,

        retrieved_documents,

        top_k=3
    )



    return retrieved_documents