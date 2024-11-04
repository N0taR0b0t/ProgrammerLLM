import os
import json
from pathlib import Path

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model Settings
MODEL = "gpt-4o-mini"

# Default Configurations
DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_TIMEOUT_SECONDS = 60

SYSTEM_PROMPT = """You are an expert Python developer with these priorities:
1. Efficiency: Write optimized, clean code
2. Reliability: Include proper error handling and input validation
3. Maintainability: Follow PEP 8 and use clear variable names
4. Memory: Learn from previous errors and avoid repeating them

Before generating code:
- Consider edge cases
- Plan resource usage
- Check for required dependencies
- Ensure proper error handling

Your code must be:
Self-contained (unless specific imports requested)
Properly formatted
Production-ready
Well-structured"""

# Directory Settings
BASE_DIR = Path(__file__).parent
STABLE_DIR = BASE_DIR / "stable"
CONTEXT_DIR = BASE_DIR / "context"
MEMORY_FILE = CONTEXT_DIR / "memory.json"

# Ensure directories exist
STABLE_DIR.mkdir(exist_ok=True)
CONTEXT_DIR.mkdir(exist_ok=True)

# Error Patterns
ERROR_PATTERNS = {
  "SyntaxError": {
      "pattern": "SyntaxError",
      "severity": "high",
      "requires_review": True
  },
  "ImportError": {
      "pattern": "ModuleNotFoundError",
      "severity": "medium",
      "requires_review": True
  },
  "TimeoutError": {
      "pattern": "timed out",
      "severity": "high",
      "requires_review": True
  },
  "RuntimeError": {
      "pattern": "RuntimeError",
      "severity": "medium",
      "requires_review": True
  },
  "LogicError": {
      "pattern": "ValueError",
      "severity": "medium",
      "requires_review": True
  }
}