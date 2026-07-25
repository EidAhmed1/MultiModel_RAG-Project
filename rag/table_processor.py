import pdfplumber


def extract_tables(pdf_path):

    tables = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_number, page in enumerate(pdf.pages):

            page_tables = page.extract_tables()

            for table_index, table in enumerate(page_tables):

                tables.append({
                    "page": page_number + 1,
                    "table_number": table_index + 1,
                    "content": table
                })

    return tables