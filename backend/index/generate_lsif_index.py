import subprocess
import sys
import os
import shutil
from pathlib import Path
from backend.config import DATA_DIR, FOLDER_PATH

LANGUAGE_SERVERS = {
    # "rs": "rust-analyzer",      # Rust
    # "py": "pyright",            # Python
    "ts": "tsserver",           # TypeScript
    "js": "jsserver",           # JavaScript
}

def get_language_server(language: str) -> str | None:
    return LANGUAGE_SERVERS.get(language)

def generate_lsif(repo_path: str, language: str):
    lang_server = get_language_server(language)
    if not lang_server:
        raise ValueError(f"No LSIF indexer found for {language}")
    
    # Correct command structure for lsif-tsc
    if lang_server == "jsserver":
        # For JavaScript files, we need to use shell=True for glob patterns
        cmd = "lsif-tsc **/*.js --allowJs --checkJs"
    elif lang_server == "tsserver":
        # For TypeScript projects with tsconfig.json
        cmd = ["lsif-tsc", "-p", "."]
    else:
        raise NotImplementedError(f"LSIF for {lang_server} not implemented yet")
    
    print(f"Running: {cmd if isinstance(cmd, str) else ' '.join(cmd)} for {repo_path}")
    
    # Run the LSIF indexer
    try:
        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, shell=True, check=True)
        print(f"Command completed successfully")
        print(f"STDOUT: {result.stdout}")
        if result.stderr:
            print(f"STDERR: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        raise
    
    # Copy the generated LSIF file to the expected location
    source_lsif = Path(repo_path) / "dump.lsif"
    target_lsif = Path(DATA_DIR) / "dump.lsif"
    
    # Ensure DATA_DIR exists
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    
    if source_lsif.exists():
        shutil.copy2(source_lsif, target_lsif)
        print(f"Copied LSIF file from {source_lsif} to {target_lsif}")
    else:
        print(f"Warning: LSIF file not found at {source_lsif}")
    
    return result.stdout, result.stderr

if __name__ == '__main__':
    # --- How to use the function ---
    # Define the directory where your TypeScript project is located.
    # Replace this path with the actual path to your project.
    # Check if the directory exists before attempting to run the command.
    if not os.path.isdir(FOLDER_PATH):
        print(f"Error: Directory not found at '{FOLDER_PATH}'")
        sys.exit(1)

    try:
        # Call the function with the target directory
        stdout, stderr = generate_lsif(FOLDER_PATH, 'js')

        # Print the results from the function call
        print("\n--- Command Output (STDOUT) ---")
        print(stdout)
        
        if stderr:
            print("\n--- Command Error (STDERR) ---")
            print(stderr)
        
        print("\nIndexer ran successfully.")

    except Exception as e:
        # This will catch any exceptions raised by the function
        print(f"An error occurred: {e}")
        sys.exit(1)
