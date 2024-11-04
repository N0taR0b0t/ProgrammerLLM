# cli_interface.py

import argparse
from config import DEFAULT_MAX_ATTEMPTS, DEFAULT_TIMEOUT_SECONDS

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run LLM code generation and execution framework.")
    parser.add_argument("prompt", type=str, help="Task description for the LLM to generate code.")
    parser.add_argument("--attempts", type=int, default=DEFAULT_MAX_ATTEMPTS, help="Maximum retry attempts.")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="Timeout for code execution in seconds.")
    parser.add_argument("--tier", choices=["light", "medium", "heavy"], help="Preset configuration for retries and timeouts.")

    args = parser.parse_args()

    # Adjust configuration based on tier
    if args.tier == "light":
        args.attempts = 2
        args.timeout = 30
    elif args.tier == "medium":
        args.attempts = 4
        args.timeout = 60
    elif args.tier == "heavy":
        args.attempts = 6
        args.timeout = 300

    # Validate prompt to avoid Markdown-style issues
    if "```" in args.prompt:
        print("Warning: Prompt contains Markdown formatting. Please remove any ``` symbols to avoid issues.")

    return args