"""Lesson 5: Concurrent Write Ordering"""

import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from .base import BaseLesson
from ..ui.display import (
    print_banner, print_section, print_concept,
    print_info, print_success, print_warning, print_error
)


class LessonConcurrentWrites(BaseLesson):
    """Concurrent write ordering lesson."""
    
    lesson_name = 'basic_ops'
    lesson_title = 'LESSON 5: CONCURRENT WRITE ORDERING'
    
    def run(self):
        """Demonstrate SC behavior with concurrent writes."""
        import aerospike
        from aerospike import exception as ae_exception
        from aerospike_helpers.operations import operations as ops
        
        print_banner(self.lesson_title)
        
        print_concept("Write Ordering Guarantee", """
In SC mode, all writes to a single record are applied in a specific,
sequential order. This means:

  • Concurrent writes from different clients are serialized
  • Each write gets a unique position in the record's history
  • No writes are lost or reordered
  • The generation number reflects the total write count
""")
        
        self.pause()
        
        print_section("Demo: Concurrent Counter Increments")
        
        key = (self.namespace, self.set_name, 'counter')
        num_threads = 5
        increments_per_thread = 20
        results = []
        errors = []
        lock = threading.Lock()
        
        try:
            # Initialize counter
            self.client.put(key, {'counter': 0})
            print_info(f"Initialized counter to 0")
            print_info(f"Starting {num_threads} threads, each doing {increments_per_thread} increments...\n")
            
            def increment_worker(thread_id):
                """Worker function to increment counter."""
                for i in range(increments_per_thread):
                    try:
                        ops_list = [
                            ops.increment('counter', 1),
                            ops.read('counter')
                        ]
                        _, _, result = self.client.operate(key, ops_list)
                        
                        with lock:
                            results.append(result['counter'])
                            
                    except ae_exception.AerospikeError as e:
                        with lock:
                            errors.append((thread_id, str(e)))
                
                return thread_id
            
            # Run concurrent increments
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(increment_worker, i) for i in range(num_threads)]
                for future in as_completed(futures):
                    future.result()
            
            elapsed = time.time() - start_time
            
            # Verify results
            _, _, final = self.client.get(key)
            expected = num_threads * increments_per_thread
            
            print(f"   Time elapsed: {elapsed:.2f}s")
            print(f"   Expected final value: {expected}")
            print(f"   Actual final value: {final['counter']}")
            print(f"   Successful increments: {len(results)}")
            print(f"   Errors: {len(errors)}")
            
            # Check uniqueness
            unique_values = len(set(results))
            
            if final['counter'] == len(results) and unique_values == len(results):
                print_success("\n✓ SC VERIFIED: All increments counted, all values unique!")
                print_info("Each concurrent increment got a unique counter value.")
            else:
                print_warning(f"Unique values: {unique_values} / {len(results)}")
            
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

