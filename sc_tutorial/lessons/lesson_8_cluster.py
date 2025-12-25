"""Lesson 8: Cluster Behavior Under Failure"""

from .base import BaseLesson
from ..ui.display import print_banner, print_section, print_concept
from ..ui.colors import Colors
from ..config import PARTITION_CONCEPT


class LessonClusterBehavior(BaseLesson):
    """Cluster behavior under failure lesson."""
    
    lesson_name = 'cluster'
    lesson_title = 'LESSON 8: CLUSTER BEHAVIOR UNDER FAILURE'
    
    def run(self):
        """Explain cluster behavior in various scenarios."""
        print_banner(self.lesson_title)
        
        print_concept("Partition States", PARTITION_CONCEPT)
        
        self.pause()
        
        print_section("Failure Scenarios")
        
        scenarios = """
        SCENARIO 1: Single Node Failure (RF=2)
        ─────────────────────────────────────
        • All partitions remain AVAILABLE
        • Reads and writes continue normally
        • Data is re-replicated to remaining nodes
        
        SCENARIO 2: Multiple Node Failures (< RF nodes remain)
        ─────────────────────────────────────────────────────
        • Some partitions become UNAVAILABLE
        • Affected records cannot be read or written
        • Restore nodes or wait for recovery
        
        SCENARIO 3: Network Partition (Split Brain)
        ──────────────────────────────────────────
        • SC prevents both sides from operating independently
        • Only the side with majority + roster continues
        • Other side marks partitions as unavailable
        • This PREVENTS data conflicts (unlike AP mode)
        
        SCENARIO 4: Unclean Shutdown
        ────────────────────────────
        • Node is marked with "evade flag"
        • Partitions may become DEAD
        • Requires manual 'revive' command
        • Use commit-to-device to prevent data loss
        """
        print(f"{Colors.DIM}{scenarios}{Colors.ENDC}")
        
        self.pause()
        
        print_section("Recovery Commands")
        
        commands = """
        # Check partition status:
        asinfo -v "namespace/sc_namespace" | grep -E "dead|unavail"
        
        # View roster status:
        asinfo -v "roster:namespace=sc_namespace"
        
        # Revive dead partitions (use with caution):
        asinfo -v "revive:namespace=sc_namespace"
        
        # Force recluster after changes:
        asinfo -v "recluster:"
        """
        print(f"{Colors.DIM}{commands}{Colors.ENDC}")
        
        self.pause()

