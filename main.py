# Standard Python libraries for system operations and command line arguments
import sys  # Access to command line arguments (sys.argv) and exit functionality
import os   # Operating system interface for environment variables and file paths

# Google Gemini AI libraries
from google import genai           # Main Gemini AI client for making API calls
from google.genai import types     # Type definitions for API requests/responses

# Third-party library for loading environment variables from .env files
from dotenv import load_dotenv

# Our custom modules
from prompts import system_prompt                           # The instructions we give to the AI
from call_function import call_function, available_functions # Function calling system


def main():
    """
    Entry point of the application. This function:
    1. Loads environment variables (like API keys)
    2. Parses command line arguments 
    3. Sets up the AI client
    4. Starts the conversation with the AI
    """
    
    # Load environment variables from .env file (if it exists)
    # This allows us to store sensitive info like API keys safely
    load_dotenv()

    # Check if user wants detailed output by looking for --verbose flag
    # "in" operator checks if "--verbose" exists anywhere in the command line arguments
    verbose = "--verbose" in sys.argv
    
    # Extract actual command arguments, filtering out any flags that start with "--"
    # sys.argv[1:] gets all arguments except the script name (which is sys.argv[0])
    # List comprehension filters out anything starting with "--" 
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    # If no arguments provided, show usage instructions and exit
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)  # Exit with error code 1 (indicates failure)

    # Get the Gemini API key from environment variables
    # os.environ.get() safely gets an environment variable, returns None if not found
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Create a Gemini AI client instance using our API key
    # This client will be used to send requests to Google's AI service
    client = genai.Client(api_key=api_key)

    # Join all command line arguments into a single string
    # For example: ["fix", "the", "calculator"] becomes "fix the calculator"
    user_prompt = " ".join(args)

    # If verbose mode is enabled, show what prompt we're sending to the AI
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    # Create the initial conversation history as a list
    # This will track the entire conversation between user, AI, and function calls
    messages = [
        # Create a user message containing the user's request
        types.Content(
            role="user",  # This message is from the user
            parts=[types.Part(text=user_prompt)]  # The actual text content
        ),
    ]

    # Start the main AI conversation loop
    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    """
    The main AI agent loop. This function implements the core logic:
    1. Send the conversation to the AI
    2. Check if AI wants to call functions
    3. Execute any function calls
    4. Add results back to conversation
    5. Repeat until AI is done or we hit iteration limit
    
    Args:
        client: The Gemini AI client for making API calls
        messages: List of conversation messages (user, assistant, tool responses)
        verbose: Boolean flag for detailed output
    """
    
    # Safety limit to prevent infinite loops
    # If the AI keeps wanting to do more work, we'll stop after 20 iterations
    max_iterations = 20
    
    # The main agent loop - this is where the "autonomous" behavior happens
    for iteration in range(max_iterations):
        
        # Send the current conversation to the AI and get a response
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",  # Specific Gemini model version
            contents=messages,              # The conversation history so far
            config=types.GenerateContentConfig(
                tools=[available_functions],    # Tell AI what functions it can call
                system_instruction=system_prompt # Give AI its instructions/role
            ),
        )
        
        # If verbose mode, show token usage (helpful for monitoring API costs)
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        
        # Check if the AI wants to call any functions
        # If not, it means the AI thinks it's done with the task
        if not response.function_calls:
            # No function calls means the AI is finished
            print("Final response:")
            print(response.text)  # Print the AI's final answer
            return response.text
        
        # Add the AI's response (containing function calls) to our conversation history
        # This is important for the AI to remember what it just decided to do
        if response.candidates:
            # response.candidates[0] is the primary response from the AI
            messages.append(response.candidates[0].content)
        
        # The AI wants to call one or more functions - let's execute them
        # We collect all the results before adding them to the conversation
        function_response_parts = []
        
        # Loop through each function the AI wants to call
        for function_call_part in response.function_calls:
            # Actually execute the function call using our call_function system
            function_call_result = call_function(function_call_part, verbose)
            
            # Safety check: make sure we got a valid result back
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            
            # If verbose mode, show what the function returned
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
            # Collect this function's result to add to conversation later
            function_response_parts.append(function_call_result.parts[0])
        
        # Add all function results as a single "tool" message in the conversation
        # This is important: the AI needs to see the results to decide what to do next
        if function_response_parts:
            tool_response = types.Content(
                role="tool",  # This indicates the message contains function results
                parts=function_response_parts  # All the function results
            )
            messages.append(tool_response)
        
        # Continue the loop - the AI will see the function results and decide what to do next
        # This might be: call more functions, analyze results, or give a final answer
    
    # If we get here, we've hit the iteration limit
    # This is a safety measure to prevent infinite loops
    print("Max iterations reached. Final response:")
    print(response.text)
    return response.text


if __name__ == "__main__":
    main()