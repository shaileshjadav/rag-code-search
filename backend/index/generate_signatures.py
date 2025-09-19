import os.path
import os
import json
from pathlib import Path
import subprocess
from backend.config import FOLDER_PATH, DATA_DIR, SUPPORTED_LANGUAGES


def run_babel_parser(js_file_path: Path):
    """
    Runs the babel_parser.js script on a given JavaScript file
    and returns a list of dictionaries.
    """
    # Define the command to run
    # Ensure 'node' is in your system's PATH
    # Ensure the babel_parser.js file is in the same directory
    cmd = ["node", "backend/tools/babel_parser.js", str(js_file_path)]
    
    try:
        # Run the subprocess and capture the standard output
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # The output is a JSON string, so we parse it
        parsed_output = json.loads(result.stdout)
        return parsed_output
    
    except subprocess.CalledProcessError as e:
        print(f"Error executing Node.js script: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Error: Node.js is not installed or not in your PATH.")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON output.")
        print("Node.js Script Output:")
        print(result.stdout)
        return None


def process_file(root_dir, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            code_lines = file.readlines()
            relative_path = os.path.relpath(file_path, root_dir)
            print(f"Processing: {relative_path}")
            parsed_data = run_babel_parser(file_path)
            if parsed_data is None:
                print(f"Warning: Failed to parse {relative_path}")
                return None
            return parsed_data
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def explore_directory(root_dir):
    result = []
    print(f"Exploring directory: {root_dir}")
    print(f"Looking for files with extensions: {SUPPORTED_LANGUAGES}")
    
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            if file_path.endswith(tuple(SUPPORTED_LANGUAGES)):
                parsed_data = process_file(root_dir, file_path)
                if parsed_data is not None:
                    for obj in parsed_data:
                        result.append(obj)
                else:
                    print(f"Skipping {file_path} due to parsing error")
    
    print(f"Total files processed successfully: {len(result)}")
    return result


def main():
    # folder_path = os.getenv('QDRANT_PATH')
    output_file = Path(DATA_DIR) / "signatures.json"

    files_data = explore_directory(FOLDER_PATH)

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(files_data, json_file, indent=2)

if __name__ == "__main__":
    main()