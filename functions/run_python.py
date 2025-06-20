# Standard library for operating system operations
import os
# Standard library for running external programs (like Python scripts)
import subprocess
# Google AI types for function schemas
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    """
    Executes a Python script and captures its output, with security constraints.
    This is like running 'python script.py' from the command line.
    
    Args:
        working_directory: The base directory we're allowed to work in (injected for security)
        file_path: Path to the Python file to execute (relative to working_directory)
        args: Optional list of command-line arguments to pass to the script
    
    Returns:
        A string containing the script's output (stdout/stderr) and exit status
        
    Security Notes:
        - Only executes files within the working directory
        - Only executes .py files (prevents running arbitrary executables)
        - 30-second timeout prevents infinite loops or long-running scripts
        - Runs in a subprocess (isolated from our main program)
    """
    
    # Convert working directory to absolute path for security checks
    abs_working_dir = os.path.abspath(working_directory)
    
    # Build the full path to the Python file we want to execute
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # SECURITY CHECK: Make sure the file is inside our allowed working directory
    # This prevents attacks like file_path="../../../usr/bin/rm" that try to run system commands
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Check if the file actually exists
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    # SECURITY CHECK: Only allow Python files to be executed
    # This prevents execution of arbitrary executables, shell scripts, etc.
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    # Try to execute the Python file (wrapped in try/except for error handling)
    try:
        # Build the command to run: ["python", "/path/to/script.py", "arg1", "arg2", ...]
        commands = ["python", abs_file_path]
        
        # Add any command-line arguments the AI wants to pass to the script
        if args:
            commands.extend(args)  # extend() adds all items from the args list
        
        # Execute the command using subprocess.run()
        result = subprocess.run(
            commands,                    # The command to run
            capture_output=True,         # Capture both stdout and stderr
            text=True,                   # Return output as strings (not bytes)
            timeout=30,                  # Kill the process after 30 seconds (prevents hangs)
            cwd=abs_working_dir,        # Run the command from the working directory
        )
        
        # Collect the output from the script
        output = []
        
        # If the script printed anything to stdout (normal output), include it
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        
        # If the script printed anything to stderr (error output), include it
        # Note: Some programs print normal output to stderr, so this isn't always an error
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        # If the script exited with a non-zero code, it usually means an error occurred
        # Exit code 0 = success, anything else = some kind of error
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        # Join all the output parts together, or return a default message if no output
        return "\n".join(output) if output else "No output produced."
        
    except Exception as e:
        # Handle various errors that might occur:
        # - subprocess.TimeoutExpired: Script ran longer than 30 seconds
        # - FileNotFoundError: Python interpreter not found
        # - PermissionError: No permission to execute the file
        # - Other subprocess errors
        return f"Error: executing Python file: {e}"


# Schema that tells the AI how to use this function
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",  # Function name the AI will use
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,  # Parameters passed as an object
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,  # file_path must be a string
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,  # args is a list/array
                items=types.Schema(
                    type=types.Type.STRING,  # Each item in the array should be a string
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],  # file_path is required, args is optional
    ),
)
