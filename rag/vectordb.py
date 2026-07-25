import chromadb


client = chromadb.PersistentClient(
    path="vector_db/chroma"
)


collection = client.get_or_create_collection(
    name="pdf_documents"
)



def store_documents(chunks, embeddings):

    ids = []
    documents = []
    metadatas = []


    for i, chunk in enumerate(chunks):

        ids.append(str(i))

        documents.append(
            chunk["content"]
        )

        metadatas.append({

    "type": chunk.get(
        "type",
        "unknown"
    ),

    "page": chunk.get(
        "page",
        -1
    ),

    "source": "Employee-Handbook-multimodal-test.pdf",

    "chunk_id": i

})


    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )