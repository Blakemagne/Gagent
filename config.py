# Configuration constants for the AI agent system
# These values control the behavior and safety limits of the agent

# Maximum number of characters to read from any single file
# This prevents the AI from reading huge files that could:
# 1. Use up too much memory
# 2. Exceed API token limits (APIs charge per token/character)
# 3. Take too long to process
# 10,000 characters is roughly 2,000-3,000 words of text
MAX_CHARS = 10000

# The directory where the AI is allowed to operate
# This is a CRITICAL SECURITY SETTING - it creates a "sandbox"
# The AI can ONLY access files within this directory, preventing it from:
# - Reading sensitive system files
# - Modifying important system files  
# - Accessing files outside the project
# "./calculator" means the "calculator" folder in the current directory
WORKING_DIR = "./calculator"
