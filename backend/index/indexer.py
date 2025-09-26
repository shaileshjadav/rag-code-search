import os

from backend.helper.embeddings import get_embedding

def read_repo_files(repo_path, exts=(".py", ".js", ".ts")):
    """Recursively read repo files with specific extensions"""

    all_files = []
    for root, _, files in os.walk(repo_path):
        for f in files:
            if f.endswith(exts):
                file_path = os.path.join(root, f)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                    code = fp.read()
                    all_files.append((file_path, code))
    return all_files

def build_index(repo_path):
    """Create vector embeddings for repo"""
    files = read_repo_files(repo_path)
    vectors, metadata = [], []
    for fpath, code in files:
        emb = get_embedding(code)
        vectors.append(emb)
        metadata.append(fpath)
    return vectors, metadata
