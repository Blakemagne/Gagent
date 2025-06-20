import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import call_function, available_functions


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    max_iterations = 20
    
    for iteration in range(max_iterations):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        
        # Check if there are function calls to make
        if not response.function_calls:
            # No function calls, agent is done
            print("Final response:")
            print(response.text)
            return response.text
        
        # Add the assistant's response with function calls to messages
        if response.candidates:
            messages.append(response.candidates[0].content)
        
        # Process function calls and collect all results
        function_response_parts = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
            # Collect the function response part
            function_response_parts.append(function_call_result.parts[0])
        
        # Add all function responses as a single tool message
        if function_response_parts:
            tool_response = types.Content(
                role="tool",
                parts=function_response_parts
            )
            messages.append(tool_response)
        
        # Continue the loop since we made function calls
    
    # If we've reached max iterations
    print("Max iterations reached. Final response:")
    print(response.text)
    return response.text


if __name__ == "__main__":
    main()