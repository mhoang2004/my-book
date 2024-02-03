import fitz  # PyMuPDF


def pdf_to_html(pdf_path):
    doc = fitz.open(pdf_path)

    pages = []

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text("text")
        pages.append({"number": page_num + 1, "text": text})
    doc.close()

    return pages
