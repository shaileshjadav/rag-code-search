import subprocess
import sys
import os

def run_lsif_indexer(project_directory: str):
    """
    Runs the lsif-tsc command in the specified directory.

    Args:
        project_directory: The absolute or relative path to the directory
                           containing the tsconfig.json file.

    Returns:
        A tuple containing (stdout, stderr) on success, or raises an
        exception on failure.
    """
    # Define the command and its arguments.
    # We use -p . to tell lsif-tsc to use the tsconfig.json in the
    # current working directory, which is set by the 'cwd' argument.
    command = 'lsif-tsc'
    arguments = ['**/*.js', '--AllowJs', '--checkJs']
    absolute_project_directory = os.path.abspath(project_directory)
    print(f"Executing '{command} {' '.join(arguments)}' in directory: {project_directory}")

    try:
        # Run the command with the specified working directory (cwd).
        # This tells the subprocess to "cd" into the project_directory
        # before running the command.
        result = subprocess.run(
            [command] + arguments,
            cwd=project_directory,
            check=True,
            capture_output=True,
            text=True
        )

        # Return the standard output and standard error
        return result.stdout, result.stderr
        
    except FileNotFoundError:
        # Handle the case where the command is not in the system's PATH
        print(f"Error: The command '{command}' was not found. "
              "Make sure it's installed and in your PATH.")
        # Re-raise the exception to be caught by the calling function or main block
        raise
    except subprocess.CalledProcessError as e:
        # Handle the case where the command returns a non-zero exit code
        print(f"Command failed with return code: {e.returncode}")
        print(f"STDOUT:\n{e.stdout}")
        print(f"STDERR:\n{e.stderr}")
        # Re-raise the exception
        raise


if __name__ == '__main__':
    # --- How to use the function ---
    # Define the directory where your TypeScript project is located.
    # Replace this path with the actual path to your project.
    target_project_directory = './express'

    # Check if the directory exists before attempting to run the command.
    if not os.path.isdir(target_project_directory):
        print(f"Error: Directory not found at '{target_project_directory}'")
        sys.exit(1)

    try:
        # Call the function with the target directory
        stdout, stderr = run_lsif_indexer(target_project_directory)

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
