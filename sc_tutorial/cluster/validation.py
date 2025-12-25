"""Cluster health validation utilities."""

from ..ui.colors import Colors
from ..ui.display import print_success, print_error, print_warning, print_info, print_code
from .shell import detect_aerolab_container, run_asinfo_command


class ClusterValidator:
    """Handles cluster health validation."""
    
    def __init__(self, client, namespace):
        self.client = client
        self.namespace = namespace
    
    def verify_sc_enabled(self):
        """Check if the namespace has Strong Consistency enabled."""
        if not self.client:
            return False, "Not connected"
        
        try:
            import aerospike
            from aerospike import exception as ae_exception
            
            # Get namespace info
            info_cmd = f"namespace/{self.namespace}"
            response = self.client.info_all(info_cmd)
            
            for node, (err, result) in response.items():
                if err is None and result:
                    params = dict(item.split('=') for item in result.split(';') if '=' in item)
                    sc_enabled = params.get('strong-consistency', 'false') == 'true'
                    dead_partitions = int(params.get('dead_partitions', 0))
                    unavail_partitions = int(params.get('unavailable_partitions', 0))
                    ns_cluster_size = int(params.get('ns_cluster_size', 0))
                    
                    return sc_enabled, {
                        'strong_consistency': sc_enabled,
                        'dead_partitions': dead_partitions,
                        'unavailable_partitions': unavail_partitions,
                        'ns_cluster_size': ns_cluster_size,
                        'replication_factor': params.get('replication-factor', 'N/A')
                    }
            
            return False, "Could not get namespace info"
            
        except Exception as e:
            return False, str(e)
    
    def validate(self, compact=False):
        """Validate cluster health and help fix any issues.
        
        Args:
            compact: If True, show brief one-line status. If False, show full details.
        
        Returns:
            True if cluster is healthy, False otherwise.
        """
        import aerospike
        from aerospike import exception as ae_exception
        
        issues_found = False
        info = {}
        
        # Check 1: Connection
        if not self.client:
            if compact:
                print_error("❌ Not connected to cluster!")
            else:
                print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
                print(f"{Colors.CYAN}           CLUSTER HEALTH CHECK{Colors.ENDC}")
                print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}\n")
                print(f"{Colors.BOLD}1. Checking connection...{Colors.ENDC}")
                print_error("Not connected to cluster!")
            return False
        else:
            # Test connection with a simple operation
            try:
                self.client.get_nodes()
            except ae_exception.AerospikeError as e:
                if compact:
                    print_error(f"❌ Connection issue: {e}")
                else:
                    print_error(f"Connection issue: {e}")
                return False
        
        # Get SC status
        sc_enabled, info = self.verify_sc_enabled()
        
        # Check for issues
        if isinstance(info, dict):
            dead = info.get('dead_partitions', 0)
            unavail = info.get('unavailable_partitions', 0)
            if dead > 0 or unavail > 0 or not sc_enabled:
                issues_found = True
        else:
            issues_found = True
        
        if compact:
            # Show compact one-line status
            if issues_found:
                status_parts = []
                if not sc_enabled:
                    status_parts.append("SC disabled")
                if isinstance(info, dict):
                    if info.get('dead_partitions', 0) > 0:
                        status_parts.append(f"dead={info['dead_partitions']}")
                    if info.get('unavailable_partitions', 0) > 0:
                        status_parts.append(f"unavail={info['unavailable_partitions']}")
                print(f"\n{Colors.YELLOW}⚠ Cluster Status: {', '.join(status_parts)} [press 'v' for details]{Colors.ENDC}")
            else:
                rf = info.get('replication_factor', '?') if isinstance(info, dict) else '?'
                ns_size = info.get('ns_cluster_size', '?') if isinstance(info, dict) else '?'
                print(f"\n{Colors.GREEN}✓ Cluster OK: SC=enabled, RF={rf}, nodes={ns_size}, partitions=healthy{Colors.ENDC}")
            return not issues_found
        
        # Full detailed output
        print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.CYAN}           CLUSTER HEALTH CHECK{Colors.ENDC}")
        print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}\n")
        
        # Check 1: Connection
        print(f"{Colors.BOLD}1. Checking connection...{Colors.ENDC}")
        print_success("Connection OK")
        
        # Check 2: SC enabled
        print(f"\n{Colors.BOLD}2. Checking Strong Consistency status...{Colors.ENDC}")
        if sc_enabled:
            print_success(f"Strong Consistency: ENABLED")
            print(f"   ├── Replication Factor: {info.get('replication_factor', 'N/A')}")
            print(f"   └── NS Cluster Size: {info.get('ns_cluster_size', 'N/A')}")
        else:
            print_error("Strong Consistency: NOT ENABLED or namespace not found")
            print_info(f"Make sure namespace '{self.namespace}' has strong-consistency=true")
        
        # Check 3: Partitions
        print(f"\n{Colors.BOLD}3. Checking partition health...{Colors.ENDC}")
        if isinstance(info, dict):
            dead = info.get('dead_partitions', 0)
            unavail = info.get('unavailable_partitions', 0)
            
            if dead > 0:
                print_error(f"Dead partitions: {dead}")
                print_warning("Dead partitions indicate potential data loss!")
                print_info("To revive dead partitions (if acceptable):")
                print_code(f"asinfo -v 'revive:namespace={self.namespace}'")
            else:
                print_success("Dead partitions: 0")
            
            if unavail > 0:
                print_warning(f"Unavailable partitions: {unavail}")
                print_info("Some partitions are temporarily unavailable.")
                print_info("This usually resolves when all roster nodes rejoin.")
            else:
                print_success("Unavailable partitions: 0")
        
        # Check 4: Roster
        print(f"\n{Colors.BOLD}4. Checking roster configuration...{Colors.ENDC}")
        container = detect_aerolab_container()
        roster_ok = True
        if container:
            roster_info = run_asinfo_command(container, f"roster:namespace={self.namespace}")
            if 'roster=null' in roster_info or 'roster=' not in roster_info:
                print_warning("Roster may not be properly configured")
                print_info("To configure roster:")
                print_code(f"aerolab conf sc -n <cluster_name>")
                print_info("Or manually:")
                print_code(f"asadm> manage roster stage observed ns {self.namespace}")
                print_code("asadm> manage recluster")
                roster_ok = False
            else:
                print_success("Roster configured")
                # Parse and show roster summary
                if 'observed_nodes=' in roster_info:
                    parts = roster_info.split(':')
                    for part in parts:
                        if part.startswith('roster='):
                            roster_val = part.split('=')[1]
                            node_count = len(roster_val.split(',')) if roster_val and roster_val != 'null' else 0
                            print(f"   └── Roster nodes: {node_count}")
        else:
            print_warning("Could not detect AeroLab container for roster check")
        
        # Summary
        print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
        if issues_found or not roster_ok:
            print_warning("Issues found! Please address them before continuing.")
            print_info("You can open ASADM shell (option 's') to investigate further.")
        else:
            print_success("All checks passed! Cluster is healthy.")
        print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}\n")
        
        return not issues_found and roster_ok

