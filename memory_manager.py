import json
from datetime import datetime
from pathlib import Path
from config import MEMORY_FILE

class MemoryManager:
  def __init__(self):
      self.memory_file = MEMORY_FILE
      self.load_memory()

  def load_memory(self):
      """Load existing memory or create new if doesn't exist."""
      if self.memory_file.exists():
          with open(self.memory_file, 'r') as f:
              self.memory = json.load(f)
      else:
          self.memory = {
              "error_history": [],
              "success_patterns": [],
              "failed_patterns": [],
              "optimization_history": []
          }

  def save_memory(self):
      """Save current memory state to file."""
      with open(self.memory_file, 'w') as f:
          json.dump(self.memory, f, indent=2)

  def add_error(self, error_type, context, code_snippet=None):
      """Record new error with context."""
      error_entry = {
          "type": error_type,
          "context": context,
          "timestamp": datetime.now().isoformat(),
          "code_snippet": code_snippet,
          "frequency": self.get_error_frequency(error_type) + 1
      }
      self.memory["error_history"].append(error_entry)
      self.save_memory()

  def add_success(self, pattern, context):
      """Record successful code pattern."""
      success_entry = {
          "pattern": pattern,
          "context": context,
          "timestamp": datetime.now().isoformat()
      }
      self.memory["success_patterns"].append(success_entry)
      self.save_memory()

  def get_error_frequency(self, error_type):
      """Calculate how often an error type occurs."""
      return sum(1 for error in self.memory["error_history"] 
                if error["type"] == error_type)
      
  def get_learning_context(self):
    """Generate learning context from historical data."""
    return {
        "common_errors": self.analyze_error_patterns(),
        "successful_patterns": self.memory["success_patterns"],
        "anti_patterns": self.memory["failed_patterns"]
    }

  def analyze_error_patterns(self):
      """Analyze patterns in error history."""
      error_counts = {}
      for error in self.memory["error_history"]:
          error_type = error["type"]
          error_counts[error_type] = error_counts.get(error_type, 0) + 1
      
      return {
          "frequent_errors": error_counts,
          "recent_errors": self.memory["error_history"][-5:],
          "total_errors": len(self.memory["error_history"])
      }

  def get_optimization_suggestions(self):
      """Generate optimization suggestions based on history."""
      return [
          entry for entry in self.memory["optimization_history"]
          if entry["success_rate"] > 0.7
      ]