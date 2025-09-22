import json
from typing import List

from backend.config import QDRANT_URL, ENCODER_NAME
from backend.helper.embeddings import get_embedding
import qdrant_client

from backend.helper.postprocessing import merge_search_results
from backend.helper.upload_code import get_collection_name as get_code_collection_name
from backend.helper.upload_signatures import get_collection_name as get_signatures_collection_name

class CodeSearcher:
    
    def __init__(self):
        self.client = qdrant_client.QdrantClient(
        url= QDRANT_URL
    )

    def search(self, query, projectRepo, limit=5) -> List[dict]:
        print(self, query)
        vector = get_embedding(query, query)
        result = self.client.search(
            collection_name=projectRepo,
            query_vector=vector,
            limit=limit,
            with_payload=["start_line", "end_line", "file", "text", "code_snippet"]
        )

        return [hit.payload for hit in result]


class NluSearcher:

    def __init__(self):
        self.client = qdrant_client.QdrantClient(url= QDRANT_URL)
        

    def search(self, query, projectRepo, limit=5) -> List[dict]:
        vector = get_embedding(query, query)
        result = self.client.search(
            collection_name=projectRepo,
            query_vector=vector,
            limit=limit,
        )

        return [hit.payload for hit in result]


class CombinedSearcher:

    def __init__(self):
        self.code_searcher = CodeSearcher()
        self.nlu_searcher = NluSearcher()

    def search(self, query, projectRepo, limit=5, code_limit=20) -> List[dict]:
        
        code_res = self.code_searcher.search(query, get_code_collection_name(projectRepo), limit=code_limit)
        print(f"Code search results: {code_res} in collection: {get_code_collection_name(projectRepo) }")
        
        nlu_res = self.nlu_searcher.search(query, get_signatures_collection_name(projectRepo), limit=limit)
        # return nlu_res
        return merge_search_results(code_res, nlu_res)


if __name__ == '__main__':
    query = "Router.handle method, where is it defined?"

    searcher = CombinedSearcher()

    res = searcher.search(query)
    for hit in res:
        print(json.dumps(hit))
