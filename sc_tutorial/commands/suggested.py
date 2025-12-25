"""Suggested commands for each tutorial lesson."""

from ..ui.colors import Colors

# Comprehensive commands organized by lesson stage
LESSON_COMMANDS = {
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
            ("Shell 1: Check if gen changed", "SELECT *, generation FROM test WHERE PK='account1'"),
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


def show_suggested_commands(lesson_name):
    """Display extensive suggested commands for the current lesson, split by shell type."""
    
    lesson_data = LESSON_COMMANDS.get(lesson_name, LESSON_COMMANDS.get('basic_ops'))
    
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

