import numpy as np
from embeddings import get_embedding

def search(query, vectors, metadata, top_k=5):
    """Find most similar code snippets to query"""
    query_emb = np.array(get_embedding(query))
    scores = np.dot(vectors, query_emb) / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(query_emb))
    top_idx = np.argsort(scores)[::-1][:top_k]
    results = [(metadata[i], float(scores[i])) for i in top_idx]
    return results
