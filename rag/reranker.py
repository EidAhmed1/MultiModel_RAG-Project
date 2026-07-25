from sentence_transformers import CrossEncoder



reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)



def rerank_documents(
    question,
    documents,
    top_k=3,
    threshold=2.0
):

    pairs = []


    for doc in documents:

        pairs.append(
            [
                question,
                doc["content"]
            ]
        )


    scores = reranker_model.predict(
        pairs
    )


    ranked = []


    for doc, score in zip(
        documents,
        scores
    ):

        doc["rerank_score"] = float(score)

        ranked.append(doc)



    ranked = sorted(
        ranked,
        key=lambda x:x["rerank_score"],
        reverse=True
    )


    filtered = [
    doc
    for doc in ranked
    if doc["rerank_score"] >= threshold
]


    return filtered[:top_k]