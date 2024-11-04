# execution_manager.py

import subprocess
import tempfile
import os
import shutil

# Check if 'python3' exists; use it if available, otherwise 'python'
PYTHON_CMD = "python3" if shutil.which("python3") else "python"

def write_and_execute_code(code, timeout):
    """Write code to a temporary file and execute it, capturing output and errors."""
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
        temp_file.write(code.encode())
        temp_file_path = temp_file.name

    try:
        # Execute the Python file
        result = subprocess.run(
            [PYTHON_CMD, temp_file_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )
        output = result.stdout
        error = result.stderr
    except subprocess.CalledProcessError as e:
        output = e.stdout
        error = e.stderr
    except subprocess.TimeoutExpired:
        output = ""
        error = "Execution timed out."
    finally:
        os.remove(temp_file_path)

    # Ensure exactly two values are returned
    return output, error