"""Lesson 7: Error Handling in SC Mode"""

from .base import BaseLesson
from ..ui.display import print_banner, print_section, print_concept
from ..config import INDOUBT_CONCEPT


class LessonErrorHandling(BaseLesson):
    """Error handling lesson."""
    
    lesson_name = 'errors'
    lesson_title = 'LESSON 7: ERROR HANDLING IN SC MODE'
    
    def run(self):
        """Explain SC-specific error handling."""
        print_banner(self.lesson_title)
        
        print_concept("InDoubt Errors", INDOUBT_CONCEPT)
        
        self.pause()
        
        print_section("Common SC Errors")
        
        errors_table = """
        ┌─────────────────────────┬────────────────────────────────────────────┐
        │ Error                   │ Meaning                                    │
        ├─────────────────────────┼────────────────────────────────────────────┤
        │ PARTITION_UNAVAILABLE   │ Data partition is not accessible           │
        │ INVALID_NODE_ERROR      │ No node available for the partition        │
        │ TIMEOUT                 │ Operation timed out (InDoubt possible)     │
        │ GENERATION_ERROR        │ Record was modified by another client      │
        │ FORBIDDEN               │ Operation not allowed (e.g., cluster issue)│
        │ FAIL_FORBIDDEN          │ Non-durable delete blocked in SC           │
        └─────────────────────────┴────────────────────────────────────────────┘
        """
        print(errors_table)
        
        print_concept("Handling InDoubt", """
When you receive a timeout with InDoubt=True:

  1. Don't assume the write failed
  2. Read the record to check its state
  3. Use idempotent operations when possible
  4. Use generation checks for safe retries
  
Example pattern:
  try:
      client.put(key, data, meta={'gen': expected_gen}, 
                 policy={'gen': POLICY_GEN_EQ})
  except TimeoutError as e:
      if e.in_doubt:
          # Read to check if write was applied
          _, meta, _ = client.get(key)
          if meta['gen'] > expected_gen:
              # Write was applied
          else:
              # Retry the write
""")
        
        self.pause()

