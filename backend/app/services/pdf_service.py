import fitz


def extract_text_from_pdf(file_path: str):

    document = fitz.open(file_path)

    pages = []
    full_text = ""

    for page_number, page in enumerate(document, start=1):

        text = page.get_text()

        pages.append({
            "page_number": page_number,
            "text": text
        })

        full_text += text + "\n"

    page_count = len(document)

    document.close()

    return {
        "page_count": page_count,
        "full_text": full_text,
        "pages": pages
    }