"""Main tutorial orchestration class."""

import aerospike
from aerospike import exception as ae_exception

from .config import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_NAMESPACE, DEFAULT_SET, CONNECTION_TIMEOUT
from .ui.display import (
    print_banner, print_section, print_success, print_error, print_info, print_warning
)
from .ui.colors import Colors
from .ui.menu import interactive_menu
from .cluster.validation import ClusterValidator
from .lessons import (
    LessonAerolab,
    LessonIntroduction,
    LessonConfiguration,
    LessonBasicOperations,
    LessonConsistency,
    LessonConcurrentWrites,
    LessonGeneration,
    LessonErrorHandling,
    LessonClusterBehavior,
    LessonBestPractices,
)


class StrongConsistencyTutorial:
    """Interactive tutorial for Aerospike Strong Consistency."""
    
    def __init__(self, hosts=None, namespace=DEFAULT_NAMESPACE, interactive=True):
        """Initialize the tutorial."""
        if hosts is None:
            hosts = [(DEFAULT_HOST, DEFAULT_PORT)]
        
        self.hosts = hosts
        self.interactive = interactive
        self.client = None
        self.namespace = namespace
        self.set_name = DEFAULT_SET
        
        self.config = {
            'hosts': hosts,
            'policies': {
                'timeout': CONNECTION_TIMEOUT,
            },
            'use_services_alternate': True,
        }
        
        self.validator = None
    
    def connect(self):
        """Connect to the Aerospike cluster."""
        try:
            self.client = aerospike.client(self.config).connect()
            self.validator = ClusterValidator(self.client, self.namespace)
            print_success(f"Connected to Aerospike cluster at {self.hosts}")
            return True
        except ae_exception.AerospikeError as e:
            print_error(f"Failed to connect: {e}")
            print_info("Make sure the Aerospike cluster is running and accessible")
            return False
    
    def disconnect(self):
        """Disconnect from the cluster."""
        if self.client:
            self.client.close()
            print_info("Disconnected from Aerospike")
    
    def show_cluster_status(self):
        """Display current cluster and SC status."""
        print_section("Cluster Status Check")
        
        sc_enabled, info = self.validator.verify_sc_enabled()
        
        if isinstance(info, dict):
            print(f"\n   Namespace: {self.namespace}")
            if sc_enabled:
                print_success(f"Strong Consistency: True")
            else:
                print_error(f"Strong Consistency: False")
            print(f"   ├── Replication Factor: {info.get('replication_factor', 'N/A')}")
            print(f"   ├── NS Cluster Size: {info.get('ns_cluster_size', 'N/A')}")
            print(f"   ├── Dead Partitions: {info.get('dead_partitions', 'N/A')}")
            print(f"   └── Unavailable Partitions: {info.get('unavailable_partitions', 'N/A')}")
        
        return sc_enabled
    
    def run_tutorial(self, lessons=None, skip_sc_check=False):
        """Run the complete tutorial or specific lessons."""
        print_banner("AEROSPIKE STRONG CONSISTENCY TUTORIAL", '═')
        
        print("""
        Welcome to the Aerospike Strong Consistency Tutorial!
        
        This interactive guide will teach you:
        
          0. Setting Up SC with AeroLab (optional)
          1. Introduction to Strong Consistency
          2. Configuration and Setup
          3. Basic SC Operations  
          4. Consistency Levels
          5. Concurrent Write Ordering
          6. Optimistic Locking with Generations
          7. Error Handling
          8. Cluster Behavior under Failure
          9. Best Practices
        
        Press Ctrl+C at any time to exit.
        """)
        
        if not self.connect():
            print_error("Cannot proceed without cluster connection.")
            print_info("\nTo set up an SC cluster with AeroLab:")
            print(f"{Colors.DIM}")
            print("  aerolab config backend -t docker")
            print("  aerolab cluster create -n mydc -c 1 -f features.conf")
            print("  aerolab conf sc -n mydc")
            print(f"{Colors.ENDC}")
            return
        
        try:
            # Verify SC is enabled
            if not skip_sc_check:
                sc_enabled = self.show_cluster_status()
                
                if not sc_enabled:
                    print_error(f"\nStrong Consistency is NOT enabled on namespace '{self.namespace}'!")
                    print_info("\nWould you like to see AeroLab setup instructions?")
                    
                    if self.interactive:
                        try:
                            response = input(f"{Colors.BLUE}Show AeroLab setup? (y/n): {Colors.ENDC}").strip().lower()
                            if response == 'y':
                                lesson = LessonAerolab(self.client, self.namespace, self.set_name, self.interactive)
                                lesson.run()
                                print_warning("\nPlease set up an SC cluster and re-run this tutorial.")
                                return
                        except KeyboardInterrupt:
                            raise SystemExit(0)
                    else:
                        print_info("Run with --lessons 0 to see AeroLab setup instructions.")
                        return
                else:
                    print_success(f"\n✓ Strong Consistency verified on namespace '{self.namespace}'")
                
                # Pause before starting lessons (using 'introduction' to skip commands)
                if self.interactive:
                    self.validator.validate(compact=True)
                    while True:
                        choice = interactive_menu('introduction', self.namespace)
                        if choice == 'continue':
                            break
                        elif choice == 'validate':
                            self.validator.validate(compact=False)
            
            # Define all lessons
            all_lessons = [
                ('0', 'AeroLab Setup', LessonAerolab),
                ('1', 'Introduction', LessonIntroduction),
                ('2', 'Configuration', LessonConfiguration),
                ('3', 'Basic Operations', LessonBasicOperations),
                ('4', 'Consistency Levels', LessonConsistency),
                ('5', 'Concurrent Writes', LessonConcurrentWrites),
                ('6', 'Generation Conflicts', LessonGeneration),
                ('7', 'Error Handling', LessonErrorHandling),
                ('8', 'Cluster Behavior', LessonClusterBehavior),
                ('9', 'Best Practices', LessonBestPractices),
            ]
            
            # Filter lessons if specific ones requested
            if lessons:
                all_lessons = [(num, name, cls) for num, name, cls in all_lessons if num in lessons]
            else:
                # Skip lesson 0 by default
                all_lessons = all_lessons[1:]
            
            # Run lessons
            for lesson_num, lesson_name, lesson_class in all_lessons:
                try:
                    lesson = lesson_class(self.client, self.namespace, self.set_name, self.interactive)
                    lesson.run()
                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}Lesson interrupted. Moving to next...{Colors.ENDC}")
                    continue
                except SystemExit:
                    raise
            
            # Completion message
            print_banner("TUTORIAL COMPLETE!", '═')
            print("""
        Congratulations! You've completed the Strong Consistency tutorial.
        
        Key Takeaways:
          ✓ SC guarantees write ordering and durability
          ✓ Use roster to manage cluster membership
          ✓ Session consistency is the default (and usually sufficient)
          ✓ Use generation checks for optimistic locking
          ✓ Handle InDoubt errors by reading to verify
          ✓ Monitor partition health for cluster issues
        
        For more information:
          • Aerospike SC Documentation: https://aerospike.com/docs/server/operations/configure/consistency
          • Managing SC Clusters: https://aerospike.com/docs/server/operations/manage/consistency
            """)
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Tutorial interrupted by user.{Colors.ENDC}")
        except SystemExit:
            pass
        finally:
            self.disconnect()

