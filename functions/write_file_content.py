# Standard library for operating system operations (file/directory handling)
import os
# Google AI types for function schemas
from google.genai import types


def write_file(working_directory, file_path, content):
    """
    Creates or overwrites a file with the specified content, with security constraints.
    This is like redirecting output to a file: echo "content" > file.txt
    
    Args:
        working_directory: The base directory we're allowed to work in (injected for security)
        file_path: Path to the file to create/overwrite (relative to working_directory)
        content: The text content to write to the file
    
    Returns:
        A success message with character count, or an error message
        
    Security Notes:
        - Only writes files within the working directory
        - Creates parent directories automatically if needed
        - Overwrites existing files (be careful!)
        - Won't overwrite directories
    """
    
    # Convert working directory to absolute path for security checks
    abs_working_dir = os.path.abspath(working_directory)
    
    # Build the full path to the file we want to create/write
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # SECURITY CHECK: Make sure the file is inside our allowed working directory
    # This prevents attacks like file_path="../../../etc/passwd" that try to overwrite system files
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # If the file doesn't exist, we might need to create parent directories first
    # For example, if file_path is "subdir/newfile.txt" and "subdir" doesn't exist
    if not os.path.exists(abs_file_path):
        try:
            # os.path.dirname() gets the directory part of the path
            # os.makedirs() creates all necessary parent directories
            # exist_ok=True means "don't error if the directory already exists"
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    
    # Safety check: make sure we're not trying to overwrite a directory with a file
    # This would be confusing and potentially destructive
    if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'
    
    # Try to write the file (wrapped in try/except for error handling)
    try:
        # Open the file in write mode ("w")
        # This will create the file if it doesn't exist, or overwrite it if it does
        # The 'with' statement ensures the file is properly closed even if an error occurs
        with open(abs_file_path, "w") as f:
            # Write the content to the file
            # Python will handle converting the string to bytes with UTF-8 encoding
            f.write(content)
        
        # Return a success message with some useful information
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
        
    except Exception as e:
        # Handle various errors that might occur:
        # - PermissionError: No permission to write to the file/directory
        # - OSError: Disk full, invalid filename, etc.
        # - UnicodeEncodeError: Content contains characters that can't be encoded
        return f"Error: writing to file: {e}"


# Schema that tells the AI how to use this function
schema_write_file = types.FunctionDeclaration(
    name="write_file",  # Function name the AI will use
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,  # Parameters passed as an object
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,  # file_path must be a string
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,  # content must be a string
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],  # Both parameters are required
    ),
)
