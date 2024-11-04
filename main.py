# main.py

from cli_interface import parse_arguments
from review_loop import run_review_loop

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Run the review loop with CLI arguments
    final_output = run_review_loop(
        prompt=args.prompt,
        max_attempts=args.attempts,
        timeout=args.timeout
    )
    print("Final Output:\n", final_output)

if __name__ == "__main__":
    main()