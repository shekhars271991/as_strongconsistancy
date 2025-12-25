"""
Configuration constants and text content for the SC tutorial.
"""

# Default connection settings
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 3100
DEFAULT_NAMESPACE = 'test'
DEFAULT_SET = 'tutorial'

# Timeout settings
CONNECTION_TIMEOUT = 5000

# =============================================================================
# CONCEPT TEXT CONTENT
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
Aerospike divides data into 4096 PARTITIONS. In SC mode, partition state is critical:

  • AVAILABLE    - Normal operation, data accessible
  • UNAVAILABLE  - Partition cannot be accessed (nodes missing from roster)
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

