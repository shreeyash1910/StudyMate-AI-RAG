from app.services.embedding_service import create_embeddings


texts = [
    "Machine learning is a branch of artificial intelligence.",
    "Deep learning uses neural networks.",
    "SQL is used to manage relational databases."
]


embeddings = create_embeddings(texts)


print("Number of texts:", len(texts))
print("Embedding shape:", embeddings.shape)
print("First embedding:")
print(embeddings[0])