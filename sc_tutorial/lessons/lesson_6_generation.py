"""Lesson 6: Generation-based Conflict Detection"""

from .base import BaseLesson
from ..ui.display import (
    print_banner, print_section, print_concept,
    print_info, print_success, print_error, print_code
)


class LessonGeneration(BaseLesson):
    """Generation conflict detection lesson."""
    
    lesson_name = 'generation'
    lesson_title = 'LESSON 6: OPTIMISTIC LOCKING WITH GENERATIONS'
    
    def run(self):
        """Demonstrate generation-based conflict detection."""
        import aerospike
        from aerospike import exception as ae_exception
        
        print_banner(self.lesson_title)
        
        print_concept("Generation Numbers", """
Every record has a GENERATION number that increments with each write.
This enables optimistic locking (check-and-set):

  1. Read record and note its generation
  2. Modify data locally
  3. Write back with generation check
  4. If generation changed, write fails → retry

This prevents lost updates in concurrent scenarios.
""")
        
        self.pause()
        
        print_section("Demo: Generation Conflict Detection")
        
        key = (self.namespace, self.set_name, 'conflict_test')
        
        try:
            # Initial write
            self.client.put(key, {'value': 'initial', 'version': 1})
            _, meta1 = self.client.exists(key)
            gen1 = meta1['gen']
            print_info(f"Initial write completed, generation: {gen1}")
            
            # Simulate another client updating the record
            print_info("Simulating another client's update...")
            self.client.put(key, {'value': 'updated_by_other', 'version': 2})
            _, meta2 = self.client.exists(key)
            gen2 = meta2['gen']
            print_info(f"Other client updated, generation: {gen2}")
            
            # Try to update with stale generation
            print_info(f"\nAttempting update with stale generation ({gen1})...")
            print_code(f"client.put(key, data, meta={{'gen': {gen1}}}, policy={{'gen': POLICY_GEN_EQ}})")
            
            try:
                policy = {'gen': aerospike.POLICY_GEN_EQ}
                self.client.put(
                    key, 
                    {'value': 'my_update', 'version': 3}, 
                    meta={'gen': gen1}, 
                    policy=policy
                )
                print_error("Update succeeded (unexpected!)")
            except ae_exception.RecordGenerationError:
                print_success("✓ CONFLICT DETECTED! Write rejected due to generation mismatch")
                print_info("This prevents overwriting another client's changes.")
            
            # Show final value
            _, _, final = self.client.get(key)
            print(f"\n   Final value: {final['value']} (preserved from other client)")
            
            self._safe_remove(key)
            
        except ae_exception.AerospikeError as e:
            print_error(f"Error: {e}")
        
        self.pause()
    
    def _safe_remove(self, key):
        """Remove a record safely in SC mode using durable delete."""
        try:
            self.client.remove(key, policy={'durable_delete': True})
        except:
            pass

