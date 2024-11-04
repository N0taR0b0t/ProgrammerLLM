import openai
from config import OPENAI_API_KEY, MODEL, SYSTEM_PROMPT
from memory_manager import MemoryManager

openai.api_key = OPENAI_API_KEY

# Global instance of CodeGenerator for backward compatibility
_generator = None

def get_generator():
    """Singleton pattern to get or create CodeGenerator instance."""
    global _generator
    if _generator is None:
        _generator = CodeGenerator()
    return _generator

class CodeGenerator:
    def __init__(self):
        self.memory_manager = MemoryManager()

    def generate_code(self, prompt, feedback_history=None):
        """Generate Python code with enhanced context and memory."""
        learning_context = self.memory_manager.get_learning_context()
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": self._format_generation_prompt(
                    prompt, 
                    feedback_history, 
                    learning_context
                )
            }
        ]

        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )

        code = response.choices[0].message["content"]
        return self._clean_code(code)

    def _format_generation_prompt(self, prompt, feedback_history, learning_context):
        """Format the generation prompt with comprehensive context."""
        return f"""Task: {prompt}

Requirements:
1. Generate complete, executable Python code without additional commentary or explanations.
2. Include necessary imports and error handling.
3. Ensure code is properly formatted, structured, and self-contained.

Expected Output Format:
Only the code without any additional commentary.
"""


    def _clean_code(self, code):
        """Clean and format the generated code."""
        code = code.replace("```python", "").replace("```", "")
        return code.strip()
    
    def _format_feedback_history(self, feedback_history):
        """Format feedback history for prompt context."""
        if not feedback_history:
            return "None"
        return "\n".join(f"- {feedback}" for feedback in feedback_history)

    def _format_learning_context(self, learning_context):
        """Format learning context for prompt."""
        common_errors = learning_context["common_errors"]
        successful_patterns = learning_context["successful_patterns"]
        
        return f"""Common Issues:
{self._format_error_patterns(common_errors)}

Successful Patterns:
{self._format_success_patterns(successful_patterns)}"""

    def _format_error_patterns(self, error_patterns):
        """Format error patterns for prompt context."""
        if not error_patterns.get("frequent_errors"):
            return "No common errors recorded"
        
        return "\n".join(
            f"- {error_type}: {count} occurrences"
            for error_type, count in error_patterns["frequent_errors"].items()
        )

    def _format_success_patterns(self, success_patterns):
        """Format success patterns for prompt context."""
        if not success_patterns:
            return "No success patterns recorded"
        
        return "\n".join(
            f"- {pattern['pattern']}"
            for pattern in success_patterns[-3:]  # Last 3 successful patterns
        )

# Backward compatibility function
def generate_code(prompt, feedback_history=None):
    """Backward compatibility wrapper for the CodeGenerator class."""
    generator = get_generator()
    return generator.generate_code(prompt, feedback_history)