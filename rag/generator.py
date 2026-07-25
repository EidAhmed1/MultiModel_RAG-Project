from typing import List


def build_context(documents: List[dict]) -> str:
    """
    Convert retrieved chunks into a single context string.
    """

    context = ""

    for i, doc in enumerate(documents, start=1):

        context += (
            f"\n\n"
            f"### Source {i}\n"
            f"Page: {doc['page']}\n"
            f"Type: {doc['type']}\n\n"
            f"{doc['content']}"
        )

    return context