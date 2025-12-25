"""Lesson 2: SC Configuration"""

from .base import BaseLesson
from ..ui.display import print_banner, print_section, print_concept, print_info, print_success
from ..ui.colors import Colors
from ..config import ROSTER_CONCEPT


class LessonConfiguration(BaseLesson):
    """SC configuration lesson."""
    
    lesson_name = 'configuration'
    lesson_title = 'LESSON 2: CONFIGURING STRONG CONSISTENCY'
    
    def run(self):
        """Lesson on SC configuration."""
        print_banner(self.lesson_title)
        
        print_section("Step 1: Enable SC in namespace configuration")
        
        config_example = """
        # In aerospike.conf:
        
        namespace sc_namespace {
            strong-consistency true     # Enable SC mode
            replication-factor 2        # RF must match cluster size (1 for single-node)
            default-ttl 0               # Recommended: disable expiration
            nsup-period 0               # Disable supervisor
            
            storage-engine memory {
                file /opt/aerospike/data/sc.dat
                filesize 2G
            }
        }
        """
        print(f"{Colors.DIM}{config_example}{Colors.ENDC}")
        
        print_concept("Key Configuration Parameters", """
• strong-consistency true  - Enables SC mode for the namespace
• replication-factor N     - SC requires nodes >= RF. Use RF=1 for single-node,
                             RF=2+ for multi-node (RF=3 recommended for production)
• default-ttl 0            - Disable expiration (recommended for SC)
• commit-to-device true    - Optional: ensures durability on crash
""")
        
        self.pause()
        
        print_section("Step 2: Configure the Roster")
        
        print_concept("Roster Configuration", ROSTER_CONCEPT)
        
        roster_commands = """
        # View current roster status:
        asinfo -v "roster:namespace=sc_namespace"
        
        # Set roster with observed nodes:
        asinfo -v "roster-set:namespace=sc_namespace;nodes=<node_ids>"
        
        # Apply the roster (trigger recluster):
        asinfo -v "recluster:"
        
        # Using asadm (easier):
        asadm> manage roster stage observed ns sc_namespace
        asadm> manage recluster
        """
        print(f"{Colors.DIM}{roster_commands}{Colors.ENDC}")
        
        self.pause()
        
        # Show actual cluster info if connected
        if self.client:
            print_section("Current Cluster Configuration")
            self._show_cluster_info()
        
        self.pause()
    
    def _show_cluster_info(self):
        """Display current cluster and namespace information."""
        try:
            nodes = self.client.get_nodes()
            print_info(f"Connected nodes: {len(nodes)}")
            
            for node in nodes:
                print(f"   • {node}")
            
            # Get namespace info using info_all
            info_dict = self.client.info_all(f"namespace/{self.namespace}")
            
            if info_dict:
                first_response = list(info_dict.values())[0]
                if isinstance(first_response, tuple):
                    info = first_response[1] if first_response[0] is None else ""
                else:
                    info = first_response
                
                params = dict(item.split('=') for item in info.split(';') if '=' in item)
                
                print(f"\n   Namespace: {self.namespace}")
                print(f"   ├── strong-consistency: {params.get('strong-consistency', 'N/A')}")
                print(f"   ├── replication-factor: {params.get('replication-factor', 'N/A')}")
                print(f"   ├── ns_cluster_size: {params.get('ns_cluster_size', 'N/A')}")
                print(f"   ├── dead_partitions: {params.get('dead_partitions', 'N/A')}")
                print(f"   └── unavailable_partitions: {params.get('unavailable_partitions', 'N/A')}")
                
        except Exception as e:
            from ..ui.display import print_warning
            print_warning(f"Could not get cluster info: {e}")

