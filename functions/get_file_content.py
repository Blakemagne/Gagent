# Standard library for operating system operations (file handling)
import os
# Google AI types for creating function schemas
from google.genai import types
# Our configuration settings (like maximum file size to read)
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    """
    Reads the contents of a text file, with size limits and security constraints.
    This is like the 'cat' command on Unix or 'type' command on Windows.
    
    Args:
        working_directory: The base directory we're allowed to work in (injected for security)
        file_path: Path to the file to read (relative to working_directory)
    
    Returns:
        The file contents as a string, possibly truncated if too large
        
    Security Notes:
        - Only reads files within the working directory (prevents path traversal)
        - Limits file size to prevent memory/API token issues
        - Only reads text files (binary files might cause encoding errors)
    """
    
    # Convert the working directory to an absolute path for security checks
    # Example: "./calculator" becomes "/home/user/project/calculator"
    abs_working_dir = os.path.abspath(working_directory)
    
    # Build the full path to the file we want to read
    # os.path.join() handles path separators correctly across operating systems
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # SECURITY CHECK: Make sure the file is inside our allowed working directory
    # This prevents attacks like file_path="../../../etc/passwd" that try to read system files
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Check if the file actually exists and is a regular file (not a directory or special file)
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # Try to read the file (wrapped in try/except for error handling)
    try:
        # Open the file in read mode with UTF-8 encoding (standard for text files)
        # The 'with' statement ensures the file is properly closed even if an error occurs
        with open(abs_file_path, "r") as f:
            # Read up to MAX_CHARS characters from the file
            # f.read(MAX_CHARS) reads at most MAX_CHARS characters, not the whole file
            # This prevents memory issues with huge files and API token limits
            content = f.read(MAX_CHARS)
            
            # If we read exactly MAX_CHARS, the file was probably larger
            # Add a note to let the user know the file was truncated
            if len(content) == MAX_CHARS:
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        
        # Return the file contents (possibly with truncation notice)
        return content
        
    except Exception as e:
        # Handle various errors that might occur:
        # - Permission denied
        # - File encoding issues (trying to read binary files as text)
        # - Disk I/O errors
        # - Out of memory (for very large files)
        return f'Error reading file "{file_path}": {e}'


# Schema that tells the AI how to use this function
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",  # Function name the AI will use
    # Description includes the character limit so the AI knows about truncation
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,  # Parameters passed as an object
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,  # file_path must be a string
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],  # file_path is required (AI must provide it)
    ),
)
