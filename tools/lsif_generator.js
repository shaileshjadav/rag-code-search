#!/usr/bin/env node

// Import the necessary modules
const { exec } = require('child_process');
const path = require('path');

/**
 * Parses command-line arguments to get the target directory.
 * Prints a usage message if the argument is missing.
 * @returns {{targetDir: string | null}}
 */
function parseArguments() {
  const args = process.argv.slice(2); // Get arguments after 'node' and script path
  const targetDir = args[0];

  if (!targetDir) {
    console.error('Error: Target directory must be provided.');
    console.log('\nUsage:');
    console.log('  node cli_script.js <target_directory>');
    console.log('\nExample:');
    console.log('  node cli_script.js ./my-project');
    return { targetDir: null };
  }

  return { targetDir };
}

/**
 * Runs a platform-specific command in a specified directory and logs the output.
 * @param {string} targetDirectory The directory to run the command in.
 */
function runCommandInDir(targetDirectory) {
  // Use a platform-specific command for listing directory contents
  const command = process.platform === 'win32' ? 'dir' : 'ls -a';

  // Determine the correct shell based on the operating system
  const shell = process.platform === 'win32' ? 'cmd.exe' : '/bin/sh';

  console.log(`Executing command '${command}' in directory: ${targetDirectory}`);

  // Use exec to run the command, explicitly setting the shell to avoid ENOENT errors
  exec(command, { cwd: targetDirectory, shell: shell }, (error, stdout, stderr) => {
    if (error) {
      // The ENOENT error occurs here if the shell is not found
      console.error(`Error executing command: ${error.message}`);
      // A more detailed explanation for ENOENT to help the user
      if (error.code === 'ENOENT') {
        console.error(`\nPossible cause: The specified shell '${shell}' was not found. Please ensure it is installed and in your system's PATH.`);
      }
      return;
    }
    if (stderr) {
      console.error(`Command stderr: ${stderr}`);
      return;
    }

    console.log(`\nCommand stdout:\n${stdout}`);
  });
}

// Main execution logic
const { targetDir } = parseArguments();
if (targetDir) {
  runCommandInDir(targetDir);
}
