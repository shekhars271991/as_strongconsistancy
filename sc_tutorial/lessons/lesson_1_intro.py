"""Lesson 1: Introduction to Strong Consistency"""

from .base import BaseLesson
from ..ui.display import print_banner, print_section, print_concept
from ..config import INTRO_TEXT


class LessonIntroduction(BaseLesson):
    """Introduction to Strong Consistency lesson."""
    
    lesson_name = 'introduction'
    lesson_title = 'LESSON 1: INTRODUCTION TO STRONG CONSISTENCY'
    
    def run(self):
        """Introduction to Strong Consistency."""
        print_banner(self.lesson_title)
        
        print_concept("What is Strong Consistency?", INTRO_TEXT)
        
        self.pause()
        
        print_section("Comparing AP vs SC Mode")
        
        comparison = """
        ┌─────────────────────┬──────────────────────┬──────────────────────┐
        │     Feature         │    AP Mode           │    SC Mode           │
        ├─────────────────────┼──────────────────────┼──────────────────────┤
        │ Data Consistency    │ Eventually consistent│ Strongly consistent  │
        │ Availability        │ Higher               │ Lower (when degraded)│
        │ Write Ordering      │ May reorder          │ Strict ordering      │
        │ Read Guarantees     │ May see stale data   │ Always current       │
        │ Network Partition   │ Both sides operate   │ One side unavailable │
        │ Use Case            │ Caching, analytics   │ Transactions, finance│
        └─────────────────────┴──────────────────────┴──────────────────────┘
        """
        print(comparison)
        
        self.pause()

