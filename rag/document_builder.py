from rag.pdf_loader import extract_text
from rag.image_processor import extract_images
from rag.table_processor import extract_tables



def build_documents(pdf_path):

    documents = []


    # 1- Text
    pages = extract_text(pdf_path)

    for page in pages:

        if page["text"].strip():

            documents.append({
                "type": "text",
                "page": page["page"],
                "content": page["text"]
            })


    # 2- Images
    images = extract_images(pdf_path)

    for image in images:

        documents.append({
            "type": "image",
            "page": image["page"],
            "content": f"Image extracted from page {image['page']}",
            "path": image["path"]
        })


    # 3- Tables
    tables = extract_tables(pdf_path)

    for table in tables:

        table_text = "\n".join(
    [
        " | ".join(
            [
                str(cell) if cell is not None else ""
                for cell in row
            ]
        )
        for row in table["content"]
        if row
    ]
)
        


        if len(table_text.strip()) > 50:

            documents.append({
                "type": "table",
                "page": table["page"],
                "content": table_text
            })


    return documents