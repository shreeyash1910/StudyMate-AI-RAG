from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(pages):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    for page in pages:

        page_number = page["page_number"]
        page_text = page["text"]

        if not page_text.strip():
            continue

        page_chunks = text_splitter.split_text(
            page_text
        )

        for chunk_number, chunk_text in enumerate(
            page_chunks,
            start=1
        ):

            chunks.append({
                "text": chunk_text,
                "page_number": page_number,
                "chunk_number": chunk_number
            })

    return chunks