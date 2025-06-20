# Gagent - AI Coding Agent

An autonomous AI agent that can analyze code, fix bugs, and implement features using Google's Gemini 2.0 Flash model.

**⚠️ IMPORTANT: This agent only works within the `./calculator` directory. It cannot access or modify files outside this sandbox for security reasons.**

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API key:**
   ```bash
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

3. **Run the agent:**
   ```bash
   python main.py "your request here"
   ```

## Usage Examples

**Note: All commands work only on files within the `./calculator` directory.**

### Basic Operations
```bash
# List files in the calculator directory
python main.py "what files are in the calculator?"

# Read a specific file (from calculator directory)
python main.py "show me the contents of main.py"

# Run Python scripts (in calculator directory)
python main.py "execute the calculator tests"

# Create new files (in calculator directory)
python main.py "create a hello world script"
```

### Advanced Tasks
```bash
# Fix bugs
python main.py "fix the bug where 3 + 7 * 2 gives wrong result"

# Add features
python main.py "add support for parentheses to the calculator"

# Refactor code
python main.py "refactor the calculator using better design patterns"

# Debug mode (see detailed function calls)
python main.py "analyze the calculator code" --verbose
```

### Complex Multi-Step Tasks
```bash
# Comprehensive analysis and improvement
python main.py "analyze the calculator, find bugs, add new features, and test everything"

# Code review and enhancement
python main.py "review the codebase and implement best practices"
```

## How It Works

The agent works by:
1. Analyzing your natural language request
2. Making a plan using available functions
3. Executing functions step-by-step (up to 20 iterations)
4. Learning from results and adapting its approach
5. Providing a final summary of what was accomplished

Available functions:
- **get_files_info**: List directory contents
- **get_file_content**: Read file contents  
- **run_python_file**: Execute Python scripts
- **write_file**: Create or modify files

**All operations are strictly sandboxed to the `./calculator` directory for safety. The agent cannot:**
- Access files outside the calculator directory
- Modify system files or configurations  
- Install packages or run system commands
- Access the internet or external services

This is designed as a learning/demo environment for the calculator project only.

## What Can The Agent Actually Do?

The agent works exclusively with a simple calculator application in the `./calculator` directory. It can:

### ✅ **Working With The Calculator Project**
- **Analyze** the calculator's Python code (main.py, tests.py, etc.)
- **Fix bugs** in the calculator logic or implementation
- **Add features** like new mathematical operations or input validation
- **Refactor code** to use better design patterns
- **Run tests** and interpret results
- **Create documentation** or additional Python files
- **Improve error handling** and user experience

### ❌ **What It Cannot Do**
- Work on real-world projects outside the calculator directory
- Install Python packages or dependencies
- Access databases, APIs, or network resources  
- Modify system configurations or environment settings
- Work with version control (git) or deployment tools
- Access your actual development projects

### 🎯 **Best Use Cases**
- **Learning AI agent architecture** and function calling patterns
- **Experimenting with autonomous debugging** on a simple codebase
- **Understanding LLM-based code analysis** and generation
- **Testing AI agent capabilities** in a safe, controlled environment
- **Educational purposes** for studying AI-assisted development

---

# Documentation

## System Architecture

### Agent Loop Flow
```
User Request → LLM Analysis → Function Plan → Execute Functions → Update Context → Repeat → Final Result
```

### Detailed Flow Diagram
```
┌─────────────────┐
│   User Input    │
│  Natural Lang.  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Gemini 2.0     │
│  Analysis       │
│  & Planning     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐     ┌─────────────────┐
│ Function Calls  │────▶│ Tool Execution  │
│ (1-10 per turn) │     │ (Sandboxed)     │
└─────────┬───────┘     └─────────┬───────┘
          │                       │
          ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│ Conversation    │◀────│ Function        │
│ History Update  │     │ Results         │
└─────────┬───────┘     └─────────────────┘
          │
          ▼
┌─────────────────┐
│ Iteration Check │
│ (Max 20 loops)  │
└─────────┬───────┘
          │
          ▼ (if continue)
     [Back to LLM]
          │
          ▼ (if done)
