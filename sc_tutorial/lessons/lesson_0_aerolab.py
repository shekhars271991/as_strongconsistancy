"""Lesson 0: AeroLab Setup"""

from .base import BaseLesson
from ..ui.display import print_banner, print_section, print_concept
from ..ui.colors import Colors
from ..config import AEROLAB_SETUP, AEROLAB_MULTI_NODE


class LessonAerolab(BaseLesson):
    """AeroLab setup instructions lesson."""
    
    lesson_name = 'aerolab'
    lesson_title = 'LESSON 0: SETTING UP SC WITH AEROLAB'
    
    def run(self):
        """Show AeroLab setup instructions."""
        print_banner(self.lesson_title)
        
        print_concept("What is AeroLab?", """
AeroLab is Aerospike's official tool for quickly deploying development 
and testing clusters. It supports Docker, AWS, and GCP backends.

For SC development, AeroLab is the fastest way to get started!
""")
        
        self.pause()
        
        print_section("Quick Setup (3 Commands)")
        print(f"{Colors.DIM}{AEROLAB_SETUP}{Colors.ENDC}")
        
        self.pause()
        
        print_section("Multi-Node SC Cluster")
        print(f"{Colors.DIM}{AEROLAB_MULTI_NODE}{Colors.ENDC}")
        
        self.pause()
        
        print_section("Verifying Your Setup")
        
        verify_commands = """
        # Check if AeroLab is installed
        aerolab version
        
        # List running clusters
        aerolab cluster list
        
        # Check SC is enabled on your cluster
        docker exec aerolab-mydc_1 asinfo -v "namespace/test" | tr ';' '\\n' | grep strong
        
        # Expected output:
        # strong-consistency=true
        # strong-consistency-allow-expunge=false
        
        # Check roster is configured
        docker exec aerolab-mydc_1 asinfo -v "roster:namespace=test"
        
        # Expected: roster=<node_id>:pending_roster=<node_id>:observed_nodes=<node_id>
        """
        print(f"{Colors.DIM}{verify_commands}{Colors.ENDC}")
        
        self.pause()

