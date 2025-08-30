
from embeddings import get_embedding
from searcher import CombinedSearcher

searcher = CombinedSearcher()

def search(query):
    """Find most similar code snippets to query"""
    return searcher.search(query, limit=5)
