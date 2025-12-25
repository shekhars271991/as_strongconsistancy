"""Base class for tutorial lessons."""

from ..ui.display import print_banner, print_section, print_concept
from ..ui.menu import interactive_menu
from ..cluster.validation import ClusterValidator


class BaseLesson:
    """Base class for all tutorial lessons."""
    
    lesson_name = 'basic_ops'  # Override in subclasses
    lesson_title = 'LESSON'    # Override in subclasses
    
    def __init__(self, client, namespace, set_name, interactive=True):
        self.client = client
        self.namespace = namespace
        self.set_name = set_name
        self.interactive = interactive
        self.validator = ClusterValidator(client, namespace)
    
    def pause(self, lesson_name=None):
        """Pause for user input in interactive mode with menu options."""
        if lesson_name is None:
            lesson_name = self.lesson_name
            
        if self.interactive:
            # Always validate cluster health before showing menu
            healthy = self.validator.validate(compact=True)
            
            if not healthy:
                from ..ui.display import print_warning
                print_warning("Issues detected! Please fix before continuing or press Enter to proceed anyway.")
            
            while True:
                choice = interactive_menu(lesson_name, self.namespace)
                if choice == 'continue':
                    break
                elif choice == 'validate':
                    # Full validation on manual request
                    self.validator.validate(compact=False)
    
    def run(self):
        """Run the lesson. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement run()")

