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

#### Basic Operations
```bash
# Code analysis
python main.py "explain how the calculator renders results"

# Simple bug fixing
python main.py "fix the bug: 3 + 7 * 2 should equal 17, not 20"

# Testing
python main.py "run the calculator tests and fix any failures"

# File operations
python main.py "create a hello world script and run it"
```

#### Advanced Capabilities
```bash
# Complex bug fixing
python main.py "the calculator has multiple complex bugs: division by zero returns infinity, there's a memory leak, and precision issues. analyze and fix these problems"

# Advanced feature development
python main.py "add support for parentheses, exponentiation operator, and modulo to the calculator with proper precedence"

# Sophisticated refactoring
python main.py "refactor the calculator using object-oriented design patterns like Strategy pattern and improve the architecture"

# Comprehensive analysis
python main.py "analyze the entire codebase, identify potential improvements, and implement best practices"

# Multi-step problem solving
python main.py "create a new calculator module with advanced features, test it thoroughly, and integrate it with the existing system"
```

#### Testing Enhanced Features
```bash
# Test complex expressions
python calculator/main.py "2**(3+1)"     # Should output: 16
python calculator/main.py "(5+3)*2"      # Should output: 16
python calculator/main.py "2**3*4+1"     # Should output: 33

# Test error handling
python calculator/main.py "10/0"         # Should show proper error message

# Verbose mode for debugging
python main.py "test all calculator features" --verbose
```

## Test Environment: Calculator App

The agent operates on a sample calculator application located in `./calculator/`:

### Calculator Structure
```
calculator/
├── main.py                    # CLI interface
├── tests.py                   # Original unit tests (9 test cases)
├── calculator.py              # Alternative simple calculator implementation
├── calculator_refactored.py   # OOP version using Strategy pattern
├── test_calculator.py         # Additional tests for enhanced features
└── pkg/
    ├── calculator.py          # Enhanced core calculator with advanced features
    └── render.py              # ASCII box rendering for results
```

### Calculator Features
- **Advanced Expression Evaluation**: Full infix notation with complex expression support
- **Supported Operations**: 
  - Basic: Addition (+), Subtraction (-), Multiplication (*), Division (/)
  - Advanced: Exponentiation (**), Parentheses grouping
- **Operator Precedence**: Exponentiation (3) > Multiplication/Division (2) > Addition/Subtraction (1)
- **Complex Expressions**: Support for nested parentheses like `2**(3+1)` and `(5+3)*2`
- **Advanced Tokenization**: Sophisticated parser handles multi-character operators
- **Robust Error Handling**: 
  - Division by zero protection with proper error messages
  - Mismatched parentheses detection
  - Invalid token and expression validation
  - Memory leak prevention
- **Visual Output**: Results displayed in ASCII box format
- **Multiple Implementations**: 
  - Enhanced version with full expression parsing
  - Refactored OOP version using Strategy pattern

## Agent Capabilities

### Advanced Autonomous Debugging
- **Complex Bug Detection**: Identifies multi-faceted issues like memory leaks, precision errors, and logic bugs
- **Root Cause Analysis**: Deep examination of code to identify interconnected problems
- **Comprehensive Fix Implementation**: Addresses multiple bugs simultaneously with proper error handling
- **Thorough Verification**: Tests fixes across multiple scenarios to ensure correctness

### Sophisticated Code Refactoring
- **Design Pattern Implementation**: Creates well-structured code using industry patterns (Strategy, Factory, etc.)
- **Architecture Improvement**: Refactors monolithic code into modular, maintainable components
- **Code Organization**: Separates concerns and improves overall code quality
- **Performance Optimization**: Eliminates inefficiencies and improves resource usage

### Advanced Feature Development
- **Complex Algorithm Implementation**: Adds sophisticated features like expression parsers and tokenizers
- **Mathematical Operations**: Implements advanced mathematical capabilities with proper precedence
- **Parser Development**: Creates robust tokenization and parsing systems
- **Error Handling Enhancement**: Implements comprehensive error detection and management

### Code Analysis & Understanding
- **Deep Structure Comprehension**: Analyzes complex codebases and understands architectural patterns
- **Cross-Module Analysis**: Traces functionality across multiple files and dependencies
- **Performance Analysis**: Identifies bottlenecks and optimization opportunities
- **Documentation Generation**: Creates comprehensive technical documentation

### File Management & Execution
- **Intelligent File Operations**: Creates, modifies, and organizes files based on project needs
- **Multi-File Coordination**: Manages changes across multiple related files
- **Test Integration**: Automatically creates and runs comprehensive test suites
- **Script Execution**: Runs complex scripts with proper error handling and output analysis

### Iterative Problem Solving
- **Multi-Step Planning**: Breaks complex tasks into manageable steps
- **Context Preservation**: Maintains conversation history for informed decision making
- **Adaptive Strategies**: Adjusts approach based on intermediate results
- **Quality Assurance**: Validates each step before proceeding to the next

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

## Recent Achievements (Prototype Branch)

The agent has demonstrated remarkable autonomous capabilities during prototype testing:

### ✅ Complex Multi-Bug Resolution
Successfully identified and fixed three interconnected bugs in a single session:
- **Division by Zero**: Implemented proper error handling with meaningful messages
- **Memory Leak**: Eliminated unnecessary expression history accumulation
- **Precision Loss**: Removed redundant float conversions causing accuracy degradation

### ✅ Advanced Feature Implementation
Added sophisticated mathematical capabilities:
- **Parentheses Support**: Full expression grouping with proper parsing
- **Exponentiation Operator**: Power calculations with correct precedence rules
- **Advanced Tokenization**: Multi-character operator recognition and handling
- **Shunting Yard Algorithm**: Proper infix-to-postfix expression conversion

### ✅ Architectural Refactoring
Created professional-grade code improvements:
- **Strategy Pattern**: Implemented proper OOP design patterns
- **Separation of Concerns**: Modular architecture with clear responsibilities
- **Error Handling**: Comprehensive exception management throughout
- **Code Quality**: Clean, maintainable, and extensible codebase

### Key Technical Achievements
- **Autonomous Problem Solving**: 20-iteration deep analysis and implementation
- **Context Preservation**: Maintained conversation history for informed decisions
- **Quality Assurance**: Verified all changes maintain backward compatibility
- **Test Integration**: Ensured existing test suites continue to pass

These achievements demonstrate the agent's evolution from a simple function-calling system to a sophisticated autonomous software engineering assistant capable of complex multi-step problem solving.

## License

This project is provided as-is for educational and demonstration purposes.