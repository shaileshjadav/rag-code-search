import os
import argparse


LSIF_FILE = "lsif.json"

import backend.index.files_to_json as files_to_json
import backend.index.convert_lsif_index as convert_lsif_index
import backend.index.generate_signatures as generate_signatures
from backend.helper.upload_code import encode_and_upload
from backend.index.generate_lsif_index import generate_lsif
from backend.config import FOLDER_PATH
from backend.helper.upload_signatures import upload_signatures


def index_repo(repo_path):
    repo_path = os.path.abspath(repo_path)  # ensure absolute path
    print(f"📂 Indexing repo at {repo_path}")
    files_to_json.main()
    generate_lsif(repo_path, 'js')
    convert_lsif_index.main()
    generate_signatures.main()
    encode_and_upload()
    upload_signatures()



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
    # elif args.command == "search":
    #     backend.search.search.search(args.query)
