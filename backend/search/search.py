
from backend.helper.embeddings import get_embedding
from backend.search.searcher import CombinedSearcher

searcher = CombinedSearcher()

def search(query):
    """Find most similar code snippets to query"""
    return searcher.search(query, limit=5)
