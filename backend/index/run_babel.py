import subprocess
import json
from pathlib import Path

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

if __name__ == '__main__':
    # Create a dummy JavaScript file for testing
    dummy_js_content = """
function greet(name) {
    console.log(`Hello, ${name}!`);
}

class User {
    constructor(name) {
        this.name = name;
    }
}
    """
    js_file = Path("./test.js")
    js_file.write_text(dummy_js_content)
    
    # Run the parser on the dummy file
    parsed_data = run_babel_parser(js_file)
    
    if parsed_data:
        # Print the results
        for item in parsed_data:
            print(json.dumps(item, indent=2))