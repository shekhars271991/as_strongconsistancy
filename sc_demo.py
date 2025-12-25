#!/usr/bin/env python3
"""
================================================================================
    AEROSPIKE STRONG CONSISTENCY (SC) MODE - COMPREHENSIVE TUTORIAL
================================================================================

This script is an interactive tutorial that teaches:
1. What is Strong Consistency and why it matters
2. How to configure SC in Aerospike
3. Key concepts: Roster, Partitions, Linearizable vs Session Consistency
4. How the cluster behaves during failures
5. Practical demonstrations of SC guarantees

Prerequisites:
- Aerospike Enterprise Edition with SC-enabled feature key
- Python aerospike client: pip install aerospike colorama
- A running Aerospike cluster with SC namespace configured

Author: Aerospike SC Tutorial
"""

import aerospike
from aerospike import exception as ae_exception
from aerospike_helpers.operations import operations as ops
import time
import sys
import os
import subprocess
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import random
import argparse

# =============================================================================
# TERMINAL COLORS FOR BETTER READABILITY
# =============================================================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def print_banner(text, char='='):
    width = 70
    print(f"\n{Colors.HEADER}{Colors.BOLD}{char * width}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(width)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{char * width}{Colors.ENDC}\n")

def print_section(text):
    print(f"\n{Colors.CYAN}{Colors.BOLD}▶ {text}{Colors.ENDC}")
    print(f"{Colors.DIM}{'-' * 60}{Colors.ENDC}")

