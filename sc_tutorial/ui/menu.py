"""Interactive menu system for the tutorial."""

from .colors import Colors
from ..cluster.shell import open_aql_shell, open_asadm_shell, detect_aerolab_container
from ..commands.suggested import show_suggested_commands


def interactive_menu(lesson_name='basic_ops', namespace='test'):
    """Display interactive menu and handle user choice."""
    container = detect_aerolab_container()
    
    # Only show suggested commands after configuration lessons (lesson 3+)
    # Skip for setup/intro/configuration lessons
    skip_commands = lesson_name in ['aerolab', 'introduction', 'configuration']
    if not skip_commands:
        show_suggested_commands(lesson_name)
    
    while True:
        print(f"\n{Colors.BOLD}{'═'*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}  What would you like to do?{Colors.ENDC}")
        print(f"{Colors.BOLD}{'═'*60}{Colors.ENDC}")
        print(f"  {Colors.GREEN}[Enter]{Colors.ENDC} Continue to next section")
        print(f"  {Colors.CYAN}[a]{Colors.ENDC}     Open AQL shell (query/insert data)")
        print(f"  {Colors.CYAN}[s]{Colors.ENDC}     Open ASADM shell (admin commands)")
        print(f"  {Colors.YELLOW}[v]{Colors.ENDC}     Validate cluster health")
        print(f"  {Colors.RED}[q]{Colors.ENDC}     Quit tutorial")
        print(f"{Colors.BOLD}{'═'*60}{Colors.ENDC}")
        
        try:
            choice = input(f"{Colors.BLUE}Enter choice [Enter/a/s/v/q]: {Colors.ENDC}").strip().lower()
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Tutorial interrupted.{Colors.ENDC}")
            raise SystemExit(0)
        except EOFError:
            return 'continue'
        
        if choice in ['', 'c', 'continue']:
            return 'continue'
        elif choice in ['a', 'aql', '1']:
            open_aql_shell(container, namespace)
            if not skip_commands:
                show_suggested_commands(lesson_name)  # Show commands again after returning
        elif choice in ['s', 'asadm', '2']:
            open_asadm_shell(container)
            if not skip_commands:
                show_suggested_commands(lesson_name)  # Show commands again after returning
        elif choice in ['v', 'validate', '3']:
            return 'validate'
        elif choice in ['q', 'quit', 'exit']:
            print(f"{Colors.YELLOW}Exiting tutorial...{Colors.ENDC}")
            raise SystemExit(0)
        else:
            print(f"{Colors.RED}Invalid choice. Please enter a, s, v, q or just press Enter.{Colors.ENDC}")

