"""Lesson 4: Consistency Levels"""

import time
from .base import BaseLesson
from ..ui.display import (
    print_banner, print_section, print_concept,
    print_info, print_success, print_error
)
from ..config import CONSISTENCY_LEVELS


class LessonConsistency(BaseLesson):
    """Consistency levels demonstration lesson."""
    
    lesson_name = 'consistency'
    lesson_title = 'LESSON 4: CONSISTENCY LEVELS'
    
    def run(self):
        """Demonstrate different consistency levels."""
        import aerospike
        from aerospike import exception as ae_exception
        
        print_banner(self.lesson_title)
        
        print_concept("Session vs Linearizable Consistency", CONSISTENCY_LEVELS)
        
        self.pause()
        
        print_section("Demo: Session Consistency (Read-Your-Writes)")
        
        key = (self.namespace, self.set_name, 'session_test')
        
        try:
            print_info("Performing sequential writes and reads...")
            print_info("In session consistency, you always see your own writes.\n")
            
            for i in range(5):
                # Write
                self.client.put(key, {'version': i, 'timestamp': time.time()})
                
                # Read immediately
                _, _, data = self.client.get(key)
                
                status = "✓" if data['version'] == i else "✗"
                print(f"   Write v{i} → Read v{data['version']} {status}")
                
                time.sleep(0.1)
            
            print_success("\nSession consistency verified: All writes were immediately visible")
            
            self._safe_remove(key)
            
        except ae_exception.AerospikeError as e:
            print_error(f"Error: {e}")
        
        self.pause()
        
        print_section("Demo: Linearizable Reads")
        
        try:
            key = (self.namespace, self.set_name, 'linear_test')
            self.client.put(key, {'value': 0})
            
            iterations = 50
            
            print_info(f"Comparing read latency ({iterations} reads each)...\n")
            
            # Session consistency reads
            start = time.time()
            for _ in range(iterations):
                self.client.get(key)
            session_time = time.time() - start
            
            # Linearizable reads
            linear_policy = {'linearize_read': True}
            start = time.time()
            for _ in range(iterations):
                self.client.get(key, policy=linear_policy)
            linear_time = time.time() - start
            
            print(f"   Session consistency:     {session_time*1000:.2f}ms total ({session_time/iterations*1000:.3f}ms avg)")
            print(f"   Linearizable consistency: {linear_time*1000:.2f}ms total ({linear_time/iterations*1000:.3f}ms avg)")
            
            if linear_time > session_time:
                overhead = ((linear_time / session_time) - 1) * 100
                print(f"\n   Linearizable reads are ~{overhead:.1f}% slower")
            
            print_info("\nLinearizable reads are slower because they must verify")
            print_info("with replica nodes to ensure global consistency.")
            
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

