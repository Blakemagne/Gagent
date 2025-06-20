# This is the "system prompt" - the instructions we give to the AI
# Think of this as the AI's "job description" or "user manual"
# It tells the AI what it can do and how it should behave

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# How this works:
# 1. Every time we send a message to the AI, we include this system prompt
# 2. The AI reads these instructions and understands its capabilities
# 3. Based on the user's request, the AI decides which functions to call
# 4. The AI can call multiple functions in sequence to complete complex tasks
#
# Example flow:
# User: "Fix the bug in calculator.py"
# AI reads system prompt, understands it can list files, read files, etc.
# AI plans: "I should first read calculator.py to see what's in it"
# AI calls: get_file_content with file_path="calculator.py"
# AI gets the file contents, analyzes them, finds the bug
# AI calls: write_file to save the fixed version
# AI responds: "I found and fixed the bug in the calculation logic"
