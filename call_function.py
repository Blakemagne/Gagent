# Google Gemini types for creating properly formatted API responses
from google.genai import types

# Import all our tool functions and their schemas (function definitions)
# Each function has two parts: the actual Python function, and a schema that tells the AI how to use it
from functions.get_files_info import get_files_info, schema_get_files_info          # List directory contents
from functions.get_file_content import get_file_content, schema_get_file_content    # Read file contents
from functions.run_python import run_python_file, schema_run_python_file           # Execute Python scripts
from functions.write_file_content import write_file, schema_write_file             # Create/modify files

# Import our configuration (like which directory we're allowed to work in)
from config import WORKING_DIR

# This is the master list of all functions the AI can call
# We package them into a Tool object that gets sent to the AI
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,      # AI can list files
        schema_get_file_content,    # AI can read files
        schema_run_python_file,     # AI can run Python scripts
        schema_write_file,          # AI can create/modify files
    ]
)


def call_function(function_call_part, verbose=False):
    """
    This is the bridge between the AI and our actual Python functions.
    When the AI says "I want to call get_files_info", this function:
    1. Figures out which Python function to call
    2. Adds security parameters (like working directory)
    3. Calls the actual function
    4. Formats the result for the AI
    
    Args:
        function_call_part: The AI's request to call a function (includes name and arguments)
        verbose: Whether to print detailed information about what's happening
    
    Returns:
        A properly formatted response that the AI can understand
    """
    
    # Show what function is being called (for user feedback)
    if verbose:
        # In verbose mode, show the function name and all its arguments
        print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        # In normal mode, just show the function name
        print(f" - Calling function: {function_call_part.name}")
    
    # This is our "phone book" - it maps function names to actual Python functions
    # When the AI says "call get_files_info", we look it up here to find the real function
    function_map = {
        "get_files_info": get_files_info,        # Maps to the actual Python function
        "get_file_content": get_file_content,    # Maps to the actual Python function
        "run_python_file": run_python_file,      # Maps to the actual Python function
        "write_file": write_file,                # Maps to the actual Python function
    }
    
    # Get the name of the function the AI wants to call
    function_name = function_call_part.name
    
    # Safety check: make sure this is a function we actually have
    if function_name not in function_map:
        # If the AI tries to call a function we don't have, return an error message
        return types.Content(
            role="tool",  # This is a response from a tool (not user or AI)
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Get the arguments the AI wants to pass to the function
    # dict() converts the AI's arguments into a regular Python dictionary
    args = dict(function_call_part.args)
    
    # SECURITY: Add the working directory to the arguments
    # This ensures all functions operate in our safe sandbox directory
    # The AI doesn't control this - we inject it for security
    args["working_directory"] = WORKING_DIR
    
    # Actually call the Python function with the arguments
    # The ** syntax "unpacks" the dictionary into keyword arguments
    # So {a: 1, b: 2} becomes function_name(a=1, b=2)
    function_result = function_map[function_name](**args)
    
    # Format the result so the AI can understand it
    # We wrap everything in the proper Google AI types
    return types.Content(
        role="tool",  # This is a response from a tool
        parts=[
            types.Part.from_function_response(
                name=function_name,                        # Which function was called
                response={"result": function_result},      # What the function returned
            )
        ],
    )
