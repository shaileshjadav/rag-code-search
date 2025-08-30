import json
from typing import List

from config import QDRANT_CODE_COLLECTION_NAME, QDRANT_URL
from embeddings import get_embedding
import qdrant_client

class CodeSearcher:
    
    def __init__(self):
        self.collection_name = QDRANT_CODE_COLLECTION_NAME
        self.client = qdrant_client.QdrantClient(
        url= QDRANT_URL
    )

    def search(self, query, limit=5) -> List[dict]:
        print(self, query)
        vector = get_embedding(query, query)
        result = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=limit,
            with_payload=["start_line", "end_line", "file", "text"]
        )

        return [hit.payload for hit in result]


class CombinedSearcher:

    def __init__(self):
        self.code_searcher = CodeSearcher()

    def search(self, query, limit=5, code_limit=20) -> List[dict]:
        code_res = self.code_searcher.search(query, limit=code_limit)
        return code_res


if __name__ == '__main__':
    query = "Router.handle method, where is it defined?"

    searcher = CombinedSearcher()

    res = searcher.search(query)
    for hit in res:
        print(json.dumps(hit))
