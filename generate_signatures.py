import os.path
import os
import json
from pathlib import Path
import subprocess

def run_babel_parser(js_file_path: Path):
    """
    Runs the babel_parser.js script on a given JavaScript file
    and returns a list of dictionaries.
    """
    # Define the command to run
    # Ensure 'node' is in your system's PATH
    # Ensure the babel_parser.js file is in the same directory
    cmd = ["node", "tools/babel_parser.js", str(js_file_path)]
    
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
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        code_lines = file.readlines()
        relative_path = os.path.relpath(file_path, root_dir)
        parsed_data = run_babel_parser(file_path)
        return parsed_data

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
    output_file = Path(DATA_DIR) / "signatures.json"

    files_data = explore_directory(DATA_DIR)

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(files_data, json_file, indent=2)

# if __name__ == "__main__":
#     main()