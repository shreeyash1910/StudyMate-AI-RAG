from pathlib import Path
import json

import faiss
import numpy as np


VECTOR_STORE_DIR = Path("vector_store")

VECTOR_STORE_DIR.mkdir(
    exist_ok=True
)


def create_faiss_index(
    embeddings,
    chunks,
    document_id
):

    # Convert embeddings to float32
    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    # Get embedding dimensions
    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatL2(
        dimension
    )

    # Add embeddings
    index.add(embeddings)

    # File paths
    index_path = (
        VECTOR_STORE_DIR
        / f"document_{document_id}.index"
    )

    metadata_path = (
        VECTOR_STORE_DIR
        / f"document_{document_id}.json"
    )

    # Save FAISS index
    faiss.write_index(
        index,
        str(index_path)
    )

    # Save chunk metadata
    with open(
        metadata_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=2
        )

    return {
        "index_path": str(index_path),
        "metadata_path": str(metadata_path),
        "total_vectors": index.ntotal,
        "dimension": dimension
    }