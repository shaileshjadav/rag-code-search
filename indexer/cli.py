import os
import json
import argparse
import requests

LSIF_FILE = "lsif.json"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/embeddings"
import files_to_json
import convert_lsif_index
import generate_signatures
import embeddings
from upload_code import encode_and_upload
import search
from generate_lsif_index import generate_lsif
from config import FOLDER_PATH

# def embed_text(text):
#     if not OPENROUTER_API_KEY:
#         print("❌ Missing OPENROUTER_API_KEY env variable")
#         return None

#     client = genai.Client(api_key=OPENROUTER_API_KEY)

#     try:
#         response = client.models.embed_content(
#             model='text-embedding-004',
#             contents=text,
#         )
#         return response.embeddings[0].values
#     except Exception as e:
#         print("❌ Embedding request failed:", e)
#         return None


def chunk_code(content, chunk_size=300, overlap=50):
    """
    Splits code into overlapping chunks for better semantic search.
    """
    chunks = []
    start = 0
    while start < len(content):
        end = min(len(content), start + chunk_size)
        chunks.append(content[start:end])
        start += chunk_size - overlap  # slide window
    return chunks

def index_repo(repo_path):
    repo_path = os.path.abspath(repo_path)  # ensure absolute path
    print(f"📂 Indexing repo at {repo_path}")
    # TODO: as future scope
    # files_to_json.main()
    generate_lsif(repo_path, 'js')
    convert_lsif_index.main()
    # generate_signatures.main()
    # encode_and_upload()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini LSIF + Embedding Search CLI")
    subparsers = parser.add_subparsers(dest="command")

    index_parser = subparsers.add_parser("index", help="Index a repo")
    index_parser.add_argument("--repo", required=True, help="Path to repo")

    search_parser = subparsers.add_parser("search", help="Search repo")
    search_parser.add_argument("--query", required=True, help="Search query")

    args = parser.parse_args()

    if args.command == "index":
        index_repo(args.repo)
    elif args.command == "search":
        search.search(args.query)