┌─────────────────┐
│  Final Response │
│  & Summary      │
└─────────────────┘
```

## Core Files

### main.py
**Purpose**: Entry point and agent orchestration

**Key Functions**:
- `main()`: CLI argument parsing and initialization
  - `verbose`: Boolean flag for detailed output
  - `args`: Cleaned command line arguments (removes --flags)
  - `user_prompt`: Joined user input string
  - `api_key`: Gemini API key from environment
  - `client`: Gemini API client instance
  - `messages`: Conversation history list

- `generate_content(client, messages, verbose)`: Core agent loop
  - `max_iterations`: 20-iteration limit to prevent infinite loops
  - `response`: Gemini API response object
  - `function_response_parts`: Collected function call results
  - `tool_response`: Properly formatted function response message

**Variables**:
- `iteration`: Current loop iteration (0-19)
- `function_call_part`: Individual function call from LLM
- `function_call_result`: Result from executing a function

### call_function.py
**Purpose**: Function calling system and available tool definitions

**Key Components**:
- `available_functions`: Tool configuration object containing all function schemas
- `call_function(function_call_part, verbose)`: Executes function calls from LLM

**Function Schemas** (using `types.FunctionDeclaration`):
- `schema_get_files_info`: Directory listing with file metadata
- `schema_get_file_content`: File reading with size limits
- `schema_run_python_file`: Python script execution with timeout
- `schema_write_file`: File creation/modification

**Variables in call_function()**:
- `function_name`: String name of function to call
- `args`: Dictionary of function arguments from LLM
- `function_map`: Dictionary mapping function names to implementations
- `function_result`: Return value from executed function

### functions/ Directory

#### functions/get_files_info.py
**Purpose**: Directory exploration and file metadata

**Function**: `get_files_info(working_directory, directory=None)`
- `abs_working_dir`: Absolute path to working directory
- `target_dir`: Directory to list (working dir if directory=None)
- `files_info`: List of formatted file information strings
- `filepath`: Full path to each file
- `file_size`: Size in bytes
- `is_dir`: Boolean indicating if item is directory

**Security**: Path traversal protection via `startswith()` check

#### functions/get_file_content.py
**Purpose**: File reading with content limits

**Function**: `get_file_content(working_directory, file_path)`
- `abs_working_dir`: Absolute working directory path
- `abs_file_path`: Absolute path to target file
- `MAX_CHARS`: Character limit constant (10,000)
- `content`: File content string (possibly truncated)

**Security**: Path validation and file existence checks

#### functions/run_python.py
**Purpose**: Python script execution with output capture

**Function**: `run_python_file(working_directory, file_path, args=None)`
- `abs_working_dir`: Absolute working directory
- `abs_file_path`: Absolute path to Python file
- `commands`: List containing python executable and file path
- `result`: subprocess.run() result object
- `output`: List of formatted output strings

**Security**: 
- File extension validation (.py only)
- 30-second timeout
- Working directory constraint

**Output Capture**:
- `result.stdout`: Standard output
- `result.stderr`: Error output  
- `result.returncode`: Exit code

#### functions/write_file_content.py
**Purpose**: File creation and modification

**Function**: `write_file(working_directory, file_path, content)`
- `abs_working_dir`: Absolute working directory
- `abs_file_path`: Absolute target file path
- `content`: String content to write

**Features**:
- Automatic directory creation with `makedirs(exist_ok=True)`
- Directory vs file conflict detection
- Character count reporting

### config.py
**Purpose**: System configuration constants

**Constants**:
- `MAX_CHARS = 10000`: File reading limit
- `WORKING_DIR = "./calculator"`: Sandboxed execution directory

### prompts.py
**Purpose**: LLM system instructions

**Variable**:
- `system_prompt`: String containing instructions for the LLM on:
  - Available operations
  - Security model (relative paths)
  - Function calling methodology

## Security Model

### Sandboxing
- All file operations constrained to `WORKING_DIR`
- Path traversal prevention via absolute path validation
- No access to parent directories or system files

### Input Validation
- File path sanitization
- Python file extension validation
- Token and expression validation

### Execution Limits
- 30-second timeout for script execution
- 10,000 character limit for file reading
- 20-iteration limit for agent loops

## Error Handling

### Function Level
- Each tool function handles its own errors gracefully
- Structured error responses using `types.Content`
- Specific error messages for different failure modes

### Agent Level  
- Loop protection prevents infinite execution
- Function call/response synchronization
- Graceful degradation on API errors

### API Level
- Proper conversation history management
- Function call batch processing
- Response validation and error recovery