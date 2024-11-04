from code_generation import generate_code
from execution_manager import write_and_execute_code
from error_handler import analyze_error, log_error
from file_namer_assistant import generate_file_name
import openai
import os
from pathlib import Path
import logging
import re

# Directory settings
STABLE_DIR = "stable"
os.makedirs(STABLE_DIR, exist_ok=True)

# Set up logging
logging.basicConfig(level=logging.INFO, filename='execution_log.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def review_output(output, error):
    """Evaluate if the code is error-free and meets expected quality."""
    return not error  # Accept if there's no error

def programmer_decision(output, error, feedback, memory):
    """Use an LLM to determine whether to save to stable or retry based on output, error, feedback, and memory."""
    memory_content = "\n".join(memory)

    # Create messages for the LLM with the full historical context
    messages = [
        {
            "role": "system",
            "content": "You are a Python coding assistant responsible for reviewing and evaluating generated code."
        },
        {
            "role": "user",
            "content": (
                "Based on the following criteria, decide whether to save to stable or retry:\n\n"
                f"Output:\n{output}\n\n"
                f"Error:\n{error}\n\n"
                f"Feedback from previous attempts:\n{feedback}\n\n"
                f"Memory of previous attempts:\n{memory_content}\n\n"
                "Respond exactly in the following format:\n"
                "Decision: [1 or 2]\n"
                "Explanation: [Concise rationale]"
            )
        }
    ]

    # Call OpenAI's chat API to make the decision
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=50,
        temperature=0.3,
    )

    # Parse the decision from the response
    decision_text = response.choices[0].message["content"].strip()
    print(f"Decision Text: {decision_text}")  # For debugging
    match = re.search(r'Decision:\s*(\d)', decision_text)
    if match:
        decision = match.group(1)
    else:
        print("Failed to parse decision from LLM response.")
        decision = None

    # Handle invalid decision
    if decision not in ["1", "2"]:
        print("Invalid decision from LLM. Defaulting to retry.")
        decision = "2"

    return decision

def save_to_stable(code, filename):
    """Save the accepted code to the stable directory with a meaningful filename."""
    stable_path = os.path.join(STABLE_DIR, filename)
    try:
        with open(stable_path, 'w') as file:
            file.write(code)
        logging.info(f"Code saved to {stable_path}")
    except Exception as e:
        logging.error(f"Failed to save code: {e}")
        print("An error occurred while saving the file. Check the log for details.")

def run_review_loop(prompt, max_attempts, timeout):
    """Main review loop that iterates until code is accepted or max attempts are reached."""
    feedback = None  # Start with no feedback for the first generation
    memory = []  # Initialize memory as an empty list

    for attempt in range(max_attempts):
        print(f"Attempt {attempt + 1}")

        # Step 1: Generate code with or without feedback
        code = generate_code(prompt, feedback)
        print("Generated Code:\n", code)

        # Step 2: Write and execute code
        output, error = write_and_execute_code(code, timeout)
        print("Output:\n", output)

        # Only print error if there is one
        if error:
            print("Error:\n", error)

        # Step 3: Decide if the code meets requirements
        if review_output(output, error):
            # Call programmer LLM for a decision, providing memory context
            decision = programmer_decision(output, error, feedback, memory)
            print(f"Programmer LLM Decision: {decision}")

            if decision == "1":
                # Get existing files in the stable directory
                existing_files = [f.name for f in Path(STABLE_DIR).iterdir() if f.is_file()]
                
                # Generate a descriptive filename for the code
                filename = generate_file_name(code, existing_files)
                
                # Save the code using the generated filename
                save_to_stable(code, filename)
                print("Code accepted and saved by LLM!")
                return output  # Exit after saving
            elif decision == "2":
                print("Retrying with LLM feedback...\n")
            else:
                print("Unrecognized decision. Defaulting to retry.")
        else:
            # Step 4: Analyze and log error
            error_category, details = analyze_error(output, error)
            log_error(error_category, details)

            # Append feedback to memory for future attempts
            memory.append(details)
            feedback = details  # Set feedback for the next attempt

    print("Max attempts reached. Final output:\n", output)
    return output