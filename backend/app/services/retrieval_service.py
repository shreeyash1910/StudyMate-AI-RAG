from pathlib import Path
import json

import faiss
import numpy as np

from app.services.embedding_service import create_embeddings


VECTOR_STORE_DIR = Path("vector_store")


def search_document(
    query: str,
    document_id: int,
    top_k: int = 5
):

    # Paths
    index_path = (
        VECTOR_STORE_DIR
        / f"document_{document_id}.index"
    )

    metadata_path = (
        VECTOR_STORE_DIR
        / f"document_{document_id}.json"
    )

    # Check whether index exists
    if not index_path.exists():

        raise FileNotFoundError(
            f"Vector index not found for document {document_id}"
        )

    if not metadata_path.exists():

        raise FileNotFoundError(
            f"Metadata not found for document {document_id}"
        )

    # Load FAISS index
    index = faiss.read_index(
        str(index_path)
    )

    # Load chunk metadata
    with open(
        metadata_path,
        "r",
        encoding="utf-8"
    ) as file:

        chunks = json.load(file)

    # Create embedding for question
    query_embedding = create_embeddings(
        [query]
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    # Don't request more results than available
    top_k = min(
        top_k,
        index.ntotal
    )

    # Search FAISS
    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, index_number in zip(
        distances[0],
        indices[0]
    ):

        if index_number == -1:
            continue

        chunk = chunks[index_number]

        results.append({
            "text": chunk["text"],
            "page_number": chunk["page_number"],
            "chunk_number": chunk["chunk_number"],
            "distance": float(distance)
        })

    return results