"""Lesson 9: Best Practices"""

from .base import BaseLesson
from ..ui.display import print_banner


class LessonBestPractices(BaseLesson):
    """Best practices lesson."""
    
    lesson_name = 'cluster'
    lesson_title = 'LESSON 9: BEST PRACTICES'
    
    def run(self):
        """Share SC best practices."""
        print_banner(self.lesson_title)
        
        practices = """
        ┌────────────────────────────────────────────────────────────────────┐
        │                    SC BEST PRACTICES                               │
        ├────────────────────────────────────────────────────────────────────┤
        │                                                                    │
        │  CONFIGURATION                                                     │
        │  ─────────────                                                     │
        │  • Set replication-factor >= cluster size (RF=3 for production)    │
        │  • Disable expiration (default-ttl 0) for critical data            │
        │  • Consider commit-to-device for maximum durability                │
        │  • Use rack-awareness for multi-AZ deployments                     │
        │                                                                    │
        │  OPERATIONS                                                        │
        │  ──────────                                                        │
        │  • Use generation checks for concurrent updates                    │
        │  • Handle InDoubt errors properly - read to verify                 │
        │  • Use durable deletes (creates tombstones)                        │
        │  • Prefer Session Consistency unless you need Linearizable         │
        │                                                                    │
        │  MONITORING                                                        │
        │  ──────────                                                        │
        │  • Watch dead_partitions and unavailable_partitions                │
        │  • Monitor client_write_error and client_read_error                │
        │  • Track fail_generation for conflict rates                        │
        │  • Alert on clock_skew_stop_writes                                 │
        │                                                                    │
        │  CLUSTER MANAGEMENT                                                │
        │  ──────────────────                                                │
        │  • Always use clean shutdowns (SIGTERM, not SIGKILL)               │
        │  • Configure NTP - clock skew > 27s can cause data loss            │
        │  • Monitor dead_partitions and unavailable_partitions              │
        │  • Plan roster changes carefully                                   │
        │                                                                    │
        │  AVOID                                                             │
        │  ─────                                                             │
        │  • Don't use non-durable deletes in production                     │
        │  • Don't enable client retransmit (can cause duplicates)           │
        │  • Don't ignore InDoubt errors                                     │
        │  • Don't switch from AP to SC on existing namespace                │
        │                                                                    │
        └────────────────────────────────────────────────────────────────────┘
        """
        print(practices)
        
        self.pause()

