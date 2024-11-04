import openai
import os
from pathlib import Path
import re

from config import OPENAI_API_KEY, MODEL

openai.api_key = OPENAI_API_KEY

STABLE_DIR = Path("stable")

def read_file_content(file_path):
    """Read the content of a Python file."""
    with open(file_path, 'r') as file:
        return file.read()

def generate_file_name(content, existing_files):
    messages = [
        {"role": "system", "content": "You are an assistant who names Python files based on their functionality."},
        {"role": "user", "content": (
            "Given the following code, suggest a short, descriptive filename based on what the code does. Do not include 'py' or 'python' in the name.\n\n"
            f"Code:\n{content}\n\n"
            "Ensure the name is in this format: `[descriptive_name].py`.\n"
            "Do not use any existing file names from this list:\n"
            f"{', '.join(existing_files)}"
        )}
    ]
    
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=0.5,
        max_tokens=20  # Limit to a short, filename-length response
    )
    
    suggested_name = response.choices[0].message["content"].strip()
    
    # Clean up the response to make sure it’s a valid Python filename
    suggested_name = re.sub(r'[^\w\-_]', '', suggested_name) + ".py"
    
    return suggested_name if suggested_name not in existing_files else None

def rename_file_with_unique_name(file_path):
    """Rename the file based on generated name and ensure uniqueness."""
    content = read_file_content(file_path)
    existing_files = [f.name for f in STABLE_DIR.iterdir() if f.is_file()]
    
    suggested_name = generate_file_name(content, existing_files)
    
    # If suggested_name is None or already exists, generate a unique name
    if not suggested_name:
        base_name = "code_file"
        counter = 1
        suggested_name = f"{base_name}_{counter}.py"
        
        # Increment counter until a unique name is found
        while suggested_name in existing_files:
            counter += 1
            suggested_name = f"{base_name}_{counter}.py"

    # Rename the file
    new_path = STABLE_DIR / suggested_name
    os.rename(file_path, new_path)
    print(f"File renamed to: {new_path}")

    return new_path

# Function to trigger the assistant on a new file in `stable`
def process_new_file():
    """Process and rename the latest file in the stable directory."""
    # Assuming new files are added with temporary names
    all_files = sorted(STABLE_DIR.glob("*.py"), key=os.path.getctime)
    if all_files:
        latest_file = all_files[-1]
        rename_file_with_unique_name(latest_file)
    else:
        print("No files to process.")