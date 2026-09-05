from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import create_chunks
from app.services.embedding_service import create_embeddings
from app.services.vector_service import create_faiss_index


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # 1. Check file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # 2. Create file path
    file_path = UPLOAD_DIR / file.filename

    # 3. Save uploaded PDF
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # 4. Extract PDF text
    pdf_data = extract_text_from_pdf(
        str(file_path)
    )

    # 5. Create chunks
    chunks = create_chunks(
        pdf_data["pages"]
    )

    # 6. Get chunk text
    chunk_texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # 7. Create embeddings
    embeddings = create_embeddings(
        chunk_texts
    )

    # 8. Save document in SQL Server
    document = Document(
        user_id=1,
        filename=file.filename,
        file_path=str(file_path),
        page_count=pdf_data["page_count"]
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # 9. Use the real database document ID
    document_id = document.id

    # 10. Create FAISS index
    vector_info = create_faiss_index(
        embeddings,
        chunks,
        document_id
    )

    # 11. Return result
    return {
        "message": "PDF processed successfully",

        "document_id": document.id,

        "filename": file.filename,

        "pages": pdf_data["page_count"],

        "text_characters": len(
            pdf_data["full_text"]
        ),

        "total_chunks": len(chunks),

        "embedding_dimensions": embeddings.shape[1],

        "total_vectors": vector_info["total_vectors"],

        "vector_dimension": vector_info["dimension"],

        "index_path": vector_info["index_path"],

        "chunks_preview": chunks[:3]
    }