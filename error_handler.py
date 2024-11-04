# error_handler.py

def analyze_error(output, error):
    """Categorize the error and provide targeted feedback for improvement."""
    if "SyntaxError" in error:
        return "syntax_error", "Syntax error detected. Please check the code structure and syntax."
    elif "ModuleNotFoundError" in error:
        missing_module = error.split("'")[-2]
        return "missing_import", f"Missing import for '{missing_module}'. Ensure necessary imports are included."
    elif "timed out" in error:
        return "timeout", "Execution timed out. Consider optimizing code or simplifying logic."
    elif output.strip() == "":
        return "empty_output", "Code executed but returned no output. Verify logic and ensure code produces output."
    else:
        return "general_error", "General error occurred. Check the code and logic flow."

def log_error(error_category, details):
    """Log error details for debugging and iterative improvement."""
    print(f"[ERROR] Category: {error_category} | Details: {details}")