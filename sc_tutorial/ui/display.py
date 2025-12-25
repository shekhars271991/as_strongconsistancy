"""Display helper functions for formatted terminal output."""

from .colors import Colors


def print_banner(text, char='='):
    """Print a prominent banner."""
    width = 70
    print(f"\n{Colors.HEADER}{Colors.BOLD}{char * width}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(width)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{char * width}{Colors.ENDC}\n")


def print_section(text):
    """Print a section header."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}▶ {text}{Colors.ENDC}")
    print(f"{Colors.DIM}{'-' * 60}{Colors.ENDC}")


def print_concept(title, explanation):
    """Print a concept with title and explanation."""
    print(f"\n{Colors.YELLOW}{Colors.BOLD}📚 {title}{Colors.ENDC}")
    for line in explanation.split('\n'):
        print(f"   {Colors.DIM}{line}{Colors.ENDC}")


def print_success(text):
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_info(text):
    """Print an info message."""
    print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")


def print_warning(text):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")


def print_error(text):
    """Print an error message."""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


def print_code(code):
    """Print code/command."""
    print(f"{Colors.DIM}  >>> {code}{Colors.ENDC}")


def wait_for_user(message="Press Enter to continue..."):
    """Wait for user input."""
    try:
        input(f"\n{Colors.BLUE}{message}{Colors.ENDC}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tutorial interrupted by user.{Colors.ENDC}")
        raise SystemExit(0)

