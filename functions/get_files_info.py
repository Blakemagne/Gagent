# Standard library for operating system operations (file/directory handling)
import os
# Google AI types for creating function schemas that the AI can understand
from google.genai import types


def get_files_info(working_directory, directory=None):
    """
    Lists all files and directories in a specified folder, with security constraints.
    This is like the 'ls' command on Unix or 'dir' command on Windows.
    
    Args:
        working_directory: The base directory we're allowed to work in (injected for security)
        directory: Optional subdirectory to list (relative to working_directory)
    
    Returns:
        A string with formatted information about each file/directory
        
    Security Note:
        This function prevents "path traversal attacks" where someone tries to access
        files outside the working directory using paths like "../../../etc/passwd"
    """
    
    # Get the absolute path of our working directory
    # os.path.abspath() converts relative paths like "./calculator" to full paths like "/home/user/project/calculator"
    abs_working_dir = os.path.abspath(working_directory)
    
    # Start with the working directory as our target
    target_dir = abs_working_dir
    
    # If a specific subdirectory was requested, calculate its path
    if directory:
        # os.path.join() safely combines paths (handles / vs \ on different operating systems)
        # Then get the absolute path to the target directory
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    
    # SECURITY CHECK: Make sure the target directory is inside our allowed working directory
    # This prevents attacks like directory="../../../etc" that try to escape the sandbox
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Check if the target is actually a directory (not a file)
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    # Try to list the files (wrapped in try/except for error handling)
    try:
        # List to collect information about each file
        files_info = []
        
        # os.listdir() returns a list of all items in the directory
        for filename in os.listdir(target_dir):
            # Build the full path to this file/directory
            filepath = os.path.join(target_dir, filename)
            
            # Initialize file size (we'll set this properly below)
            file_size = 0
            
            # Check if this item is a directory or a file
            is_dir = os.path.isdir(filepath)
            
            # Get the size of the file/directory in bytes
            # For directories, this is usually 4096 bytes (the size of the directory entry)
            file_size = os.path.getsize(filepath)
            
            # Format the information in a human-readable way
            # Example output: "- script.py: file_size=1234 bytes, is_dir=False"
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        
        # Join all the file information with newlines to create a readable list
        return "\n".join(files_info)
        
    except Exception as e:
        # If anything goes wrong (permissions, disk errors, etc.), return an error message
        return f"Error listing files: {e}"


# This is the "schema" - it tells the AI how to use this function
# Think of it as the function's "instruction manual" for the AI
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",  # The name the AI will use to call this function
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,  # Parameters are passed as an object (dictionary)
        properties={
            # Define each parameter the AI can pass to this function
            "directory": types.Schema(
                type=types.Type.STRING,  # This parameter should be a string
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
        # Note: "directory" is not in "required" list, so it's optional
        # If the AI doesn't provide it, the function lists the working directory
    ),
)
