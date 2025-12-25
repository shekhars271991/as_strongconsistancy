"""Lesson 3: Basic SC Operations"""

from datetime import datetime
from .base import BaseLesson
from ..ui.display import (
    print_banner, print_section, print_concept, 
    print_info, print_success, print_warning, print_error, print_code
)


class LessonBasicOperations(BaseLesson):
    """Basic SC operations lesson."""
    
    lesson_name = 'basic_ops'
    lesson_title = 'LESSON 3: BASIC SC OPERATIONS'
    
    def run(self):
        """Demonstrate basic SC operations."""
        import aerospike
        from aerospike import exception as ae_exception
        
        print_banner(self.lesson_title)
        
        print_concept("SC Write Guarantees", """
When a write succeeds in SC mode:
  • The write has been replicated to all required nodes
  • The write is durable (won't be lost)
  • All subsequent reads will see this write
  • The write has a specific position in the record's history
""")
        
        self.pause()
        
        print_section("Demo: Write and Read Operations")
        
        key = (self.namespace, self.set_name, 'demo_key_1')
        
        try:
            # Write
            print_info("Writing a record...")
            print_code(f"client.put(key, {{'name': 'Alice', 'balance': 1000}})")
            
            record = {
                'name': 'Alice',
                'balance': 1000,
                'created_at': datetime.now().isoformat()
            }
            
            self.client.put(key, record)
            print_success("Write successful!")
            
            # Read
            print_info("\nReading the record back...")
            print_code("client.get(key)")
            
            _, meta, fetched = self.client.get(key)
            print_success(f"Read successful!")
            print(f"   Data: {fetched}")
            print(f"   Generation: {meta['gen']}")
            print(f"   TTL: {meta['ttl']}")
            
            # Update
            print_info("\nUpdating the record...")
            print_code(f"client.put(key, {{'balance': 1500}})")
            
            self.client.put(key, {'balance': 1500})
            
            _, meta2, fetched2 = self.client.get(key)
            print_success(f"Update successful!")
            print(f"   New balance: {fetched2.get('balance')}")
            print(f"   Generation: {meta['gen']} → {meta2['gen']}")
            
            # Cleanup - use durable delete in SC mode
            print_info("\nCleaning up with durable delete...")
            print_code("client.remove(key, policy={'durable_delete': True})")
            try:
                self.client.remove(key, policy={'durable_delete': True})
                print_success("Record deleted with tombstone")
            except ae_exception.AerospikeError:
                print_warning("Delete requires durable_delete or allow-expunge enabled")
            
        except ae_exception.AerospikeError as e:
            print_error(f"Operation failed: {e}")
            self._explain_error(e)
        
        self.pause()
    
    def _explain_error(self, error):
        """Provide helpful explanation for common errors."""
        error_str = str(error)
        
        if 'PARTITION_UNAVAILABLE' in error_str:
            print_info("This partition's data is not currently accessible.")
            print_info("Check if nodes are missing from the cluster or roster.")
        elif 'TIMEOUT' in error_str:
            print_info("The operation timed out. Check if the cluster is healthy.")
            if hasattr(error, 'in_doubt') and error.in_doubt:
                print_warning("InDoubt: The write may or may not have been applied!")
        elif 'GENERATION' in error_str:
            print_info("The record was modified since you last read it.")
            print_info("Re-read the record and retry with the new generation.")
        elif 'FORBIDDEN' in error_str:
            print_info("This operation is not allowed in SC mode.")
            print_info("For deletes, use durable_delete=True or enable allow-expunge.")

