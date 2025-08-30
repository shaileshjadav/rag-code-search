import os.path
import os
import json
from pathlib import Path
import subprocess
from config import FOLDER_PATH, DATA_DIR


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


def main():
    # folder_path = os.getenv('QDRANT_PATH')
    output_file = Path(DATA_DIR) / "rs_files.json"

    files_data = explore_directory(FOLDER_PATH)
    
    full_path = os.path.join(FOLDER_PATH)

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(files_data, json_file, indent=2)

# if __name__ == "__main__":
#     main()