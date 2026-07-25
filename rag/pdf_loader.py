import fitz  # PyMuPDF


def extract_text(pdf_path):

    doc = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(doc):

        text = page.get_text()

        pages.append({
            "page": page_number + 1,
            "text": text
        })

    return pages