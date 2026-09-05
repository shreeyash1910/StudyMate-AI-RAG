from sentence_transformers import SentenceTransformer


_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )

    return _model


def create_embeddings(texts):

    model = get_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False,
        batch_size=1
    )

    return embeddings