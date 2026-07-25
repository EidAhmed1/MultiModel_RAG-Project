from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []

    for doc in documents:

        content = doc["content"]

        splitted = splitter.split_text(content)

        for chunk in splitted:

            chunks.append({
                "content": chunk,
                "type": doc["type"],
                "page": doc["page"]
            })

    return chunks