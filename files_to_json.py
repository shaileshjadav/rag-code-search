import os.path
import os
import json
from pathlib import Path
import subprocess

LANGUAGE_SERVERS = {
    "rs": "rust-analyzer",      # Rust
    "py": "pyright",            # Python
    "ts": "tsserver",           # TypeScript
    "js": "jsserver",           # JavaScript
    "c": "clangd",              # C
    "cpp": "clangd",            # C++
    "php": "intelephense",      # PHP
}

def get_language_server(language: str) -> str | None:
    # _, ext = os.path.splitext(file_path)
    return LANGUAGE_SERVERS.get(language)

def generate_lsif(repo_path: str, language: str):
    lang_server = get_language_server(language)
    if not lang_server:
        raise ValueError(f"No LSIF indexer found for {file_path}")

    # Example commands (different for each analyzer!)
    if lang_server == "jsserver":
        cmd = ["scip-typescript index", repo_path, "--infer-tsconfig"]
    elif lang_server == "tsserver":
        cmd = ["scip-typescript index", repo_path]
    else:
        raise NotImplementedError(f"LSIF for {lang_server} not implemented yet")

    print(f"Running: {' '.join(cmd)}")
    return subprocess.Popen(cmd, shell=True, cwd=repo_path)

def process_file(root_dir, file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        code_lines = file.readlines()
        relative_path = os.path.relpath(file_path, root_dir)
        return {
            "path": relative_path,
            "code": code_lines,
            "startline": 1,
            "endline": len(code_lines)
        }


def explore_directory(root_dir):
    result = []
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            if file_path.endswith((".py", ".js", ".ts", ".java", ".go", ".php", ".cpp", ".c")):
                print(f"Processing file: {file_path}")
                result.append(process_file(root_dir, file_path)) 
    return result


def main(DATA_DIR):
    # folder_path = os.getenv('QDRANT_PATH')
    output_file = Path(DATA_DIR) / "rs_files.json"

    files_data = explore_directory(DATA_DIR)
    
    full_path = os.path.join(DATA_DIR)

    language_server = generate_lsif(DATA_DIR, 'js')   

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(files_data, json_file, indent=2)

# if __name__ == "__main__":
#     main()