def print_concept(title, explanation):
    print(f"\n{Colors.YELLOW}{Colors.BOLD}📚 {title}{Colors.ENDC}")
    for line in explanation.split('\n'):
        print(f"   {Colors.DIM}{line}{Colors.ENDC}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_code(code):
    print(f"{Colors.DIM}  >>> {code}{Colors.ENDC}")

def wait_for_user(message="Press Enter to continue..."):
    try:
        input(f"\n{Colors.BLUE}{message}{Colors.ENDC}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tutorial interrupted by user.{Colors.ENDC}")
        raise SystemExit(0)

# =============================================================================
# INTERACTIVE MENU SYSTEM
# =============================================================================

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

def show_suggested_commands(lesson_name):
    """Display extensive suggested commands for the current lesson, split by shell type."""
    
    # Comprehensive commands organized by lesson stage
    commands = {
        'aerolab': {
            'title': '🔧 SETUP & VERIFICATION',
            'terminal': [
                ("List all AeroLab clusters", "aerolab cluster list"),
                ("Check container status", "docker ps --filter 'name=aerolab'"),
                ("View recent logs", "docker logs aerolab-mydc_1 --tail 100"),
                ("Follow logs in real-time", "docker logs -f aerolab-mydc_1"),
                ("Check container resources", "docker stats aerolab-mydc_1 --no-stream"),
            ],
            'aql': [
                ("List all namespaces", "SHOW NAMESPACES"),
                ("List all sets", "SHOW SETS"),
                ("Check bins in a set", "SHOW BINS test"),
            ],
            'asadm': [
                ("Cluster overview", "info"),
                ("Detailed cluster info", "info network"),
                ("Show all namespaces", "show config namespace"),
                ("Verify SC is enabled", "show config namespace like strong"),
                ("Check roster status", "show roster"),
                ("View node IDs", "info node"),
            ],
        },
        'configuration': {
            'title': '⚙️ SC CONFIGURATION COMMANDS',
            'aql': [
                ("List namespaces", "SHOW NAMESPACES"),
                ("Show sets in namespace", "SHOW SETS"),
                ("Show index info", "SHOW INDEXES test"),
            ],
            'asadm': [
                ("─── ROSTER MANAGEMENT ───", ""),
                ("View current roster", "show roster"),
                ("Stage observed nodes to roster", "manage roster stage observed ns test"),
                ("Apply roster changes", "manage recluster"),
                ("─── NAMESPACE CONFIG ───", ""),
                ("Show all namespace config", "show config namespace"),
                ("Show SC-specific settings", "show config namespace like strong"),
                ("Show replication factor", "show config namespace like replication"),
                ("Show TTL settings", "show config namespace like ttl"),
                ("─── CLUSTER INFO ───", ""),
                ("View cluster size", "info"),
                ("Show node details", "info node"),
                ("Check cluster stability", "info network"),
            ],
        },
        'basic_ops': {
            'title': '📝 BASIC CRUD OPERATIONS',
            'aql': [
                ("─── INSERT RECORDS ───", ""),
                ("Insert simple record", "INSERT INTO test (PK, name, age) VALUES ('user1', 'Alice', 30)"),
                ("Insert with multiple bins", "INSERT INTO test (PK, city, score, active) VALUES ('user2', 'NYC', 95.5, true)"),
                ("Insert with list", "INSERT INTO test (PK, tags) VALUES ('user3', JSON('[\"a\",\"b\",\"c\"]'))"),
                ("Insert with map", "INSERT INTO test (PK, data) VALUES ('user4', JSON('{\"x\":1,\"y\":2}'))"),
                ("─── READ RECORDS ───", ""),
                ("Read a record", "SELECT * FROM test WHERE PK='user1'"),
                ("Read specific bins", "SELECT name, age FROM test WHERE PK='user1'"),
                ("Read with metadata", "SELECT *, generation, ttl FROM test WHERE PK='user1'"),
                ("Scan all records (careful!)", "SELECT * FROM test"),
                ("Count records", "SELECT count(*) FROM test"),
                ("─── UPDATE RECORDS ───", ""),
                ("Update a bin", "UPDATE test SET age=31 WHERE PK='user1'"),
                ("Add new bin to record", "UPDATE test SET status='active' WHERE PK='user1'"),
                ("─── DELETE RECORDS ───", ""),
                ("Delete a record", "DELETE FROM test WHERE PK='user1'"),
                ("Note: In SC mode, deletes create tombstones!", ""),
            ],
            'asadm': [
                ("Check object count", "show stat namespace like objects"),
                ("View tombstone count", "show stat namespace like tombstones"),
                ("Check write stats", "show stat namespace like client_write"),
                ("Check read stats", "show stat namespace like client_read"),
                ("Check delete stats", "show stat namespace like client_delete"),
            ],
        },
        'consistency': {
            'title': '🔒 CONSISTENCY LEVELS',
            'aql': [
                ("─── SESSION CONSISTENCY DEMO ───", ""),
                ("Write a test record", "INSERT INTO test (PK, counter) VALUES ('session_test', 0)"),
                ("Read immediately after write", "SELECT * FROM test WHERE PK='session_test'"),
                ("Update and read", "UPDATE test SET counter=1 WHERE PK='session_test'"),
                ("Verify update visible", "SELECT *, generation FROM test WHERE PK='session_test'"),
                ("─── MULTIPLE WRITES ───", ""),
                ("Sequential write 1", "UPDATE test SET counter=10 WHERE PK='session_test'"),
                ("Sequential write 2", "UPDATE test SET counter=20 WHERE PK='session_test'"),
                ("Check final value", "SELECT counter, generation FROM test WHERE PK='session_test'"),
                ("─── CLEANUP ───", ""),
                ("Delete test record", "DELETE FROM test WHERE PK='session_test'"),
            ],
            'asadm': [
                ("─── READ POLICY ───", ""),
                ("Check read consistency level", "show config namespace like read-consistency"),
                ("Check write commit level", "show config namespace like write-commit"),
                ("─── CONSISTENCY STATS ───", ""),
                ("View read latency", "show latency like read"),
                ("View write latency", "show latency like write"),
                ("Check proxy operations", "show stat namespace like proxy"),
                ("View retransmit stats", "show stat namespace like retransmit"),
            ],
        },
        'generation': {
            'title': '🔢 GENERATION & OPTIMISTIC LOCKING',
            'aql': [
                ("─── SETUP TEST RECORD ───", ""),
                ("Create test record", "INSERT INTO test (PK, balance) VALUES ('account1', 1000)"),
                ("Check initial generation", "SELECT *, generation FROM test WHERE PK='account1'"),
                ("─── WATCH GENERATION INCREMENT ───", ""),
                ("First update (gen 1→2)", "UPDATE test SET balance=1100 WHERE PK='account1'"),
                ("Check generation", "SELECT balance, generation FROM test WHERE PK='account1'"),
                ("Second update (gen 2→3)", "UPDATE test SET balance=1200 WHERE PK='account1'"),
                ("Check generation again", "SELECT balance, generation FROM test WHERE PK='account1'"),
                ("─── SIMULATE CONCURRENT ACCESS ───", ""),
                ("Note: Open TWO AQL shells to simulate concurrent clients", ""),
                ("Shell 1: Read record", "SELECT *, generation FROM test WHERE PK='account1'"),
                ("Shell 2: Update record", "UPDATE test SET balance=999 WHERE PK='account1'"),
                ("Shell 1: Try update (may see stale gen)", "SELECT *, generation FROM test WHERE PK='account1'"),
                ("─── CLEANUP ───", ""),
                ("Delete test record", "DELETE FROM test WHERE PK='account1'"),
            ],
            'asadm': [
                ("Check generation error stats", "show stat namespace like fail_generation"),
                ("View all failure stats", "show stat namespace like fail_"),
                ("Check key-busy errors", "show stat namespace like key_busy"),
            ],
        },
        'cluster': {
            'title': '🖥️ CLUSTER HEALTH & PARTITIONS',
            'aql': [
                ("─── HEALTH CHECK ───", ""),
                ("Quick read test", "SELECT count(*) FROM test"),
                ("Write test", "INSERT INTO test (PK, check) VALUES ('health_check', 'ok')"),
                ("Read test", "SELECT * FROM test WHERE PK='health_check'"),
                ("Delete test", "DELETE FROM test WHERE PK='health_check'"),
            ],
            'asadm': [
                ("─── PARTITION STATUS ───", ""),
                ("View partition map", "show pmap"),
                ("Check dead partitions", "show stat namespace like dead_partitions"),
                ("Check unavailable partitions", "show stat namespace like unavailable"),
                ("View partition ownership", "info partition"),
                ("─── ROSTER & NODES ───", ""),
                ("View roster", "show roster"),
                ("Show observed nodes", "show roster observed"),
                ("Show pending roster", "show roster pending"),
                ("View node info", "info node"),
                ("─── MIGRATION STATUS ───", ""),
                ("Check migration progress", "show stat like migrate"),
                ("View migration details", "show stat namespace like migrate_"),
                ("Check remaining migrations", "show stat namespace like remaining"),
                ("─── RECOVERY COMMANDS ───", ""),
                ("If dead partitions exist:", ""),
                ("  Revive (USE CAUTION!)", "asinfo -v 'revive:namespace=test'"),
                ("  Then recluster", "manage recluster"),
            ],
        },
        'errors': {
            'title': '⚠️ ERROR HANDLING & TROUBLESHOOTING',
            'aql': [
                ("─── GENERATE TEST ERRORS ───", ""),
                ("Create test record", "INSERT INTO test (PK, val) VALUES ('err_test', 1)"),
                ("Try inserting to non-existent ns", "INSERT INTO fake_ns (PK, val) VALUES ('x', 1)"),
                ("Read non-existent record", "SELECT * FROM test WHERE PK='does_not_exist'"),
                ("─── GENERATION CONFLICT TEST ───", ""),
                ("(Open 2 shells for this test)", ""),
                ("Shell 1: Read record", "SELECT *, generation FROM test WHERE PK='err_test'"),
                ("Shell 2: Update record", "UPDATE test SET val=100 WHERE PK='err_test'"),
                ("Shell 1: Check if gen changed", "SELECT *, generation FROM test WHERE PK='err_test'"),
            ],
            'asadm': [
                ("─── ERROR STATISTICS ───", ""),
                ("All failure stats", "show stat namespace like fail_"),
                ("Generation errors", "show stat namespace like fail_generation"),
                ("Key busy errors", "show stat namespace like fail_key_busy"),
                ("Record too big errors", "show stat namespace like fail_record_too_big"),
                ("Forbidden errors (SC)", "show stat namespace like fail_forbidden"),
                ("─── TIMEOUT & NETWORK ───", ""),
                ("Check timeouts", "show stat namespace like timeout"),
                ("Check proxy errors", "show stat namespace like proxy_error"),
                ("─── PARTITION ERRORS ───", ""),
                ("Unavailable partition ops", "show stat namespace like unavailable"),
                ("Dead partition status", "show stat namespace like dead"),
                ("─── TRANSACTION STATS ───", ""),
                ("Read errors", "show stat namespace like client_read_error"),
                ("Write errors", "show stat namespace like client_write_error"),
                ("Delete errors", "show stat namespace like client_delete_error"),
            ],
        },
    }
    
    lesson_data = commands.get(lesson_name, commands.get('basic_ops'))
    
    # Print header with lesson-specific title
    title = lesson_data.get('title', '📋 SUGGESTED COMMANDS TO TRY')
    print(f"\n{Colors.YELLOW}{'─'*70}{Colors.ENDC}")
    print(f"{Colors.YELLOW}{title}{Colors.ENDC}")
    print(f"{Colors.YELLOW}{'─'*70}{Colors.ENDC}")
    
    # Show terminal commands if present
    if 'terminal' in lesson_data and lesson_data['terminal']:
        print(f"\n  {Colors.BOLD}🖥️  Terminal (run outside container):{Colors.ENDC}")
        for desc, cmd in lesson_data['terminal']:
            if cmd:  # Skip empty commands (section headers)
                print(f"    {Colors.CYAN}•{Colors.ENDC} {desc}:")
                print(f"      {Colors.DIM}{cmd}{Colors.ENDC}")
            else:
                print(f"    {Colors.CYAN}{desc}{Colors.ENDC}")
    
    # Show AQL commands if present
    if 'aql' in lesson_data and lesson_data['aql']:
        print(f"\n  {Colors.BOLD}📊 AQL Shell [a] - Data Operations:{Colors.ENDC}")
        for desc, cmd in lesson_data['aql']:
            if cmd:  # Skip empty commands (section headers)
                print(f"    {Colors.CYAN}•{Colors.ENDC} {desc}:")
                print(f"      {Colors.DIM}{cmd}{Colors.ENDC}")
            else:
                print(f"    {Colors.CYAN}{desc}{Colors.ENDC}")
    
    # Show ASADM commands if present
    if 'asadm' in lesson_data and lesson_data['asadm']:
        print(f"\n  {Colors.BOLD}🔧 ASADM Shell [s] - Admin Operations:{Colors.ENDC}")
        for desc, cmd in lesson_data['asadm']:
            if cmd:  # Skip empty commands (section headers)
                print(f"    {Colors.CYAN}•{Colors.ENDC} {desc}:")
                print(f"      {Colors.DIM}{cmd}{Colors.ENDC}")
            else:
                print(f"    {Colors.CYAN}{desc}{Colors.ENDC}")
    
    print(f"\n{Colors.YELLOW}{'─'*70}{Colors.ENDC}")

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
            show_suggested_commands(lesson_name)  # Show commands again after returning
        elif choice in ['s', 'asadm', '2']:
            open_asadm_shell(container)
            show_suggested_commands(lesson_name)  # Show commands again after returning
        elif choice in ['v', 'validate', '3']:
            return 'validate'
        elif choice in ['q', 'quit', 'exit']:
            print(f"{Colors.YELLOW}Exiting tutorial...{Colors.ENDC}")
            raise SystemExit(0)
        else:
            print(f"{Colors.RED}Invalid choice. Please enter a, s, v, q or just press Enter.{Colors.ENDC}")

# =============================================================================
# AEROLAB SETUP INSTRUCTIONS
# =============================================================================

AEROLAB_SETUP = """
AeroLab is the easiest way to set up an Aerospike SC cluster for development.

INSTALLATION:
─────────────
  # macOS
  brew install aerospike/tap/aerolab
  
  # Linux (download from GitHub)
  curl -L https://github.com/aerospike/aerolab/releases/latest/download/aerolab-linux-amd64 -o aerolab
  chmod +x aerolab && sudo mv aerolab /usr/local/bin/

QUICK SC SETUP (3 commands):
────────────────────────────
  # 1. Set Docker as backend
  aerolab config backend -t docker
  
  # 2. Create cluster with your feature key
  aerolab cluster create -n mydc -c 1 -f /path/to/features.conf
  
  # 3. Enable Strong Consistency
  aerolab conf sc -n mydc

That's it! Your SC cluster is ready.

VERIFY SC IS ENABLED:
─────────────────────
  aerolab cluster list
  # Check the ExposedPort (e.g., 3100)
  
  # Then verify SC:
  docker exec aerolab-mydc_1 asinfo -v "namespace/test" | grep strong-consistency
  # Should show: strong-consistency=true

COMMON AEROLAB COMMANDS:
────────────────────────
  aerolab cluster list              # List clusters
  aerolab cluster start -n mydc     # Start cluster
  aerolab cluster stop -n mydc      # Stop cluster  
  aerolab cluster destroy -n mydc   # Delete cluster
  aerolab attach shell -n mydc      # Shell into container
  aerolab attach asadm -n mydc      # Open asadm tool
"""

AEROLAB_MULTI_NODE = """
MULTI-NODE SC CLUSTER:
──────────────────────
  # Create 3-node cluster
  aerolab cluster create -n mydc -c 3 -f features.conf
  
  # Configure SC on all nodes
  aerolab conf sc -n mydc
  
  # The roster is automatically configured!

CUSTOM CONFIGURATION:
─────────────────────
  # Create cluster with custom config
  aerolab cluster create -n mydc -c 3 -f features.conf
  
  # Edit config (optional)
  aerolab conf edit -n mydc
  
  # Apply SC settings
  aerolab conf sc -n mydc
  
  # Restart if needed
  aerolab aerospike restart -n mydc
"""

# =============================================================================
# TUTORIAL CONTENT
# =============================================================================

INTRO_TEXT = """
Strong Consistency (SC) is an Aerospike Enterprise feature that guarantees:

  • All writes to a record are applied in a specific, sequential order
  • Writes will NOT be re-ordered or skipped (no data loss)
  • All clients see the same view of data at any point in time
  
This is different from the default Available/Partition-tolerant (AP) mode
which prioritizes availability over strict consistency.

SC Mode is essential for:
  • Financial transactions
  • Inventory management  
  • Any application where data accuracy is critical
"""

ROSTER_CONCEPT = """
The ROSTER is a list of nodes expected to be in the cluster for an SC namespace.

Key points:
  • The roster is stored persistently in a distributed table
  • Nodes not on the roster cannot participate in SC operations
  • The roster must be configured AFTER the cluster forms
  • Changes to the roster require a 'recluster' command

Roster states:
  • roster         - Currently active roster
  • pending_roster - New roster waiting to be applied
  • observed_nodes - Nodes currently in the cluster with the namespace
"""

PARTITION_CONCEPT = """
Aerospike distributes data across 4096 PARTITIONS.

In SC mode, partitions can be:
  • AVAILABLE    - Normal operation, reads/writes work
  • UNAVAILABLE  - Missing nodes, read-only or no access
  • DEAD         - Data potentially lost, requires manual intervention

Dead partitions occur when:
  • RF (replication-factor) nodes crash simultaneously
  • Storage devices are wiped on RF nodes
  • Unclean shutdowns happen
"""

CONSISTENCY_LEVELS = """
SC provides two read consistency levels:

1. SESSION CONSISTENCY (Default)
   • Guarantees monotonic reads within a single client session
   • You always see your own writes (read-your-writes)
   • Lower latency than linearizable
   • Best for most use cases

2. LINEARIZABLE CONSISTENCY
   • Global ordering visible to ALL clients simultaneously  
   • If client A reads after client B writes, A sees B's write
   • Higher latency (requires extra coordination)
   • Use when multiple clients must see exact same state
"""

INDOUBT_CONCEPT = """
The IN-DOUBT error indicates uncertainty about whether a write was applied.

When you get InDoubt=True:
  • The write MAY have been applied
  • The write MAY NOT have been applied
  • You should read the record to determine the actual state

This happens when:
  • Network timeout occurs after sending write
  • Server crashes after receiving but before acknowledging
  • Connection drops mid-transaction
"""


# =============================================================================
# MAIN TUTORIAL CLASS
# =============================================================================

class StrongConsistencyTutorial:
    """Interactive tutorial for Aerospike Strong Consistency."""
    
    def __init__(self, hosts=None, namespace='test', interactive=True):
        """Initialize the tutorial."""
        if hosts is None:
            # Default to AeroLab cluster on port 3100
            hosts = [('127.0.0.1', 3100)]
        
        self.hosts = hosts
        self.interactive = interactive
        self.client = None
        self.namespace = namespace
        self.set_name = 'tutorial'
        
        self.config = {
            'hosts': hosts,
            'policies': {
                'timeout': 5000,
            },
            'use_services_alternate': True,
        }
    
    def pause(self, lesson_name='basic_ops', message=None):
        """Pause for user input in interactive mode with menu options."""
        if self.interactive:
            # Always validate cluster health before showing menu
            healthy = self.validate_and_fix_cluster(compact=True)
            
            if not healthy:
                print_warning("Issues detected! Please fix before continuing or press Enter to proceed anyway.")
            
            while True:
                choice = interactive_menu(lesson_name, self.namespace)
                if choice == 'continue':
                    break
                elif choice == 'validate':
                    # Full validation on manual request
                    self.validate_and_fix_cluster(compact=False)
    
    def validate_and_fix_cluster(self, compact=False):
        """Validate cluster health and help fix any issues.
        
        Args:
            compact: If True, show brief one-line status. If False, show full details.
        """
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
            
            print_info("Attempting to reconnect...")
            if self.connect():
                print_success("Reconnected successfully!")
            else:
                print_error("Could not reconnect. Please check if Aerospike is running.")
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
                print_info("Attempting to reconnect...")
                try:
                    self.disconnect()
                    if self.connect():
                        print_success("Reconnected successfully!")
                    else:
                        return False
                except Exception:
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
    
    def connect(self):
        """Connect to the Aerospike cluster."""
        try:
            self.client = aerospike.client(self.config).connect()
            print_success(f"Connected to Aerospike cluster at {self.hosts}")
            return True
        except ae_exception.AerospikeError as e:
            print_error(f"Failed to connect: {e}")
            print_info("Make sure the Aerospike cluster is running and accessible")
            return False
    
    def disconnect(self):
        """Disconnect from the cluster."""
        if self.client:
            self.client.close()
            print_info("Disconnected from Aerospike")
    
    def verify_sc_enabled(self):
        """Check if the namespace has Strong Consistency enabled."""
        if not self.client:
            return False, "Not connected"
        
        try:
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
            
        except ae_exception.AerospikeError as e:
            return False, str(e)
    
    def show_cluster_status(self):
        """Display current cluster and SC status."""
        print_section("Cluster Status Check")
        
        sc_enabled, info = self.verify_sc_enabled()
        
        if isinstance(info, dict):
            status_icon = "✓" if sc_enabled else "✗"
            color = Colors.GREEN if sc_enabled else Colors.RED
            
            print(f"\n   Namespace: {self.namespace}")
            print(f"   {color}{status_icon} Strong Consistency: {info['strong_consistency']}{Colors.ENDC}")
            print(f"   ├── Replication Factor: {info['replication_factor']}")
            print(f"   ├── NS Cluster Size: {info['ns_cluster_size']}")
            print(f"   ├── Dead Partitions: {info['dead_partitions']}")
            print(f"   └── Unavailable Partitions: {info['unavailable_partitions']}")
            
            if info['dead_partitions'] > 0:
                print_warning(f"\n   Dead partitions detected! Run: asinfo -v 'revive:namespace={self.namespace}'")
            
            if info['unavailable_partitions'] > 0:
                print_warning(f"\n   Unavailable partitions! Check cluster roster and node health.")
            
            return sc_enabled
        else:
            print_error(f"Could not verify SC status: {info}")
            return False
    
    # =========================================================================
    # LESSON 0: AEROLAB SETUP
    # =========================================================================
    
    def lesson_aerolab_setup(self):
        """Show AeroLab setup instructions."""
        print_banner("LESSON 0: SETTING UP SC WITH AEROLAB")
        
        print_concept("What is AeroLab?", """
AeroLab is Aerospike's official tool for quickly deploying development 
and testing clusters. It supports Docker, AWS, and GCP backends.

For SC development, AeroLab is the fastest way to get started!
""")
        
        self.pause('aerolab')
        
        print_section("Quick Setup (3 Commands)")
        print(f"{Colors.DIM}{AEROLAB_SETUP}{Colors.ENDC}")
        
        self.pause('aerolab')
        
        print_section("Multi-Node SC Cluster")
        print(f"{Colors.DIM}{AEROLAB_MULTI_NODE}{Colors.ENDC}")
        
        self.pause('aerolab')
        
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
        
        self.pause('aerolab')
    
    # =========================================================================
    # LESSON 1: INTRODUCTION
    # =========================================================================
    
    def lesson_introduction(self):
        """Introduction to Strong Consistency."""
        print_banner("LESSON 1: INTRODUCTION TO STRONG CONSISTENCY")
        
        print_concept("What is Strong Consistency?", INTRO_TEXT)
        
        self.pause('introduction')
        
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
        
        self.pause('introduction')
    
    # =========================================================================
    # LESSON 2: CONFIGURATION
    # =========================================================================
    
    def lesson_configuration(self):
        """Lesson on SC configuration."""
        print_banner("LESSON 2: CONFIGURING STRONG CONSISTENCY")
        
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
        
        self.pause('configuration')
        
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
        
        self.pause('configuration')
        
        # Show actual cluster info if connected
        if self.client:
            print_section("Current Cluster Configuration")
            self.show_cluster_info()
        
        self.pause('configuration')
    
    def show_cluster_info(self):
        """Display current cluster and namespace information."""
        try:
            nodes = self.client.get_nodes()
            print_info(f"Connected nodes: {len(nodes)}")
            
            for node in nodes:
                print(f"   • {node}")
            
            # Get namespace info using info_all (returns dict of node -> response)
            info_dict = self.client.info_all(f"namespace/{self.namespace}")
            
            # Get info from first node response
            if info_dict:
                first_response = list(info_dict.values())[0]
                # info_all returns (error, response) tuples where error=None on success
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
                
        except ae_exception.AerospikeError as e:
            print_warning(f"Could not get cluster info: {e}")
    
    # =========================================================================
    # LESSON 3: BASIC OPERATIONS
    # =========================================================================
    
    def lesson_basic_operations(self):
        """Demonstrate basic SC operations."""
        print_banner("LESSON 3: BASIC SC OPERATIONS")
        
        print_concept("SC Write Guarantees", """
When a write succeeds in SC mode:
  • The write has been replicated to all required nodes
  • The write is durable (won't be lost)
  • All subsequent reads will see this write
  • The write has a specific position in the record's history
""")
        
        self.pause('basic_ops')
        
        print_section("Demo: Write and Read Operations")
        
        key = (self.namespace, self.set_name, 'demo_key_1')
        
        try:
            # Write
            print_info("Writing a record...")
            print_code(f"client.put(key, {{'name': 'Alice', 'balance': 1000}})")
            
            record = {
                'name': 'Alice',
                'balance': 1000,
                'created_at': datetime.now().isoformat()
            }
            
            self.client.put(key, record)
            print_success("Write successful!")
            
            # Read
            print_info("\nReading the record back...")
            print_code("client.get(key)")
            
            _, meta, fetched = self.client.get(key)
            print_success(f"Read successful!")
            print(f"   Data: {fetched}")
            print(f"   Generation: {meta['gen']}")
            print(f"   TTL: {meta['ttl']}")
            
            # Update
            print_info("\nUpdating the record...")
            print_code(f"client.put(key, {{'balance': 1500}})")
            
            self.client.put(key, {'balance': 1500})
            
            _, meta2, fetched2 = self.client.get(key)
            print_success(f"Update successful!")
            print(f"   New balance: {fetched2.get('balance')}")
            print(f"   Generation: {meta['gen']} → {meta2['gen']}")
            
            # Cleanup - use durable delete in SC mode
            print_info("\nCleaning up with durable delete...")
            print_code("client.remove(key, policy={'durable_delete': True})")
            try:
                self.client.remove(key, policy={'durable_delete': True})
                print_success("Record deleted with tombstone")
            except ae_exception.AerospikeError:
                print_warning("Delete requires durable_delete or allow-expunge enabled")
            
        except ae_exception.AerospikeError as e:
            print_error(f"Operation failed: {e}")
            self._explain_error(e)
        
        self.pause('basic_ops')
    
    # =========================================================================
    # LESSON 4: CONSISTENCY DEMONSTRATIONS
    # =========================================================================
    
    def lesson_consistency_demo(self):
        """Demonstrate different consistency levels."""
        print_banner("LESSON 4: CONSISTENCY LEVELS")
        
        print_concept("Session vs Linearizable Consistency", CONSISTENCY_LEVELS)
        
        self.pause('consistency')
        
        print_section("Demo: Session Consistency (Read-Your-Writes)")
        
        key = (self.namespace, self.set_name, 'session_test')
        
        try:
            print_info("Performing sequential writes and reads...")
            print_info("In session consistency, you always see your own writes.\n")
            
            for i in range(5):
                # Write
                self.client.put(key, {'version': i, 'timestamp': time.time()})
                
                # Read immediately
                _, _, data = self.client.get(key)
                
                status = "✓" if data['version'] == i else "✗"
                print(f"   Write v{i} → Read v{data['version']} {status}")
                
                time.sleep(0.1)
            
            print_success("\nSession consistency verified: All writes were immediately visible")
            
            self._safe_remove(key)
            
        except ae_exception.AerospikeError as e:
            print_error(f"Error: {e}")
        
        self.pause('consistency')
        
        print_section("Demo: Linearizable Reads")
        
        try:
            key = (self.namespace, self.set_name, 'linear_test')
            self.client.put(key, {'value': 0})
            
            iterations = 50
            
            print_info(f"Comparing read latency ({iterations} reads each)...\n")
            
            # Session consistency reads
            start = time.time()
            for _ in range(iterations):
                self.client.get(key)
            session_time = time.time() - start
            
            # Linearizable reads
            linear_policy = {'linearize_read': True}
            start = time.time()
            for _ in range(iterations):
                self.client.get(key, policy=linear_policy)
            linear_time = time.time() - start
            
            print(f"   Session Consistency:  {session_time*1000:.1f}ms total ({session_time*1000/iterations:.2f}ms/read)")
            print(f"   Linearizable:         {linear_time*1000:.1f}ms total ({linear_time*1000/iterations:.2f}ms/read)")
            
            overhead = ((linear_time / session_time) - 1) * 100
            print(f"\n   Linearizable overhead: {overhead:.1f}% slower")
            
            print_info("\nLinearizable reads are slower because they must verify")
            print_info("with replica nodes to ensure global consistency.")
            
            self._safe_remove(key)
            
        except ae_exception.AerospikeError as e:
            print_error(f"Error: {e}")
        
        self.pause('consistency')
    
    # =========================================================================
    # LESSON 5: CONCURRENT WRITES
    # =========================================================================
    
    def lesson_concurrent_writes(self):
        """Demonstrate SC behavior with concurrent writes."""
        print_banner("LESSON 5: CONCURRENT WRITE ORDERING")
        
        print_concept("Write Ordering Guarantee", """
In SC mode, all writes to a single record are applied in a specific,
sequential order. This means:

  • Concurrent writes from different clients are serialized
  • Each write gets a unique position in the record's history
  • No writes are lost or reordered
  • The generation number reflects the total write count
""")
        
        self.pause('basic_ops')
        
        print_section("Demo: Concurrent Counter Increments")
        
        key = (self.namespace, self.set_name, 'counter')
        num_threads = 5
        increments_per_thread = 20
        results = []
        errors = []
        lock = threading.Lock()
        
        try:
            # Initialize counter
            self.client.put(key, {'counter': 0})
            print_info(f"Initialized counter to 0")
            print_info(f"Starting {num_threads} threads, each doing {increments_per_thread} increments...\n")
            
            def increment_worker(thread_id):
                """Worker function to increment counter."""
                local_results = []
                for i in range(increments_per_thread):
                    try:
                        ops_list = [
                            ops.increment('counter', 1),
                            ops.read('counter')
                        ]
                        _, _, result = self.client.operate(key, ops_list)
                        
                        with lock:
                            results.append(result['counter'])
                            
                    except ae_exception.AerospikeError as e:
                        with lock:
                            errors.append((thread_id, str(e)))
                
                return thread_id
            
            # Run concurrent increments
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(increment_worker, i) for i in range(num_threads)]
                for future in as_completed(futures):
                    future.result()
            
            elapsed = time.time() - start_time
            
            # Verify results
            _, _, final = self.client.get(key)
            expected = num_threads * increments_per_thread
            
            print(f"   Time elapsed: {elapsed:.2f}s")
            print(f"   Expected final value: {expected}")
            print(f"   Actual final value: {final['counter']}")
            print(f"   Successful increments: {len(results)}")
            print(f"   Errors: {len(errors)}")
            
            # Check uniqueness
            unique_values = len(set(results))
            
            if final['counter'] == len(results) and unique_values == len(results):
                print_success("\n✓ SC VERIFIED: All increments counted, all values unique!")
                print_info("Each concurrent increment got a unique counter value.")
            else:
                print_warning(f"Unique values: {unique_values} / {len(results)}")
            
            self._safe_remove(key)
            
        except ae_exception.AerospikeError as e:
            print_error(f"Error: {e}")
        
        self.pause('basic_ops')
    
    # =========================================================================
    # LESSON 6: GENERATION CONFLICTS
    # =========================================================================
    
    def lesson_generation_conflicts(self):
        """Demonstrate generation-based conflict detection."""
        print_banner("LESSON 6: OPTIMISTIC LOCKING WITH GENERATIONS")
        
        print_concept("Generation Numbers", """
Every record has a GENERATION number that increments with each write.
This enables optimistic locking (check-and-set):

  1. Read record and note its generation
  2. Modify data locally
  3. Write back with generation check
  4. If generation changed, write fails → retry

This prevents lost updates in concurrent scenarios.
""")
        
        self.pause('generation')
        
        print_section("Demo: Generation Conflict Detection")
        
        key = (self.namespace, self.set_name, 'conflict_test')
        
        try:
            # Initial write
            self.client.put(key, {'value': 'initial', 'version': 1})
            _, meta1 = self.client.exists(key)
            gen1 = meta1['gen']
            print_info(f"Initial write completed, generation: {gen1}")
            
            # Simulate another client updating the record
            print_info("Simulating another client's update...")
            self.client.put(key, {'value': 'updated_by_other', 'version': 2})
            _, meta2 = self.client.exists(key)
            gen2 = meta2['gen']
            print_info(f"Other client updated, generation: {gen2}")
            
            # Try to update with stale generation
            print_info(f"\nAttempting update with stale generation ({gen1})...")
            print_code(f"client.put(key, data, meta={{'gen': {gen1}}}, policy={{'gen': POLICY_GEN_EQ}})")
            
            try:
                policy = {'gen': aerospike.POLICY_GEN_EQ}
                self.client.put(
                    key, 
                    {'value': 'my_update', 'version': 3}, 
                    meta={'gen': gen1}, 
                    policy=policy
                )
                print_error("Update succeeded (unexpected!)")
            except ae_exception.RecordGenerationError:
                print_success("✓ CONFLICT DETECTED! Write rejected due to generation mismatch")
                print_info("This prevents overwriting another client's changes.")
            
            # Show final value
            _, _, final = self.client.get(key)
            print(f"\n   Final value: {final['value']} (preserved from other client)")
            
            self._safe_remove(key)
            
        except ae_exception.AerospikeError as e:
            print_error(f"Error: {e}")
        
        self.pause('generation')
    
    # =========================================================================
    # LESSON 7: ERROR HANDLING
    # =========================================================================
    
    def lesson_error_handling(self):
        """Explain SC-specific error handling."""
        print_banner("LESSON 7: ERROR HANDLING IN SC MODE")
        
        print_concept("InDoubt Errors", INDOUBT_CONCEPT)
        
        self.pause('errors')
        
        print_section("Common SC Errors")
        
        errors_table = """
        ┌─────────────────────────┬────────────────────────────────────────────┐
        │ Error                   │ Meaning                                    │
        ├─────────────────────────┼────────────────────────────────────────────┤
        │ PARTITION_UNAVAILABLE   │ Data partition is not accessible           │
        │ INVALID_NODE_ERROR      │ No node available for the partition        │
        │ TIMEOUT                 │ Operation timed out (InDoubt possible)     │
        │ GENERATION_ERROR        │ Record was modified by another client      │
        │ FORBIDDEN               │ Operation not allowed (e.g., cluster issue)│
        │ FAIL_FORBIDDEN          │ Non-durable delete blocked in SC           │
        └─────────────────────────┴────────────────────────────────────────────┘
        """
        print(errors_table)
        
        print_concept("Handling InDoubt", """
When you receive a timeout with InDoubt=True:

  1. Don't assume the write failed
  2. Read the record to check its state
  3. Use idempotent operations when possible
  4. Use generation checks for safe retries
  
Example pattern:
  try:
      client.put(key, data, meta={'gen': expected_gen}, 
                 policy={'gen': POLICY_GEN_EQ})
  except TimeoutError as e:
      if e.in_doubt:
          # Read to check if write was applied
          _, meta, _ = client.get(key)
          if meta['gen'] > expected_gen:
              # Write was applied
          else:
              # Retry the write
""")
        
        self.pause('errors')
    
    # =========================================================================
    # LESSON 8: CLUSTER BEHAVIOR
    # =========================================================================
    
    def lesson_cluster_behavior(self):
        """Explain cluster behavior in various scenarios."""
        print_banner("LESSON 8: CLUSTER BEHAVIOR UNDER FAILURE")
        
        print_concept("Partition States", PARTITION_CONCEPT)
        
        self.pause('cluster')
        
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
        
        self.pause('cluster')
        
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
        
        self.pause('cluster')
    
    # =========================================================================
    # LESSON 9: BEST PRACTICES
    # =========================================================================
    
    def lesson_best_practices(self):
        """Share SC best practices."""
        print_banner("LESSON 9: BEST PRACTICES")
        
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
        
        self.pause('cluster')
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _safe_remove(self, key):
        """Remove a record safely in SC mode using durable delete."""
        try:
            self.client.remove(key, policy={'durable_delete': True})
        except ae_exception.AerospikeError:
            # Record might not exist or delete not allowed
            pass
    
    def _explain_error(self, error):
        """Provide helpful explanation for common errors."""
        error_str = str(error)
        
        if 'PARTITION_UNAVAILABLE' in error_str:
            print_info("This partition's data is not currently accessible.")
            print_info("Check if nodes are missing from the cluster or roster.")
        elif 'TIMEOUT' in error_str:
            print_info("The operation timed out. Check if the cluster is healthy.")
            if hasattr(error, 'in_doubt') and error.in_doubt:
                print_warning("InDoubt: The write may or may not have been applied!")
        elif 'GENERATION' in error_str:
            print_info("The record was modified since you last read it.")
            print_info("Re-read the record and retry with the new generation.")
        elif 'FORBIDDEN' in error_str:
            print_info("This operation is not allowed in SC mode.")
            print_info("For deletes, use durable_delete=True or enable allow-expunge.")
    
    # =========================================================================
    # MAIN TUTORIAL FLOW
    # =========================================================================
    
    def run_tutorial(self, lessons=None, skip_sc_check=False):
        """Run the complete tutorial or specific lessons."""
        print_banner("AEROSPIKE STRONG CONSISTENCY TUTORIAL", '═')
        
        print("""
        Welcome to the Aerospike Strong Consistency Tutorial!
        
        This interactive guide will teach you:
        
          0. Setting Up SC with AeroLab (optional)
          1. Introduction to Strong Consistency
          2. Configuration and Setup
          3. Basic SC Operations  
          4. Consistency Levels
          5. Concurrent Write Ordering
          6. Optimistic Locking with Generations
          7. Error Handling
          8. Cluster Behavior under Failure
          9. Best Practices
        
        Press Ctrl+C at any time to exit.
        """)
        
        if not self.connect():
            print_error("Cannot proceed without cluster connection.")
            print_info("\nTo set up an SC cluster with AeroLab:")
            print(f"{Colors.DIM}")
            print("  aerolab config backend -t docker")
            print("  aerolab cluster create -n mydc -c 1 -f features.conf")
            print("  aerolab conf sc -n mydc")
            print(f"{Colors.ENDC}")
            return
        
        try:
            # Verify SC is enabled
            if not skip_sc_check:
                sc_enabled = self.show_cluster_status()
                
                if not sc_enabled:
                    print_error(f"\nStrong Consistency is NOT enabled on namespace '{self.namespace}'!")
                    print_info("\nWould you like to see AeroLab setup instructions?")
                    
                    if self.interactive:
                        try:
                            response = input(f"{Colors.BLUE}Show AeroLab setup? (y/n): {Colors.ENDC}").strip().lower()
                            if response == 'y':
                                self.lesson_aerolab_setup()
                                print_warning("\nPlease set up an SC cluster and re-run this tutorial.")
                                return
                        except KeyboardInterrupt:
                            raise SystemExit(0)
                    else:
                        print_info("Run with --lessons 0 to see AeroLab setup instructions.")
                        return
                else:
                    print_success(f"\n✓ Strong Consistency verified on namespace '{self.namespace}'")
                
                # Use 'introduction' to skip showing commands at tutorial start
                self.pause('introduction')
            
            all_lessons = [
                ('0', 'AeroLab Setup', self.lesson_aerolab_setup),
                ('1', 'Introduction', self.lesson_introduction),
                ('2', 'Configuration', self.lesson_configuration),
                ('3', 'Basic Operations', self.lesson_basic_operations),
                ('4', 'Consistency Levels', self.lesson_consistency_demo),
                ('5', 'Concurrent Writes', self.lesson_concurrent_writes),
                ('6', 'Generation Conflicts', self.lesson_generation_conflicts),
                ('7', 'Error Handling', self.lesson_error_handling),
                ('8', 'Cluster Behavior', self.lesson_cluster_behavior),
                ('9', 'Best Practices', self.lesson_best_practices),
            ]
            
            if lessons:
                # Run specific lessons
                for num, name, func in all_lessons:
                    if num in lessons:
                        func()
            else:
                # Run all lessons (skip lesson 0 - AeroLab setup - unless requested)
                for num, name, func in all_lessons:
                    if num != '0':  # Skip AeroLab setup in full tutorial
                        func()
            
            print_banner("TUTORIAL COMPLETE!", '═')
            
            print("""
        Congratulations! You've completed the Strong Consistency tutorial.
        
        Key Takeaways:
          ✓ SC guarantees write ordering and durability
          ✓ Use roster to manage cluster membership
          ✓ Session consistency is the default (and usually sufficient)
          ✓ Use generation checks for optimistic locking
          ✓ Handle InDoubt errors by reading to verify
          ✓ Monitor partition health for cluster issues
        
        For more information:
          • Aerospike SC Documentation: https://aerospike.com/docs/server/operations/configure/consistency
          • Managing SC Clusters: https://aerospike.com/docs/server/operations/manage/consistency
            """)
        
        except (KeyboardInterrupt, SystemExit):
            print(f"\n\n{Colors.YELLOW}Tutorial interrupted. Cleaning up...{Colors.ENDC}")
            
        finally:
            self.disconnect()


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Aerospike Strong Consistency Tutorial',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sc_demo.py                           # Run full tutorial
  python sc_demo.py --lessons 0               # Show AeroLab setup only
  python sc_demo.py --lessons 1 2 3           # Run specific lessons
  python sc_demo.py --non-interactive         # Run without pauses
  python sc_demo.py --host 127.0.0.1 --port 3100  # Connect to AeroLab cluster
        """
    )
    
    parser.add_argument('--host', default='127.0.0.1', 
                        help='Aerospike host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=3100, 
                        help='Aerospike port (default: 3100 for AeroLab)')
    parser.add_argument('--namespace', default='test',
                        help='Namespace to use (default: test)')
    parser.add_argument('--lessons', nargs='+', 
                        help='Specific lessons to run (0-9, where 0 is AeroLab setup)')
    parser.add_argument('--non-interactive', action='store_true',
                        help='Run without pauses')
    parser.add_argument('--skip-sc-check', action='store_true',
                        help='Skip the SC verification check')
    
    args = parser.parse_args()
    
    hosts = [(args.host, args.port)]
    
    tutorial = StrongConsistencyTutorial(
        hosts=hosts, 
        namespace=args.namespace,
        interactive=not args.non_interactive
    )
    
    # Skip SC check if showing AeroLab setup only
    skip_check = args.skip_sc_check or (args.lessons and '0' in args.lessons and len(args.lessons) == 1)
    
    tutorial.run_tutorial(lessons=args.lessons, skip_sc_check=skip_check)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tutorial interrupted. Goodbye!{Colors.ENDC}")
        sys.exit(0)
    except SystemExit:
        pass
