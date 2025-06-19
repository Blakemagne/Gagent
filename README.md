# Gagent - AI Coding Agent

## Overview

Gagent is an autonomous AI coding agent built with Google's Gemini 2.0 Flash model that can perform complex software engineering tasks through function calling and iterative problem solving. The agent can analyze codebases, execute code, fix bugs, and interact with files within a sandboxed environment.

## Architecture

### Core Components

#### 1. Agent Loop (`main.py`)
- **Purpose**: Main execution loop that enables autonomous multi-step problem solving
- **Key Features**:
  - Iterative conversation with LLM (max 20 iterations to prevent infinite loops)
  - Function call orchestration and result integration
  - Conversation history management for context preservation
  - Automatic termination when task completion is detected

#### 2. Function Calling System (`call_function.py`)
- **Purpose**: Bridges LLM function calls to actual Python function execution
- **Security**: All operations are constrained to `WORKING_DIR` (`./calculator`)
- **Function Mapping**: Translates function names to actual implementations
- **Error Handling**: Robust error handling with structured responses

#### 3. Tool Functions (`functions/`)
Each tool function follows a consistent pattern with security constraints:

##### `get_files_info.py`
- **Purpose**: Directory listing with file metadata
- **Security**: Path traversal protection, working directory constraints
- **Output**: File sizes, directory flags, formatted listing

##### `get_file_content.py`
- **Purpose**: File reading with content limits
- **Security**: File existence validation, path traversal protection
- **Limits**: `MAX_CHARS` (10,000) character limit with truncation notice

##### `run_python.py`
- **Purpose**: Python script execution with output capture
- **Security**: Working directory constraint, 30-second timeout
- **Features**: STDOUT/STDERR capture, exit code reporting, argument support

##### `write_file_content.py`
- **Purpose**: File creation and modification
- **Security**: Path validation, directory creation as needed
- **Features**: Content length reporting, overwrite protection warnings

#### 4. Configuration (`config.py`)
- `MAX_CHARS`: File content reading limit (10,000 characters)
- `WORKING_DIR`: Sandboxed working directory (`./calculator`)

#### 5. System Prompt (`prompts.py`)
Instructs the LLM on:
- Available operations and their purposes
- Security model (relative paths, automatic working directory injection)
- Function calling methodology

## Function Call Flow

```
User Request → LLM Analysis → Function Call Plan → Tool Execution → Result Integration → Next Iteration
```

### Detailed Flow:
1. **User Input**: Natural language request
2. **LLM Processing**: Gemini analyzes request and determines function calls
3. **Function Routing**: `call_function()` maps function names to implementations
4. **Security Injection**: Working directory automatically added to function arguments
5. **Tool Execution**: Function executes with error handling
6. **Result Integration**: Function results added to conversation history as tool responses
7. **Iteration**: Process repeats until LLM determines task completion

## Security Model

### Sandboxing
- All file operations constrained to `WORKING_DIR` (`./calculator`)
- Path traversal attacks prevented through absolute path validation
- No access to parent directories or system files

### Input Validation
- File path sanitization and validation
- Token validation in expressions
- Error handling for malformed inputs

### Execution Limits
- 30-second timeout for Python script execution
- 10,000 character limit for file reading
- 20-iteration limit for agent loops

## Dependencies

```python
google-genai==1.12.1    # Google Gemini API client
python-dotenv==1.1.0    # Environment variable management
```

## Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## Usage

### Basic Usage
```bash
python main.py "your request here"
```

### Verbose Mode
```bash
python main.py "your request here" --verbose
```

### Example Commands
```bash
# Code analysis
python main.py "explain how the calculator renders results"

# Bug fixing
python main.py "fix the bug: 3 + 7 * 2 should equal 17, not 20"

# Testing
python main.py "run the calculator tests and fix any failures"

# File operations
python main.py "create a hello world script and run it"
```

## Test Environment: Calculator App

The agent operates on a sample calculator application located in `./calculator/`:

### Calculator Structure
```
calculator/
├── main.py              # CLI interface
├── tests.py             # Unit tests (9 test cases)
└── pkg/
    ├── calculator.py    # Core calculator logic with operator precedence
    └── render.py        # ASCII box rendering for results
```

### Calculator Features
- **Expression Evaluation**: Infix notation with proper operator precedence
- **Supported Operations**: Addition (+), Subtraction (-), Multiplication (*), Division (/)
- **Operator Precedence**: Multiplication/Division (2) > Addition/Subtraction (1)
- **Visual Output**: Results displayed in ASCII box format
- **Error Handling**: Invalid token and expression validation

## Agent Capabilities

### Autonomous Debugging
- **Bug Detection**: Analyzes unexpected behavior through testing
- **Root Cause Analysis**: Examines code to identify issues
- **Fix Implementation**: Modifies code to resolve problems
- **Verification**: Tests fixes to ensure correctness

### Code Analysis
- **Structure Understanding**: Navigates and comprehends codebases
- **Function Tracing**: Follows execution flow across modules
- **Documentation Generation**: Explains code functionality

### File Management
- **Content Reading**: Retrieves and analyzes file contents
- **File Creation**: Generates new files with specified content
- **Directory Navigation**: Explores project structure

### Code Execution
- **Script Running**: Executes Python files with argument support
- **Output Capture**: Collects STDOUT, STDERR, and exit codes
- **Test Execution**: Runs test suites and interprets results

## Implementation Details

### Function Declaration Schema
Uses Google GenAI's `types.FunctionDeclaration` for structured function definitions:

```python
schema_example = types.FunctionDeclaration(
    name="function_name",
    description="Clear description of function purpose",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "param_name": types.Schema(
                type=types.Type.STRING,
                description="Parameter description",
            ),
        },
        required=["param_name"],
    ),
)
```

### Message Flow Structure
Conversation history maintains context through structured messages:
- **User Messages**: Original requests
- **Assistant Messages**: LLM responses with function calls
- **Tool Messages**: Function execution results

### Error Handling Strategy
- **Function-Level**: Each tool function handles its own errors gracefully
- **Agent-Level**: Loop protections prevent infinite execution
- **Security-Level**: Path validation prevents unauthorized access

## Extending the Agent

### Adding New Functions
1. Create function implementation in `functions/`
2. Define schema with `types.FunctionDeclaration`
3. Add to `available_functions` in `call_function.py`
4. Update function mapping dictionary
5. Update system prompt with new capability

### Modifying Security Constraints
- Adjust `WORKING_DIR` in `config.py`
- Modify path validation logic in tool functions
- Update timeout and limit constants

### Enhancing the Agent Loop
- Modify iteration limits in `generate_content()`
- Add new termination conditions
- Implement conversation state persistence

## Performance Considerations

### Token Usage
- Conversation history grows with each iteration
- Function results consume input tokens for subsequent calls
- Verbose mode increases token consumption significantly

### Execution Time
- Network latency for API calls
- Function execution time (especially code execution)
- Iteration overhead for complex tasks

### Rate Limits
- Google GenAI API rate limits apply
- Consider implementing request throttling for production use

## Troubleshooting

### Common Issues
1. **API Key**: Ensure `GEMINI_API_KEY` is set in `.env`
2. **Working Directory**: Verify `./calculator` exists and contains test app
3. **Dependencies**: Install requirements with `pip install -r requirements.txt`
4. **Path Issues**: All function calls use relative paths from working directory

### Debug Mode
Use `--verbose` flag to see:
- Token usage statistics
- Function call details with arguments
- Function execution results
- Conversation flow progression

## License

This project is provided as-is for educational and demonstration purposes.