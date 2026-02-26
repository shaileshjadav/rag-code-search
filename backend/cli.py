import os
import argparse


LSIF_FILE = "lsif.json"

import backend.index.files_to_json as files_to_json
import backend.index.convert_lsif_index as convert_lsif_index
import backend.index.generate_signatures as generate_signatures
from backend.helper.upload_code import encode_and_upload
from backend.index.generate_lsif_index import generate_lsif
from backend.helper.upload_signatures import upload_signatures
from backend.config import DATA_DIR


def index_repo(repo_path):
    repo_abs_path = os.path.abspath(repo_path)  # ensure absolute path
    repo_name = os.path.basename(repo_path)
    if not repo_name:
        raise ValueError(f"Repo name could not be determined from path: {repo_path}")
    
    print(f"📂 Indexing repo {repo_name} at {repo_path}")
    files_to_json.main(repo_path)
    generate_lsif(repo_abs_path, 'ts')
    convert_lsif_index.main()
    generate_signatures.main(repo_path)
    encode_and_upload(repo_name)
    upload_signatures(repo_name)

def clean_data_files():
    ## iterate all files in data directory excluding .keep file
    for file in os.listdir(DATA_DIR):
        if file != ".keep":
            # print(f"Removing {file}")
            os.remove(os.path.join(DATA_DIR, file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini LSIF + Embedding Search CLI")
    subparsers = parser.add_subparsers(dest="command")

    index_parser = subparsers.add_parser("index", help="Index a repo")
    index_parser.add_argument("--repo", required=True, help="Path to repo")

    search_parser = subparsers.add_parser("search", help="Search repo")
    search_parser.add_argument("--query", required=True, help="Search query")

    args = parser.parse_args()

    if args.command == "index":
        clean_data_files()
        index_repo(args.repo)
    # elif args.command == "search":
    #     backend.search.search.search(args.query)
