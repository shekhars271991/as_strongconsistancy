"""Shell interaction utilities for AQL and ASADM."""

import subprocess
from ..ui.colors import Colors
from ..ui.display import print_warning, print_info, print_code


def detect_aerolab_container():
    """Detect running AeroLab container name."""
    try:
        result = subprocess.run(
            ['docker', 'ps', '--format', '{{.Names}}'],
            capture_output=True, text=True, timeout=5
        )
        for name in result.stdout.strip().split('\n'):
            if name.startswith('aerolab-'):
                return name
    except Exception:
        pass
    return None


def open_aql_shell(container_name=None, namespace='test'):
    """Open an AQL shell for the user."""
    if container_name is None:
        container_name = detect_aerolab_container()
    
    if container_name:
        print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.CYAN}Opening AQL shell in container: {container_name}{Colors.ENDC}")
        print(f"{Colors.DIM}Type 'exit' or press Ctrl+D to return to tutorial{Colors.ENDC}")
        print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}\n")
        
        try:
            # Use -Uadmin with no password for default AeroLab setup
            subprocess.run(
                ['docker', 'exec', '-it', container_name, 'aql'],
                check=False
            )
        except KeyboardInterrupt:
            pass
        print(f"\n{Colors.GREEN}Returned to tutorial.{Colors.ENDC}")
    else:
        print_warning("No AeroLab container detected. Try manually:")
        print_code("docker exec -it <container_name> aql")
        print_info("List containers with: docker ps")


def open_asadm_shell(container_name=None):
    """Open an ASADM shell for the user."""
    if container_name is None:
        container_name = detect_aerolab_container()
    
    if container_name:
        print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.CYAN}Opening ASADM shell in container: {container_name}{Colors.ENDC}")
        print(f"{Colors.DIM}Type 'exit' or press Ctrl+D to return to tutorial{Colors.ENDC}")
        print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}\n")
        
        try:
            subprocess.run(
                ['docker', 'exec', '-it', container_name, 'asadm'],
                check=False
            )
        except KeyboardInterrupt:
            pass
        print(f"\n{Colors.GREEN}Returned to tutorial.{Colors.ENDC}")
    else:
        print_warning("No AeroLab container detected. Try manually:")
        print_code("docker exec -it <container_name> asadm")
        print_info("List containers with: docker ps")


def run_asinfo_command(container_name, command):
    """Run an asinfo command and return output."""
    if container_name is None:
        container_name = detect_aerolab_container()
    
    if container_name:
        try:
            result = subprocess.run(
                ['docker', 'exec', container_name, 'asinfo', '-v', command],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {e}"
    return "No container detected"

