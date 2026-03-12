"""
FastAPI Web Application for Aerospike SC Tutorial
"""

import os
import asyncio
import json
from typing import Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import subprocess

# Import tutorial components
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sc_tutorial.config import (
    INTRO_TEXT, ROSTER_CONCEPT, PARTITION_CONCEPT, 
    CONSISTENCY_LEVELS, INDOUBT_CONCEPT, AEROLAB_SETUP, AEROLAB_MULTI_NODE
)

app = FastAPI(title="Aerospike SC Tutorial")

# Setup static files and templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# =============================================================================
# LESSON DATA
# =============================================================================

LESSONS = [
    {
        "id": 0,
        "title": "Setting Up SC with AeroLab",
        "short": "AeroLab Setup",
        "icon": "",
        "category": "setup",
        "content": f"""
        <h3>What is AeroLab?</h3>
        <p>AeroLab is Aerospike's official tool for quickly deploying development 
        and testing clusters. It supports Docker, AWS, and GCP backends.</p>
        <p><strong>For SC development, AeroLab is the fastest way to get started!</strong></p>
        
        <h3>Quick Setup (3 Commands)</h3>
        <pre><code># 1. Set Docker as backend
aerolab config backend -t docker

# 2. Create a 3-node cluster with your feature key
#    SC requires nodes >= replication-factor (RF=2 needs at least 2 nodes,
#    but 3 nodes is recommended for fault tolerance)
aerolab cluster create -n mydc -c 3 -f features.conf

# 3. Enable Strong Consistency (configures SC + roster automatically)
aerolab conf sc -n mydc</code></pre>

        <div class="info-box">
            <strong>Why 3 nodes?</strong> With RF=2, a 3-node cluster can tolerate 1 node failure.
            A 2-node RF=2 cluster has zero fault tolerance (both nodes are required).
            For single-node dev/test, set <code>replication-factor 1</code> in the config.
        </div>

        <h3>Verify SC is Enabled</h3>
        <pre><code>aerolab cluster list

# Check SC status
docker exec aerolab-mydc_1 asinfo -v "namespace/test" | grep strong-consistency</code></pre>

        <h3>Common AeroLab Commands</h3>
        <pre><code>aerolab cluster list              # List clusters
aerolab cluster start -n mydc     # Start cluster
aerolab cluster stop -n mydc      # Stop cluster  
aerolab cluster destroy -n mydc   # Delete cluster
aerolab attach shell -n mydc      # Shell into container</code></pre>
        """
    },
    {
        "id": 1,
        "title": "Introduction to Strong Consistency",
        "short": "Introduction",
        "icon": "",
        "category": "concepts",
        "content": f"""
        <h3>What is Strong Consistency?</h3>
        <p>Strong Consistency (SC) is an Aerospike Enterprise feature that guarantees:</p>
        <ul>
            <li>All writes to a record are applied in a specific, sequential order</li>
            <li>Writes will NOT be re-ordered or skipped (no data loss)</li>
            <li>All clients see the same view of data at any point in time</li>
        </ul>
        <p>This is different from the default Available/Partition-tolerant (AP) mode
        which prioritizes availability over strict consistency.</p>
        
        <h3>SC Mode is Essential For:</h3>
        <ul>
            <li>Financial transactions</li>
            <li>Inventory management</li>
            <li>Any application where data accuracy is critical</li>
        </ul>

        <h3>AP vs SC Mode Comparison</h3>
        <table class="comparison-table">
            <tr><th>Feature</th><th>AP Mode</th><th>SC Mode</th></tr>
            <tr><td>Data Consistency</td><td>Eventually consistent</td><td>Strongly consistent</td></tr>
            <tr><td>Availability</td><td>Higher</td><td>Lower (when degraded)</td></tr>
            <tr><td>Write Ordering</td><td>May reorder</td><td>Strict ordering</td></tr>
            <tr><td>Read Guarantees</td><td>May see stale data</td><td>Always current</td></tr>
            <tr><td>Network Partition</td><td>Both sides operate</td><td>One side unavailable</td></tr>
            <tr><td>Use Case</td><td>Caching, analytics</td><td>Transactions, finance</td></tr>
        </table>
        """
    },
    {
        "id": 2,
        "title": "Configuration and Setup",
        "short": "Configuration",
        "icon": "",
        "category": "setup",
        "content": f"""
        <p>In this lesson you'll explore how an SC namespace is configured and learn
        the <strong>roster</strong> — the single most important SC concept.
        Follow each step below using the terminal tabs on the right.</p>

        <div class="guided-steps" data-guided="lesson2">

            <!-- Step 1 -->
            <div class="guided-step active" data-step="1">
                <div class="guided-step-header">
                    <span class="guided-step-num">1</span>
                    <span class="guided-step-title">Check if SC is enabled</span>
                    <span class="guided-step-status"></span>
                </div>
                <div class="guided-step-body">
                    <p>Open the <strong>Shell</strong> tab and run this command to check the namespace configuration:</p>
                    <pre><code>asinfo -v "namespace/test" | tr ';' '\\n' | grep -E "strong-consistency|replication-factor"</code></pre>
                    <div class="guided-step-expect">
                        <strong>You should see:</strong><br>
                        <code>strong-consistency=true</code> and <code>replication-factor=2</code>
                    </div>
                    <p class="guided-step-why">This confirms your namespace is running in SC mode with 2 copies of every record.</p>
                    <button class="btn btn-primary btn-sm guided-done-btn" onclick="completeStep('lesson2', 1)">Done — I can see it</button>
                </div>
            </div>

            <!-- Step 2 -->
            <div class="guided-step locked" data-step="2">
                <div class="guided-step-header">
                    <span class="guided-step-num">2</span>
                    <span class="guided-step-title">View the current roster</span>
                    <span class="guided-step-status"></span>
                </div>
                <div class="guided-step-body">
                    <p>Switch to the <strong>ASADM</strong> tab and run:</p>
                    <pre><code>show roster</code></pre>
                    <div class="guided-step-expect">
                        <strong>Look for three columns:</strong><br>
                        <code>Current Roster</code> — the active list of trusted nodes<br>
                        <code>Pending Roster</code> — staged changes waiting for recluster<br>
                        <code>Observed Nodes</code> — nodes the cluster currently sees
                    </div>
                    <p class="guided-step-why">The roster is what makes SC special — only nodes on the roster can hold master/replica copies.
                    If a node isn't on the roster, the cluster doesn't trust it with data.</p>
                    <button class="btn btn-primary btn-sm guided-done-btn" onclick="completeStep('lesson2', 2)">Done — I see the roster</button>
                </div>
            </div>

            <!-- Step 3 -->
            <div class="guided-step locked" data-step="3">
                <div class="guided-step-header">
                    <span class="guided-step-num">3</span>
                    <span class="guided-step-title">Compare cluster_size vs ns_cluster_size</span>
                    <span class="guided-step-status"></span>
                </div>
                <div class="guided-step-body">
                    <p>Still in <strong>ASADM</strong>, run:</p>
                    <pre><code>show stat -flip like cluster_size</code></pre>
                    <div class="guided-step-expect">
                        <strong>You should see two numbers:</strong><br>
                        <code>cluster_size</code> — total nodes in the network cluster<br>
                        <code>ns_cluster_size</code> — nodes on the SC roster for this namespace<br><br>
                        When these match, every node is on the roster. If <code>cluster_size &gt; ns_cluster_size</code>,
                        a node has joined but hasn't been added to the roster yet.
                    </div>
                    <p class="guided-step-why">This is the first thing to check when debugging SC issues — a mismatch
                    means the roster needs updating.</p>
                    <button class="btn btn-primary btn-sm guided-done-btn" onclick="completeStep('lesson2', 3)">Done — numbers match</button>
                </div>
            </div>

            <!-- Step 4 -->
            <div class="guided-step locked" data-step="4">
                <div class="guided-step-header">
                    <span class="guided-step-num">4</span>
                    <span class="guided-step-title">Check partition health</span>
                    <span class="guided-step-status"></span>
                </div>
                <div class="guided-step-body">
                    <p>Run this in <strong>ASADM</strong> to see if all partitions are healthy:</p>
                    <pre><code>show stat namespace for test like dead_partitions -flip
show stat namespace for test like unavailable_partitions -flip</code></pre>
                    <div class="guided-step-expect">
                        <strong>Both should show 0</strong> on every node.<br>
                        <code>dead_partitions = 0</code> — no data loss<br>
                        <code>unavailable_partitions = 0</code> — all data accessible
                    </div>
                    <p class="guided-step-why">These two metrics are the heartbeat of an SC cluster.
                    In later lessons you'll see what happens when nodes go down and these numbers change.</p>
                    <button class="btn btn-primary btn-sm guided-done-btn" onclick="completeStep('lesson2', 4)">Done — all zeros</button>
                </div>
            </div>

            <!-- Step 5 -->
            <div class="guided-step locked" data-step="5">
                <div class="guided-step-header">
                    <span class="guided-step-num">5</span>
                    <span class="guided-step-title">View the full namespace config</span>
                    <span class="guided-step-status"></span>
                </div>
                <div class="guided-step-body">
                    <p>Finally, see all the SC-related settings at once in <strong>ASADM</strong>:</p>
                    <pre><code>show config namespace for test like strong-consistency
show config namespace for test like commit-to-device
show config namespace for test like default-ttl</code></pre>
                    <div class="guided-step-expect">
                        <strong>Key settings to note:</strong><br>
                        <code>strong-consistency = true</code> — SC is on<br>
                        <code>commit-to-device = false</code> — default (enable for max durability)<br>
                        <code>default-ttl = 0</code> — no expiration (recommended for SC)
                    </div>
                    <p class="guided-step-why">Now you've seen the full picture: SC mode is a namespace-level
                    setting, the roster controls which nodes participate, and partition health
                    tells you if everything is working.</p>
                    <button class="btn btn-primary btn-sm guided-done-btn" onclick="completeStep('lesson2', 5)">Done — lesson complete!</button>
                </div>
            </div>

        </div>

        <div class="guided-summary" id="lesson2-summary" style="display:none;">
            <h3>Summary</h3>
            <ul>
                <li><code>strong-consistency true</code> enables SC on a namespace (cannot switch from AP later)</li>
                <li>The <strong>roster</strong> is the list of trusted nodes — only roster nodes hold data</li>
                <li><code>cluster_size</code> vs <code>ns_cluster_size</code> tells you if all nodes are on the roster</li>
                <li><code>dead_partitions</code> and <code>unavailable_partitions</code> are the two key health metrics</li>
                <li><code>commit-to-device</code>, <code>default-ttl 0</code>, and <code>node-id</code> are important optional settings</li>
            </ul>
        </div>
        """
    },
    {
        "id": 3,
        "title": "Basic SC Operations",
        "short": "Basic Ops",
        "icon": "",
        "category": "practice",
        "content": f"""
        <h3>SC Write Guarantees</h3>
        <p>When a write succeeds in SC mode:</p>
        <ul>
            <li>The write has been replicated to all required nodes</li>
            <li>The write is durable (won't be lost)</li>
            <li>All subsequent reads will see this write</li>
            <li>The write has a specific position in the record's history</li>
        </ul>

        <div class="info-box">
            <strong>Python Terminal:</strong> The Python tab has a pre-connected client:
            <ul>
                <li><code>client</code> - Connected Aerospike client object</li>
                <li>Keys are tuples: <code>(namespace, set, primary_key)</code></li>
                <li>Use <code>None</code> for default set: <code>("test", None, "key1")</code></li>
            </ul>
        </div>

        <div class="exercise-box">
            <h4>Exercise: Create and Read Records</h4>
            <p>Try this in <strong>AQL</strong> or <strong>Python</strong> terminal tabs:</p>
            
            <div class="code-tabs">
                <div class="code-tabs-header">
                    <button class="code-tab-btn active" data-lang="aql">AQL</button>
                    <button class="code-tab-btn" data-lang="python">Python</button>
                </div>
                <div class="code-tab-content active" data-lang="aql">
                    <pre><code># 1. Insert a user record
INSERT INTO test (PK, name, age) VALUES ('user1', 'Alice', 30)

# 2. Read it back with generation
SELECT *, generation FROM test WHERE PK='user1'

# 3. Update the record (INSERT overwrites)
INSERT INTO test (PK, name, age) VALUES ('user1', 'Alice', 31)

# 4. Read again - generation increased!
SELECT *, generation FROM test WHERE PK='user1'</code></pre>
                </div>
                <div class="code-tab-content" data-lang="python">
                    <pre><code># 1. Insert a user record
key = ("test", None, "user1")
client.put(key, {{"name": "Alice", "age": 30}})

# 2. Read it back with metadata
(key, meta, bins) = client.get(key)
print(f"Data: {{bins}}, Generation: {{meta['gen']}}")

# 3. Update the record
client.put(key, {{"name": "Alice", "age": 31}})

# 4. Read again - generation increased!
(key, meta, bins) = client.get(key)
print(f"Data: {{bins}}, Generation: {{meta['gen']}}")</code></pre>
                </div>
            </div>
            
            <div class="verify-box">
                <strong>Verify:</strong> The generation should have increased from 1 to 2. 
                This proves your write was applied!
            </div>
        </div>

        <div class="exercise-box">
            <h4>Exercise: Understand Tombstones</h4>
            <p>In SC mode, deletes create tombstones to ensure consistency across replicas.</p>
            
            <div class="code-tabs">
                <div class="code-tabs-header">
                    <button class="code-tab-btn active" data-lang="aql">AQL</button>
                    <button class="code-tab-btn" data-lang="python">Python</button>
                </div>
                <div class="code-tab-content active" data-lang="aql">
                    <pre><code># 1. Delete the record
DELETE FROM test WHERE PK='user1'

# 2. Try to read it (returns nothing)
SELECT * FROM test WHERE PK='user1'</code></pre>
                </div>
                <div class="code-tab-content" data-lang="python">
                    <pre><code># 1. Delete the record (durable delete for SC)
key = ("test", None, "user1")
client.remove(key)

# 2. Try to read it (raises exception)
try:
    (key, meta, bins) = client.get(key)
except aerospike.exception.RecordNotFound:
    print("Record not found (tombstone created)")</code></pre>
                </div>
            </div>
            
            <p>Check tombstone count in <strong>ASADM</strong>:</p>
            <pre><code>show stat namespace like tombstones</code></pre>
            
            <div class="verify-box">
                <strong>Verify:</strong> The read returns nothing, but <code>tombstones</code> count is &gt; 0.
                Tombstones ensure deletes propagate correctly in SC mode.
            </div>
        </div>
        """
    },
    {
        "id": 4,
        "title": "Consistency Levels",
        "short": "Consistency",
        "icon": "",
        "category": "concepts",
        "content": f"""
        <h3>Two Read Consistency Levels</h3>
        
        <div class="card">
            <h4>1. SESSION CONSISTENCY (Default)</h4>
            <ul>
                <li>Guarantees monotonic reads within a single client session</li>
                <li>You always see your own writes (read-your-writes)</li>
                <li>Lower latency than linearizable</li>
                <li><strong>Best for most use cases</strong></li>
            </ul>
        </div>

        <div class="card">
            <h4>2. LINEARIZABLE CONSISTENCY</h4>
            <ul>
                <li>Global ordering visible to ALL clients simultaneously</li>
                <li>If client A reads after client B writes, A sees B's write</li>
                <li>Higher latency (requires extra coordination)</li>
                <li>Use when multiple clients must see exact same state</li>
            </ul>
        </div>

        <div class="exercise-box">
            <h4>Exercise: Verify Read-Your-Writes</h4>
            <p>Session consistency guarantees you always see your own writes:</p>
            
            <div class="code-tabs">
                <div class="code-tabs-header">
                    <button class="code-tab-btn active" data-lang="aql">AQL</button>
                    <button class="code-tab-btn" data-lang="python">Python</button>
                </div>
                <div class="code-tab-content active" data-lang="aql">
                    <pre><code># 1. Create a test record
INSERT INTO test (PK, counter) VALUES ('session_test', 0)

# 2. Immediately read it back
SELECT * FROM test WHERE PK='session_test'

# 3. Update the value
INSERT INTO test (PK, counter) VALUES ('session_test', 100)

# 4. Read again immediately
SELECT counter, generation FROM test WHERE PK='session_test'</code></pre>
                </div>
                <div class="code-tab-content" data-lang="python">
                    <pre><code># 1. Create a test record
key = ("test", None, "session_test")
client.put(key, {{"counter": 0}})

# 2. Immediately read it back
(_, meta, bins) = client.get(key)
print(f"Initial: {{bins}}")

# 3. Update the value
client.put(key, {{"counter": 100}})

# 4. Read again immediately
(_, meta, bins) = client.get(key)
print(f"After update: {{bins}}, gen={{meta['gen']}}")</code></pre>
                </div>
            </div>
            
            <div class="verify-box">
                <strong>Verify:</strong> You should see <code>counter=100</code> immediately. 
                This is the "read-your-writes" guarantee of session consistency.
            </div>
        </div>

        <h3>Relaxed Read Modes</h3>
        <p>SC also provides two <strong>relaxed</strong> read policies that trade strict monotonicity for better availability:</p>

        <div class="card">
            <h4>3. ALLOW_REPLICA</h4>
            <ul>
                <li>Allows reads from <strong>replica partitions</strong> (not just the master)</li>
                <li>Reads are still committed records, but no longer strictly monotonic</li>
                <li>Prevents read timeouts when a node/rack goes down</li>
                <li>Enables <code>PREFER_RACK</code> policy to reduce cross-AZ traffic</li>
                <li>In practice, session consistency violations are very rare</li>
            </ul>
        </div>

        <div class="card">
            <h4>4. ALLOW_UNAVAILABLE</h4>
            <ul>
                <li>Allows reads from <strong>unavailable partitions</strong> (previously committed data)</li>
                <li>Stale reads possible, but never dirty (uncommitted) reads</li>
                <li>Useful for applications sensitive to read unavailability</li>
                <li>When partitions are available, behaves identically to ALLOW_REPLICA</li>
            </ul>
        </div>

        <div class="exercise-box">
            <h4>Exercise: Check Consistency Configuration</h4>
            <p>View the current consistency settings in <strong>ASADM</strong>:</p>
            
            <ol>
                <li>Check read consistency level:
                    <pre><code>show config namespace like read-consistency</code></pre>
                </li>
                <li>Check write commit level:
                    <pre><code>show config namespace like write-commit</code></pre>
                </li>
            </ol>
            
            <div class="info-box">
                <strong>Performance Guide:</strong>
                <ul>
                    <li>Session Consistency (default) — best balance of safety and speed</li>
                    <li>Linearizable — ~20-50% slower due to replica regime checks</li>
                    <li>ALLOW_REPLICA — same performance, better availability during failures</li>
                    <li>ALLOW_UNAVAILABLE — maximum read availability during major outages</li>
                </ul>
            </div>
        </div>
        """
    },
    {
        "id": 5,
        "title": "Concurrent Write Ordering",
        "short": "Concurrency",
        "icon": "",
        "category": "concepts",
        "content": f"""
        <h3>Write Ordering Guarantee</h3>
        <p>In SC mode, all writes to a single record are applied in a specific, sequential order:</p>
        <ul>
            <li>Concurrent writes from different clients are serialized</li>
            <li>Each write gets a unique position in the record's history</li>
            <li>No writes are lost or reordered</li>
            <li>The generation number reflects the total write count</li>
        </ul>

        <h3>Counter Increment Example</h3>
        <p>Multiple clients incrementing a counter will never lose updates.</p>
        
        <div class="info-box">
            <strong>Note:</strong> AQL doesn't support arithmetic operations like <code>counter + 1</code>.
            In production, use the client SDK's <code>operate()</code> API with <code>add</code> operation.
            In AQL, we demonstrate the concept by manually incrementing:
        </div>
        
        <pre><code># Initialize counter
INSERT INTO test (PK, counter) VALUES ('counter', 0)

# Read current value
SELECT counter, generation FROM test WHERE PK='counter'

# Manually increment (in real apps, use SDK's add operation)
INSERT INTO test (PK, counter) VALUES ('counter', 1)

# Check value and generation
SELECT counter, generation FROM test WHERE PK='counter'</code></pre>

        <div class="success-box">
            SC guarantees: Each write gets a unique generation. No writes are lost or reordered.
        </div>
        """
    },
    {
        "id": 6,
        "title": "Optimistic Locking with Generations",
        "short": "Generations",
        "icon": "",
        "category": "practice",
        "content": f"""
        <h3>Generation Numbers</h3>
        <p>Every record has a <strong>GENERATION</strong> number that increments with each write.</p>
        
        <h4>Optimistic Locking Pattern:</h4>
        <ol>
            <li>Read record and note its generation</li>
            <li>Modify data locally</li>
            <li>Write back with generation check</li>
            <li>If generation changed, write fails → retry</li>
        </ol>

        <div class="exercise-box">
            <h4>Exercise: Track Generation Changes</h4>
            <p>Observe how generation increments with each write:</p>
            
            <div class="code-tabs">
                <div class="code-tabs-header">
                    <button class="code-tab-btn active" data-lang="aql">AQL</button>
                    <button class="code-tab-btn" data-lang="python">Python</button>
                </div>
                <div class="code-tab-content active" data-lang="aql">
                    <pre><code># 1. Create an account record
INSERT INTO test (PK, balance) VALUES ('account1', 1000)

# 2. Check generation (should be 1)
SELECT balance, generation FROM test WHERE PK='account1'

# 3. Update the balance
INSERT INTO test (PK, balance) VALUES ('account1', 1100)

# 4. Check generation (should be 2)
SELECT balance, generation FROM test WHERE PK='account1'

# 5. Update once more
INSERT INTO test (PK, balance) VALUES ('account1', 1200)

# 6. Final check (should be 3)
SELECT balance, generation FROM test WHERE PK='account1'</code></pre>
                </div>
                <div class="code-tab-content" data-lang="python">
                    <pre><code># 1. Create an account record
key = ("test", None, "account1")
client.put(key, {{"balance": 1000}})

# 2. Check generation (should be 1)
(_, meta, bins) = client.get(key)
print(f"balance={{bins['balance']}}, gen={{meta['gen']}}")

# 3. Update the balance
client.put(key, {{"balance": 1100}})

# 4. Check generation (should be 2)
(_, meta, bins) = client.get(key)
print(f"balance={{bins['balance']}}, gen={{meta['gen']}}")

# 5. Update once more
client.put(key, {{"balance": 1200}})

# 6. Final check (should be 3)
(_, meta, bins) = client.get(key)
print(f"balance={{bins['balance']}}, gen={{meta['gen']}}")</code></pre>
                </div>
            </div>
            
            <div class="verify-box">
                <strong>Verify:</strong> Generation incremented from 1 → 2 → 3 with each write.
                This counter lets applications detect concurrent modifications.
            </div>
        </div>

        <div class="exercise-box">
            <h4>Exercise: Monitor Generation Conflicts</h4>
            <p>Check the generation conflict statistics in <strong>ASADM</strong>:</p>
            
            <ol>
                <li>View generation failure stats:
                    <pre><code>show stat namespace like fail_generation</code></pre>
                </li>
                <li>View all failure stats:
                    <pre><code>show stat namespace like fail_</code></pre>
                </li>
            </ol>
            
            <div class="info-box">
                High <code>fail_generation</code> rates indicate application concurrency issues.
                Consider reviewing your application's read-modify-write patterns.
            </div>
        </div>
        """
    },
    {
        "id": 7,
        "title": "Error Handling",
        "short": "Errors",
        "icon": "",
        "category": "practice",
        "content": f"""
        <h3>InDoubt Errors</h3>
        <p>The <strong>IN-DOUBT</strong> error indicates uncertainty about whether a write was applied.</p>
        
        <div class="warning-box">
            When you get InDoubt=True:
            <ul>
                <li>The write MAY have been applied</li>
                <li>The write MAY NOT have been applied</li>
                <li>You should <strong>read the record</strong> to determine the actual state</li>
            </ul>
        </div>

        <h3>Common SC Errors</h3>
        <table class="comparison-table">
            <tr><th>Error</th><th>Meaning</th></tr>
            <tr><td>PARTITION_UNAVAILABLE</td><td>Data partition is not accessible</td></tr>
            <tr><td>INVALID_NODE_ERROR</td><td>No node available for the partition</td></tr>
            <tr><td>TIMEOUT</td><td>Operation timed out (InDoubt possible)</td></tr>
            <tr><td>GENERATION_ERROR</td><td>Record was modified by another client</td></tr>
            <tr><td>FORBIDDEN</td><td>Operation not allowed (cluster issue)</td></tr>
            <tr><td>FAIL_FORBIDDEN</td><td>Non-durable delete blocked in SC</td></tr>
        </table>

        <div class="exercise-box">
            <h4>Exercise: Handle SC Errors in Python</h4>
            <p>Proper error handling is critical in SC mode:</p>
            
            <div class="code-tabs">
                <div class="code-tabs-header">
                    <button class="code-tab-btn active" data-lang="python">Python</button>
                </div>
                <div class="code-tab-content active" data-lang="python">
                    <pre><code>import aerospike
from aerospike import exception as ex

key = ("test", None, "error_test")

# Write with generation check (optimistic locking)
try:
    # First, read and get current generation
    (_, meta, _) = client.get(key)
    current_gen = meta['gen']
    
    # Write with expected generation
    write_policy = {{'gen': aerospike.POLICY_GEN_EQ}}
    meta = {{'gen': current_gen}}
    client.put(key, {{"value": "updated"}}, meta, write_policy)
    print("Write succeeded!")
    
except ex.RecordGenerationError as e:
    print(f"Generation conflict! Record was modified.")
    print(f"in_doubt: {{e.in_doubt}}")
    # Retry: read again and retry the write
    
except ex.RecordNotFound as e:
    print("Record doesn't exist")
    
except ex.TimeoutError as e:
    print(f"Timeout! in_doubt: {{e.in_doubt}}")
    if e.in_doubt:
        # Read to check if write was applied
        (_, meta, bins) = client.get(key)
        print(f"Actual state: {{bins}}")

except ex.AerospikeError as e:
    print(f"Error: {{e.msg}}, in_doubt: {{e.in_doubt}}")</code></pre>
                </div>
            </div>
        </div>

        <h3>Check Error Stats in ASADM</h3>
        <pre><code>show stat namespace like fail_
show stat namespace like fail_generation
show stat namespace like timeout</code></pre>
        """
    },
    {
        "id": 8,
        "title": "Cluster Behavior Under Failure",
        "short": "Failure Modes",
        "icon": "",
        "category": "concepts",
        "content": f"""
        <h3>Partition States</h3>
        <ul>
            <li><strong>AVAILABLE</strong> - Normal operation, data accessible</li>
            <li><strong>UNAVAILABLE</strong> - Partition cannot be accessed (nodes missing)</li>
            <li><strong>DEAD</strong> - Data potentially lost, requires manual intervention</li>
        </ul>

        <h3>Failure Scenarios</h3>
        
        <div class="card">
            <h4>Scenario 1: Single Node Failure (RF=2)</h4>
            <p>All partitions remain AVAILABLE. Data re-replicates automatically.</p>
        </div>

        <div class="card">
            <h4>Scenario 2: Multiple Node Failures</h4>
            <p>Some partitions become UNAVAILABLE. Affected records cannot be accessed.</p>
        </div>

        <div class="card">
            <h4>Scenario 3: Network Partition (Split Brain)</h4>
            <p>SC prevents both sides from operating independently. Only the side with majority continues.</p>
        </div>

        <h3>Try It: Check Partition Status</h3>
        <pre><code># In ASADM - Check partition status
show pmap
show stat namespace like dead_partitions
show stat namespace like unavailable

# View roster
show roster</code></pre>

        <div class="warning-box">
            <strong>Important:</strong> Recovery commands like <code>revive</code> should only be used 
            when you understand the implications. Move to the next lessons to learn proper recovery procedures.
        </div>
        """
    },
    {
        "id": 9,
        "title": "Adding Nodes to SC Cluster",
        "short": "Add Nodes",
        "icon": "",
        "category": "operations",
        "content": f"""
        <h3>Why Add Nodes?</h3>
        <p>Adding nodes increases capacity and fault tolerance. In SC mode, new nodes must be added to the <strong>roster</strong> to participate in data replication.</p>

        <div class="warning-box">
            <strong>Prerequisites Before Adding a Node:</strong>
            <ul>
                <li>New drives must be initialized (data will be erased)</li>
                <li>Remove <code>/opt/aerospike/smd</code> folder if node was in a different cluster</li>
                <li>Configuration must match existing nodes (memory, disk allocation)</li>
                <li>Add nodes during low-traffic periods (migrations consume resources)</li>
            </ul>
        </div>

        <div class="exercise-box">
            <h4>Exercise: Check Current Cluster State</h4>
            <p>Before adding a node, verify your cluster's current state in <strong>ASADM</strong>:</p>
            
            <ol>
                <li>View current cluster info:
                    <pre><code>info</code></pre>
                </li>
                <li>Compare cluster_size vs ns_cluster_size:
                    <pre><code>show stat -flip like cluster_size</code></pre>
                </li>
                <li>View the current roster:
                    <pre><code>show roster</code></pre>
                </li>
            </ol>
            
            <div class="verify-box">
                <strong>Verify:</strong> Note the current <code>cluster_size</code> and the nodes listed in the roster.
                All nodes in <strong>Current Roster</strong> should match <strong>Observed Nodes</strong>.
            </div>
        </div>

        <div class="info-box">
            <strong>Key Insight:</strong> When <code>cluster_size</code> &gt; <code>ns_cluster_size</code>, a new node has joined the cluster but is NOT yet on the SC roster. You must update the roster for SC operations to use the new node.
        </div>

        <div class="exercise-box">
            <h4>Exercise: Roster Update Procedure</h4>
            <p>After a new node joins, follow these steps in <strong>ASADM</strong> to add it to the roster:</p>
            
            <ol>
                <li>Enable admin mode:
                    <pre><code>enable</code></pre>
                </li>
                <li>Stage observed nodes to pending roster:
                    <pre><code>manage roster stage observed ns test</code></pre>
                    <div class="expected-output">Pending roster now contains observed nodes.
Run "manage recluster" for your changes to take effect.</div>
                </li>
                <li>Apply the roster change:
                    <pre><code>manage recluster</code></pre>
                    <div class="expected-output">Successfully started recluster</div>
                </li>
                <li>Verify the roster is updated:
                    <pre><code>show roster</code></pre>
                </li>
                <li>Watch migrations complete (wait for 0):
                    <pre><code>show stat service like partitions_remaining -flip</code></pre>
                </li>
            </ol>
            
            <div class="verify-box">
                <strong>Verify:</strong> 
                <ul>
                    <li><code>cluster_size</code> equals <code>ns_cluster_size</code></li>
                    <li><code>migrate_partitions_remaining = 0</code> on all nodes</li>
                    <li>New node appears in <strong>Current Roster</strong></li>
                </ul>
            </div>
        </div>

        <h3>Best Practices</h3>
        <ul>
            <li>Add one node at a time and wait for migrations to complete</li>
            <li>Avoid adding multiple nodes simultaneously (can form separate cluster)</li>
            <li>Mixed-version clusters are only supported temporarily (rolling upgrades)</li>
        </ul>
        """
    },
    {
        "id": 10,
        "title": "Removing Nodes from SC Cluster",
        "short": "Remove Nodes",
        "icon": "",
        "category": "operations",
        "content": f"""
        <h3>Safe Node Removal</h3>
        <p>Removing nodes from an SC cluster requires careful planning to avoid data unavailability.</p>

        <div class="warning-box">
            <strong>CRITICAL:</strong> Do NOT remove nodes equal to or greater than your replication-factor (RF) simultaneously!
            <ul>
                <li>RF=2: Can safely remove 1 node at a time</li>
                <li>RF=3: Can safely remove up to 2 nodes at a time</li>
                <li>Removing too many nodes causes <strong>unavailable partitions</strong></li>
            </ul>
        </div>

        <h3>Step 1: Verify No Ongoing Migrations</h3>
        <pre><code># In ASADM - must show 0 for all nodes
show stat service like partitions_remaining -flip</code></pre>

        <h3>Step 2: Verify Roster State</h3>
        <pre><code># All roster nodes should be present
show roster</code></pre>

        <h3>Step 3: Shutdown the Node (Gracefully)</h3>
        <pre><code># On the node being removed:
systemctl stop aerospike

# Or for Docker:
docker stop &lt;container_name&gt;</code></pre>

        <div class="info-box">
            <strong>Note:</strong> A graceful shutdown (SIGTERM) flushes data to disk and notifies other nodes.
        </div>

        <h3>Step 4: Wait for Migrations</h3>
        <pre><code># Watch until all nodes show 0
show stat service like partitions_remaining -flip</code></pre>

        <h3>Step 5: Update the Roster</h3>
        <pre><code># In ASADM (enable mode)
enable

# View roster - removed node gone from Observed Nodes
show roster

# Stage observed nodes (excludes the removed node)
manage roster stage observed ns test

# Apply the change
manage recluster</code></pre>

        <h3>Step 6: Cleanup</h3>
        <pre><code># Clear the removed node from heartbeat tip list
asinfo -v 'tip-clear:host-port-list=&lt;removed_ip&gt;:3002'

# Clear from alumni list
asinfo -v 'services-alumni-reset'</code></pre>

        <h3>Step 7: Update Configuration</h3>
        <p>On remaining nodes, remove the departed node from <code>mesh-seed-address-port</code> in aerospike.conf.</p>

        <div class="success-box">
            <strong>Success Indicators:</strong>
            <ul>
                <li><code>migrate_partitions_remaining = 0</code> on all nodes</li>
                <li>Roster shows correct node count</li>
                <li>No dead or unavailable partitions</li>
            </ul>
        </div>
        """
    },
    {
        "id": 11,
        "title": "Validating Partition Health",
        "short": "Partition Health",
        "icon": "",
        "category": "operations",
        "content": f"""
        <h3>Understanding Partitions</h3>
        <p>Aerospike distributes data across 4096 partitions. In SC mode, each partition must have the required number of replicas to be available.</p>

        <div class="exercise-box">
            <h4>Exercise: Check Partition Health</h4>
            <p>Run a complete health check in <strong>ASADM</strong>:</p>
            
            <ol>
                <li>Check for dead partitions:
                    <pre><code>show stat namespace for test like dead_partitions -flip</code></pre>
                </li>
                <li>Check for unavailable partitions:
                    <pre><code>show stat namespace for test like unavailable_partitions -flip</code></pre>
                </li>
                <li>Check migration status:
                    <pre><code>show stat service like partitions_remaining -flip</code></pre>
                </li>
                <li>View the roster:
                    <pre><code>show roster</code></pre>
                </li>
            </ol>
            
            <div class="verify-box">
                <strong>Healthy Cluster Indicators:</strong>
                <ul>
                    <li><code>dead_partitions = 0</code> on all nodes</li>
                    <li><code>unavailable_partitions = 0</code> on all nodes</li>
                    <li><code>migrate_partitions_remaining = 0</code> on all nodes</li>
                    <li>All roster nodes are <strong>Observed</strong></li>
                </ul>
            </div>
        </div>

        <h3>What The Numbers Mean</h3>
        <table class="comparison-table">
            <tr><th>Metric</th><th>Value 0</th><th>Value &gt; 0</th></tr>
            <tr>
                <td><code>dead_partitions</code></td>
                <td>All data accessible</td>
                <td>Data potentially lost - requires manual intervention</td>
            </tr>
            <tr>
                <td><code>unavailable_partitions</code></td>
                <td>All partitions operational</td>
                <td>Some data temporarily inaccessible - will recover when nodes return</td>
            </tr>
        </table>

        <div class="exercise-box">
            <h4>Exercise: Verify Data Accessibility</h4>
            <p>Confirm you can read and write data in <strong>AQL</strong>:</p>
            
            <ol>
                <li>Write a test record:
                    <pre><code>INSERT INTO test (PK, val) VALUES ('health_check', 1)</code></pre>
                </li>
                <li>Read it back:
                    <pre><code>SELECT * FROM test WHERE PK='health_check'</code></pre>
                </li>
                <li>Clean up:
                    <pre><code>DELETE FROM test WHERE PK='health_check'</code></pre>
                </li>
            </ol>
            
            <div class="verify-box">
                <strong>Verify:</strong> If all commands succeed without errors, your data partitions are healthy!
            </div>
        </div>

        <h3>Common Causes of Partition Issues</h3>
        <div class="card">
            <h4>Unavailable Partitions</h4>
            <ul>
                <li>Node(s) temporarily down</li>
                <li>Network connectivity issues</li>
                <li>Node not yet on roster</li>
            </ul>
            <p><strong>Resolution:</strong> Restore nodes or fix network. Partitions become available automatically.</p>
        </div>

        <div class="card">
            <h4>Dead Partitions</h4>
            <ul>
                <li>All replicas of a partition were lost</li>
                <li>Nodes removed without proper procedure</li>
                <li>Multiple simultaneous node failures</li>
            </ul>
            <p><strong>Resolution:</strong> Requires manual <code>revive</code> command (accepts potential data loss).</p>
        </div>
        """
    },
    {
        "id": 12,
        "title": "Reviving Dead Partitions",
        "short": "Revive Partitions",
        "icon": "",
        "category": "operations",
        "content": f"""
        <h3>When to Revive Partitions</h3>
        <p>The <code>revive</code> command is used when partitions are <strong>dead</strong> and you need to restore cluster operation, accepting that some data may be lost.</p>

        <div class="warning-box">
            <strong>WARNING:</strong> Reviving dead partitions acknowledges potential data loss!
            <ul>
                <li>Only use when you cannot restore the missing nodes</li>
                <li>Consider reloading data from backup or message queue after revive</li>
                <li>Document the incident for compliance/audit purposes</li>
            </ul>
        </div>

        <h3>Step 1: Identify Dead Partitions</h3>
        <pre><code># In ASADM
show stat namespace for test like dead -flip</code></pre>

        <p>Example output showing 264 dead partitions:</p>
        <pre><code>~test Namespace Statistics~
                    Node|dead_partitions
node1.example.com:3000  |            264
node2.example.com:3000  |            264</code></pre>

        <h3>Step 2: Verify All Available Nodes Are Present</h3>
        <pre><code># Ensure remaining nodes are on the roster
show roster

# Check cluster stability
info</code></pre>

        <h3>Step 3: Execute Revive</h3>
        <pre><code># Enable admin mode
enable

# Revive dead partitions for the namespace
manage revive ns test</code></pre>

        <p>Expected output:</p>
        <pre><code>~~~Revive Namespace Partitions~~~
                    Node|Response
node1.example.com:3000  |ok
node2.example.com:3000  |ok</code></pre>

        <h3>Step 4: Recluster to Apply</h3>
        <pre><code># Apply the revive operation
manage recluster</code></pre>

        <h3>Step 5: Verify Recovery</h3>
        <pre><code># Dead partitions should now be 0
show stat namespace for test like dead -flip

# Monitor migrations
show stat service like partitions_remaining -flip</code></pre>

        <div class="success-box">
            <strong>Success:</strong> <code>dead_partitions = 0</code> on all nodes
        </div>

        <h3>Post-Revive Actions</h3>
        <ul>
            <li>Verify application functionality</li>
            <li>Check if data needs to be reloaded</li>
            <li>Update monitoring/alerting thresholds</li>
            <li>Document root cause and remediation</li>
        </ul>
        """
    },
    {
        "id": 13,
        "title": "Multi-Node Cluster Setup",
        "short": "Multi-Node",
        "icon": "",
        "category": "setup",
        "content": f"""
        <h3>Creating a Multi-Node SC Cluster</h3>
        <p>Production SC deployments typically use 3+ nodes with RF=2 or RF=3 for high availability.</p>

        <h3>Using AeroLab for Multi-Node</h3>
        <pre><code># Create 3-node cluster
aerolab cluster create -n mydc -c 3 -f features.conf

# Enable SC on all nodes
aerolab conf sc -n mydc

# Verify cluster formed
aerolab cluster list</code></pre>

        <h3>Network Configuration (Mesh Mode)</h3>
        <p>Each node needs to know about at least one other node to form a cluster:</p>
        <pre><code># In aerospike.conf (each node)
network {{
    heartbeat {{
        mode mesh
        address &lt;this_node_ip&gt;
        port 3002
        
        # List seed nodes
        mesh-seed-address-port &lt;node1_ip&gt; 3002
        mesh-seed-address-port &lt;node2_ip&gt; 3002
        mesh-seed-address-port &lt;node3_ip&gt; 3002
        
        interval 250
        timeout 10
    }}
}}</code></pre>

        <div class="info-box">
            <strong>Tip:</strong> Include the node's own address in mesh-seed list for consistent configuration across all nodes.
        </div>

        <h3>Verify Cluster Formation</h3>
        <pre><code># In ASADM
info

# Expected: All nodes show same Cluster Key and Cluster Size</code></pre>

        <h3>Configure SC Roster for Multi-Node</h3>
        <pre><code># Enable admin mode
enable

# Stage all observed nodes
manage roster stage observed ns test

# Apply roster
manage recluster

# Verify
show roster</code></pre>

        <h3>Recommended Configurations</h3>
        <table class="comparison-table">
            <tr><th>Nodes</th><th>RF</th><th>Fault Tolerance</th><th>Use Case</th></tr>
            <tr><td>2</td><td>2</td><td>0 nodes (no tolerance)</td><td>Dev/Test only</td></tr>
            <tr><td>3</td><td>2</td><td>1 node</td><td>Small production</td></tr>
            <tr><td>5</td><td>2</td><td>1-2 nodes</td><td>Medium production</td></tr>
            <tr><td>5</td><td>3</td><td>2 nodes</td><td>High availability</td></tr>
        </table>

        <h3>Capacity Planning</h3>
        <ul>
            <li>Each namespace should have same memory/disk on all nodes</li>
            <li>Total capacity = (single node capacity × nodes) / RF</li>
            <li>Account for migrations during maintenance</li>
        </ul>
        """
    },
    {
        "id": 14,
        "title": "Migrations & Rebalancing",
        "short": "Migrations",
        "icon": "",
        "category": "operations",
        "content": f"""
        <h3>What Are Migrations?</h3>
        <p>When the cluster membership changes, data must be <strong>migrated</strong> (rebalanced) across nodes to maintain proper replication.</p>

        <h3>When Migrations Occur</h3>
        <ul>
            <li>Node added to cluster</li>
            <li>Node removed from cluster</li>
            <li>Node failure/recovery</li>
            <li>Roster changes</li>
        </ul>

        <h3>Monitoring Migrations</h3>
        <pre><code># In ASADM - watch migration progress
show stat service like partitions_remaining -flip

# Detailed migration stats
show stat service like migrate -flip

# Continuous monitoring
watch 2 diff show stat service like migrate</code></pre>

        <h3>Migration Statistics Explained</h3>
        <table class="comparison-table">
            <tr><th>Stat</th><th>Meaning</th></tr>
            <tr><td><code>migrate_partitions_remaining</code></td><td>Partitions still to be migrated</td></tr>
            <tr><td><code>migrate_tx_partitions_active</code></td><td>Outgoing migrations in progress</td></tr>
            <tr><td><code>migrate_rx_partitions_active</code></td><td>Incoming migrations in progress</td></tr>
            <tr><td><code>migrate_allowed</code></td><td>Whether migrations are enabled</td></tr>
        </table>

        <h3>Migration Performance Tuning</h3>
        <pre><code># View current settings
show config namespace like migrate

# Adjust migration threads (requires restart)
# In aerospike.conf:
# migrate-threads 4</code></pre>

        <div class="warning-box">
            <strong>During Migrations:</strong>
            <ul>
                <li>Avoid making additional cluster changes</li>
                <li>Monitor system resources (CPU, network, disk I/O)</li>
                <li>Client latency may increase temporarily</li>
            </ul>
        </div>

        <h3>Try It: Monitor a Migration</h3>
        <pre><code># Check if any migrations are in progress
show stat service like partitions_remaining -flip

# View overall namespace health
info namespace</code></pre>

        <div class="success-box">
            Migrations are complete when <code>migrate_partitions_remaining = 0</code> on ALL nodes.
        </div>
        """
    },
    {
        "id": 15,
        "title": "SC Monitoring & Alerting",
        "short": "Monitoring",
        "icon": "",
        "category": "operations",
        "content": f"""
        <h3>Critical Metrics to Monitor</h3>
        <p>Proactive monitoring prevents data unavailability in SC clusters.</p>

        <div class="exercise-box">
            <h4>Exercise: Run a Complete Health Check</h4>
            <p>Perform this monitoring sequence in <strong>ASADM</strong> to assess cluster health:</p>
            
            <ol>
                <li><strong>Check partition health (CRITICAL):</strong>
                    <pre><code>show stat namespace for test like 'dead|unavailable' -flip</code></pre>
                    <div class="verify-box">Both values must be 0. If not, investigate immediately!</div>
                </li>
                <li><strong>Check clock synchronization (CRITICAL):</strong>
                    <pre><code>show stat service like clock_skew_stop_writes -flip</code></pre>
                    <div class="verify-box">Must be <code>false</code>. If <code>true</code>, fix NTP immediately!</div>
                </li>
                <li><strong>Verify cluster stability:</strong>
                    <pre><code>show stat -flip like cluster_size</code></pre>
                    <div class="verify-box"><code>cluster_size</code> must equal <code>ns_cluster_size</code> on all nodes.</div>
                </li>
                <li><strong>Check migration status:</strong>
                    <pre><code>show stat service like partitions_remaining -flip</code></pre>
                    <div class="verify-box">Should be 0 when cluster is stable.</div>
                </li>
                <li><strong>Review error rates:</strong>
                    <pre><code>show stat namespace like fail_ -flip</code></pre>
                    <div class="verify-box">Watch for increasing error counts over time.</div>
                </li>
            </ol>
        </div>

        <div class="warning-box">
            <strong>Alert Immediately If:</strong>
            <ul>
                <li><code>clock_skew_stop_writes = true</code> - Writes are blocked!</li>
                <li><code>dead_partitions > 0</code> - Data may be lost!</li>
                <li><code>unavailable_partitions > 0</code> for extended period - Service degraded!</li>
            </ul>
        </div>

        <h3>Recommended Alert Thresholds</h3>
        <table class="comparison-table">
            <tr><th>Metric</th><th>Warning</th><th>Critical</th></tr>
            <tr><td>dead_partitions</td><td>&gt;0</td><td>&gt;0</td></tr>
            <tr><td>unavailable_partitions</td><td>&gt;0 for 5min</td><td>&gt;0 for 15min</td></tr>
            <tr><td>migrate_partitions_remaining</td><td>&gt;1000 for 30min</td><td>&gt;1000 for 2hr</td></tr>
            <tr><td>clock_skew_stop_writes</td><td>true</td><td>true</td></tr>
            <tr><td>fail_generation rate</td><td>&gt;100/sec</td><td>&gt;1000/sec</td></tr>
        </table>

        <div class="exercise-box">
            <h4>Exercise: Check Error Statistics</h4>
            <p>Monitor error rates in <strong>ASADM</strong>:</p>
            
            <ol>
                <li>Check generation conflicts:
                    <pre><code>show stat namespace like fail_generation -flip</code></pre>
                </li>
                <li>Check key-busy errors:
                    <pre><code>show stat namespace like fail_key_busy -flip</code></pre>
                </li>
                <li>Check client errors:
                    <pre><code>show stat namespace like client_.*_error -flip</code></pre>
                </li>
            </ol>
            
            <div class="info-box">
                High error rates indicate application issues or cluster problems.
                Monitor trends over time rather than absolute values.
            </div>
        </div>
        """
    },
    {
        "id": 16,
        "title": "Best Practices",
        "short": "Best Practices",
        "icon": "",
        "category": "reference",
        "content": f"""
        <h3>Configuration Best Practices</h3>
        <ul>
            <li>Set <code>replication-factor >= 2</code> (RF=3 for critical production)</li>
            <li>Disable expiration (<code>default-ttl 0</code>) for critical data</li>
            <li>Consider <code>commit-to-device true</code> for maximum durability</li>
            <li>Use rack-awareness for multi-AZ/multi-datacenter deployments</li>
            <li>Ensure NTP is configured and monitored on all nodes</li>
        </ul>

        <h3>Operational Best Practices</h3>
        <ul>
            <li>Use generation checks for concurrent updates</li>
            <li>Handle InDoubt errors properly - always read to verify</li>
            <li>Use durable deletes (creates tombstones)</li>
            <li>Prefer Session Consistency unless you need Linearizable</li>
            <li>Add/remove one node at a time, wait for migrations</li>
            <li>Maintain documentation of roster changes</li>
        </ul>

        <h3>Monitoring Best Practices</h3>
        <ul>
            <li>Watch <code>dead_partitions</code> and <code>unavailable_partitions</code></li>
            <li>Monitor <code>client_write_error</code> and <code>client_read_error</code></li>
            <li>Track <code>fail_generation</code> for conflict rates</li>
            <li>Alert on <code>clock_skew_stop_writes</code></li>
            <li>Set up dashboards for migration progress</li>
        </ul>

        <h3>Things to Avoid</h3>
        <div class="warning-box">
            <ul>
                <li>Don't use non-durable deletes in production</li>
                <li>Don't enable client retransmit (can cause duplicates)</li>
                <li>Don't ignore InDoubt errors</li>
                <li>Don't switch from AP to SC on existing namespace</li>
                <li>Don't remove multiple nodes simultaneously (>= RF)</li>
                <li>Don't skip waiting for migrations to complete</li>
                <li>Don't use revive without understanding data loss implications</li>
            </ul>
        </div>

        <h3>Emergency Procedures</h3>
        <div class="card">
            <h4>If Partitions Become Unavailable:</h4>
            <ol>
                <li>Check which nodes are missing</li>
                <li>Attempt to restore the nodes</li>
                <li>If nodes cannot be restored, evaluate revive option</li>
                <li>Document and investigate root cause</li>
            </ol>
        </div>

        <div class="card">
            <h4>If Clock Skew Stops Writes:</h4>
            <ol>
                <li>Check NTP synchronization on all nodes</li>
                <li>Fix time synchronization issues</li>
                <li>Writes will resume automatically once clocks sync</li>
            </ol>
        </div>
        """
    },
    {
        "id": 17,
        "title": "Troubleshooting Guide",
        "short": "Troubleshooting",
        "icon": "",
        "category": "reference",
        "content": f"""
        <h3>Common Issues and Solutions</h3>

        <div class="card">
            <h4>Issue: Writes Failing with PARTITION_UNAVAILABLE</h4>
            <p><strong>Symptoms:</strong> Applications receiving PARTITION_UNAVAILABLE errors</p>
            <p><strong>Diagnosis:</strong></p>
            <pre><code>show stat namespace like unavailable -flip
show roster
info</code></pre>
            <p><strong>Solutions:</strong></p>
            <ul>
                <li>Check if all roster nodes are online</li>
                <li>Verify network connectivity between nodes</li>
                <li>Check if new nodes need to be added to roster</li>
            </ul>
        </div>

        <div class="card">
            <h4>Issue: Dead Partitions After Node Failure</h4>
            <p><strong>Symptoms:</strong> <code>dead_partitions > 0</code></p>
            <p><strong>Diagnosis:</strong></p>
            <pre><code>show stat namespace like dead -flip
show roster</code></pre>
            <p><strong>Solutions:</strong></p>
            <ul>
                <li>Try to restore the failed node</li>
                <li>If restoration impossible, use <code>manage revive ns test</code></li>
                <li>Plan for data recovery from backup</li>
            </ul>
        </div>

        <div class="card">
            <h4>Issue: Cluster Size Mismatch</h4>
            <p><strong>Symptoms:</strong> <code>cluster_size</code> != <code>ns_cluster_size</code></p>
            <p><strong>Diagnosis:</strong></p>
            <pre><code>show stat -flip like cluster_size
show roster</code></pre>
            <p><strong>Solutions:</strong></p>
            <ul>
                <li>New nodes need to be added to roster</li>
                <li>Run <code>manage roster stage observed ns test</code></li>
                <li>Run <code>manage recluster</code></li>
            </ul>
        </div>

        <div class="card">
            <h4>Issue: Migrations Not Completing</h4>
            <p><strong>Symptoms:</strong> <code>migrate_partitions_remaining</code> stuck or very slow</p>
            <p><strong>Diagnosis:</strong></p>
            <pre><code>show stat service like migrate -flip
show config namespace like migrate</code></pre>
            <p><strong>Solutions:</strong></p>
            <ul>
                <li>Check network bandwidth between nodes</li>
                <li>Check disk I/O on nodes</li>
                <li>Consider increasing migrate-threads (requires restart)</li>
                <li>Reduce client load during migration</li>
            </ul>
        </div>

        <div class="card">
            <h4>Issue: High Generation Conflict Rate</h4>
            <p><strong>Symptoms:</strong> High <code>fail_generation</code> count</p>
            <p><strong>Diagnosis:</strong></p>
            <pre><code>show stat namespace like fail_generation -flip</code></pre>
            <p><strong>Solutions:</strong></p>
            <ul>
                <li>Review application logic for concurrent writes</li>
                <li>Implement proper retry logic with generation checks</li>
                <li>Consider using CAS operations</li>
            </ul>
        </div>

        <h3>Useful Diagnostic Commands</h3>
        <pre><code># Complete cluster overview
info

# All namespace statistics
show stat namespace for test

# Configuration check
show config namespace for test

# Log inspection (on node)
tail -f /var/log/aerospike/aerospike.log | grep -i error</code></pre>
        """
    },
    {
        "id": 18,
        "title": "Clock Synchronization",
        "short": "Clock Sync",
        "icon": "",
        "category": "concepts",
        "content": f"""
        <h3>Why Clock Sync Matters in SC</h3>
        <p>Strong Consistency relies on a <strong>hybrid clock</strong> to order writes. If clocks drift too far apart, 
        SC guarantees can be violated.</p>

        <div class="warning-box">
            <strong>Critical Thresholds (default heartbeat configuration):</strong>
            <ul>
                <li><strong>≤10 seconds</strong> — Well within acceptable limits, no action needed</li>
                <li><strong>~12 seconds</strong> — Warnings logged to provide early notification</li>
                <li><strong>~17 seconds</strong> — <code>stop-writes</code> mode activated, writes are BLOCKED (forbidden error)</li>
                <li><strong>~23 seconds</strong> — Potential data loss if writes were somehow allowed</li>
            </ul>
            <p>These thresholds scale with the heartbeat <code>interval</code> (default 150ms) and 
            <code>timeout</code> (default 10). Changing those values changes the skew tolerances accordingly.
            The clock skew threshold for data loss is approximately 27 seconds with default settings.</p>
        </div>

        <h3>How Aerospike Protects You</h3>
        <p>Aerospike's gossip protocol continuously monitors clock skew between nodes:</p>
        <ul>
            <li>Detects drift before it becomes dangerous</li>
            <li>Sends alerts when skew is detected</li>
            <li>Disables writes at 20 seconds (before data loss at 27 seconds)</li>
        </ul>

        <div class="exercise-box">
            <h4>Exercise: Check Clock Skew Status</h4>
            <p>In <strong>ASADM</strong>, verify clock synchronization:</p>
            
            <ol>
                <li>Check if writes are blocked due to clock skew:
                    <pre><code>show stat service like clock_skew_stop_writes -flip</code></pre>
                    <div class="verify-box"><strong>Must be <code>false</code></strong>. If <code>true</code>, fix NTP immediately!</div>
                </li>
                <li>Check cluster time info:
                    <pre><code>info</code></pre>
                </li>
            </ol>
        </div>

        <h3>Causes of Clock Discontinuity</h3>
        <div class="card">
            <h4>Common Causes (AVOID THESE!):</h4>
            <ul>
                <li><strong>Administrator error</strong> - Manually setting clock far into future/past</li>
                <li><strong>Malfunctioning NTP</strong> - Time sync service not working</li>
                <li><strong>VM hibernation</strong> - Virtual machine suspended and resumed</li>
                <li><strong>Docker/Linux process pause</strong> - Container or process frozen</li>
                <li><strong>VM live migration</strong> - Moving VM between hosts without stopping</li>
            </ul>
        </div>

        <h3>Best Practices</h3>
        <ul>
            <li>Use NTP on all cluster nodes</li>
            <li>Monitor NTP synchronization status</li>
            <li>Avoid VM live migrations - stop Aerospike first, migrate, then restart</li>
            <li>Never use Docker pause or Linux process pause on Aerospike containers</li>
            <li>Set up alerts for clock skew warnings in logs</li>
        </ul>
        """
    },
    {
        "id": 19,
        "title": "Clean vs Unclean Shutdowns",
        "short": "Shutdowns",
        "icon": "",
        "category": "concepts",
        "content": f"""
        <h3>Understanding Shutdown Types</h3>
        <p>How a node shuts down has significant implications for SC data integrity.</p>

        <div class="card">
            <h4>Clean Shutdown</h4>
            <ul>
                <li>Initiated with <code>SIGTERM</code> signal</li>
                <li>Aerospike flushes all data to disk</li>
                <li>Properly signals other nodes in cluster</li>
                <li>Logs: <code>finished clean shutdown - exiting</code></li>
                <li><strong>No data loss risk</strong></li>
            </ul>
            <pre><code># Clean shutdown methods
systemctl stop aerospike
service aerospike stop
kill -TERM &lt;asd_pid&gt;</code></pre>
        </div>

        <div class="card">
            <h4>Unclean Shutdown</h4>
            <ul>
                <li>Server crash, power failure</li>
                <li><code>SIGKILL</code> (kill -9)</li>
                <li>Hardware failure</li>
                <li>Data in write buffer may be lost</li>
                <li><strong>Node gets "evade flag" (e-flag) on restart</strong></li>
            </ul>
            <pre><code># These cause UNCLEAN shutdowns - AVOID!
kill -9 &lt;asd_pid&gt;
docker kill &lt;container&gt;
Power outage</code></pre>
        </div>

        <h3>The Evade Flag (E-Flag)</h3>
        <p>When a node rejoins after an unclean shutdown:</p>
        <ul>
            <li>It's marked with an "evade flag"</li>
            <li>Its data is <strong>not immediately trusted</strong></li>
            <li>Node is not counted in super-majority calculations</li>
            <li>Unavailable partitions may become <strong>dead partitions</strong></li>
        </ul>

        <div class="warning-box">
            <strong>Critical Risk:</strong> If RF nodes all shut down uncleanly within <code>flush-max-ms</code> 
            (default ~1 second), writes in the buffer may be lost!
        </div>

        <div class="exercise-box">
            <h4>Exercise: Verify Clean Shutdown</h4>
            <p>Check your container logs to see shutdown messages:</p>
            
            <ol>
                <li>View recent logs in terminal:
                    <pre><code>docker logs aerolab-mydc_1 --tail 50</code></pre>
                </li>
                <li>Look for:
                    <div class="expected-output">finished clean shutdown - exiting</div>
                </li>
            </ol>
            
            <div class="info-box">
                Always use <code>docker stop</code> (sends SIGTERM) instead of <code>docker kill</code> (sends SIGKILL).
            </div>
        </div>
        """
    },
    {
        "id": 20,
        "title": "Commit-to-Device",
        "short": "Durability",
        "icon": "",
        "category": "concepts",
        "content": f"""
        <h3>What is Commit-to-Device?</h3>
        <p>By default, Aerospike considers a write complete when data is in the write buffer. 
        <code>commit-to-device</code> ensures data is flushed to storage before acknowledging the write.</p>

        <h3>Default Behavior (Without commit-to-device)</h3>
        <ul>
            <li>Write acknowledged when data reaches write buffer</li>
            <li>Higher performance</li>
            <li>Risk: Data in buffer can be lost if RF nodes crash simultaneously</li>
            <li>Time window for loss: <code>flush-max-ms</code> (typically ~1 second)</li>
        </ul>

        <h3>With commit-to-device Enabled</h3>
        <ul>
            <li>Write acknowledged only after flush to storage</li>
            <li>Simultaneous crashes cannot cause data loss</li>
            <li><strong>Never generates dead partitions from crashes</strong></li>
            <li>Performance penalty (flush on every write)</li>
        </ul>

        <h3>When to Use commit-to-device</h3>
        <table class="comparison-table">
            <tr><th>Scenario</th><th>Recommendation</th></tr>
            <tr><td>Low write throughput</td><td>Enable - minimal performance impact</td></tr>
            <tr><td>PMem storage</td><td>Enable - no noticeable performance penalty</td></tr>
            <tr><td>Shared memory (RAM) storage</td><td>Enable - no performance penalty (7.0.0+)</td></tr>
            <tr><td>High write throughput + SSD</td><td>Consider tradeoffs carefully</td></tr>
            <tr><td>Multi-AZ deployment with rack-awareness</td><td>May skip - reduced risk of simultaneous failures</td></tr>
        </table>

        <h3>Configuration</h3>
        <pre><code># In aerospike.conf namespace section:
namespace sc_namespace {{
    strong-consistency true
    
    # Enable for maximum durability
    commit-to-device true
    
    storage-engine device {{
        # ... device config
    }}
}}</code></pre>

        <div class="info-box">
            <strong>Tip:</strong> Rack-aware deployments across multiple Availability Zones reduce the 
            likelihood of RF nodes failing simultaneously, making commit-to-device less critical.
        </div>
        """
    },
    {
        "id": 21,
        "title": "Auto-Revive Feature",
        "short": "Auto-Revive",
        "icon": "",
        "category": "concepts",
        "content": f"""
        <h3>What is Auto-Revive?</h3>
        <p>Introduced in <strong>Aerospike Database 7.1.0</strong>, auto-revive automatically revives dead partitions 
        caused by unclean shutdowns, without operator intervention.</p>

        <h3>How It Works</h3>
        <ul>
            <li>Detects dead partitions caused by RF nodes with unclean shutdowns</li>
            <li>Automatically revives these partitions on startup</li>
            <li><strong>Selective:</strong> Does NOT revive partitions if storage was wiped</li>
            <li>Storage-wiped scenarios still require manual intervention</li>
        </ul>

        <h3>When Auto-Revive Helps</h3>
        <div class="card">
            <h4>Automatic Revival:</h4>
            <ul>
                <li>RF nodes crashed (unclean shutdown)</li>
                <li>All nodes restarted with data intact</li>
                <li>Dead partitions from the crash are auto-revived</li>
            </ul>
        </div>

        <div class="card">
            <h4>Manual Intervention Required:</h4>
            <ul>
                <li>Storage devices were wiped on RF nodes</li>
                <li>Data files were deleted</li>
                <li>Must manually recover data from backup, then revive</li>
            </ul>
        </div>

        <h3>Mitigating Unclean Shutdown Effects</h3>
        <p>To reduce or eliminate dead partitions from unclean shutdowns:</p>
        
        <ol>
            <li><strong>Enable commit-to-device</strong> - Crashes never cause dead partitions</li>
            <li><strong>Use rack-aware deployment</strong> - Reduces chance of RF nodes failing together</li>
            <li><strong>Use multi-AZ deployment</strong> - Each rack in different datacenter</li>
            <li><strong>Enable auto-revive</strong> - Automatic recovery from crash scenarios</li>
        </ol>

        <div class="info-box">
            <strong>Note:</strong> Auto-revive is safe to use with rack-aware multi-AZ deployments 
            where simultaneous RF node failures are unlikely.
        </div>
        """
    },
    {
        "id": 22,
        "title": "SC Limitations & Caveats",
        "short": "Limitations",
        "icon": "",
        "category": "concepts",
        "content": f"""
        <h3>Important SC Limitations</h3>
        <p>SC provides strong guarantees, but there are specific scenarios where guarantees don't apply.</p>

        <div class="warning-box">
            <strong>Non-Durable Deletes, Expiration & Eviction</strong>
            <p>These are <strong>NOT strongly consistent</strong>:</p>
            <ul>
                <li>Non-durable deletes don't create tombstones</li>
                <li>Data expiration (TTL)</li>
                <li>Data eviction</li>
            </ul>
            <p>Without tombstones, deleted data may "reappear" after network issues.</p>
            <p><strong>Recommendation:</strong> Disable expiration and eviction for SC namespaces, 
            use durable deletes only.</p>
        </div>

        <h3>If You Must Use Expiration</h3>
        <p>Enable with caution using:</p>
        <pre><code>strong-consistency-allow-expunge true</code></pre>
        <p>Only safe when there's a large time gap between writes and expiration.</p>

        <div class="card">
            <h4>UDF Limitations</h4>
            <ul>
                <li>UDF <strong>reads are NOT linearized</strong></li>
                <li>UDF writes that fail in certain ways may cause inconsistencies</li>
                <li>Use with caution in SC namespaces</li>
            </ul>
        </div>

        <div class="card">
            <h4>Secondary Index Queries</h4>
            <ul>
                <li>Queries may return <strong>stale reads</strong></li>
                <li>Queries may return <strong>dirty reads</strong> (uncommitted data)</li>
                <li>This is for performance - will be fixed in future releases</li>
                <li>Only affects queries, not direct record access</li>
            </ul>
        </div>

        <div class="warning-box">
            <strong>Client Retransmit - DISABLE IT!</strong>
            <p>If client write retransmission is enabled:</p>
            <ul>
                <li>Writes may be applied multiple times</li>
                <li>Can cause consistency violations</li>
                <li>May generate incorrect error codes</li>
            </ul>
            <p><strong>Recommendation:</strong> Disable client retransmit. Handle retries in your application 
            using read-modify-write pattern with generation checks.</p>
        </div>

        <h3>Durability Exceptions</h3>
        <p>These scenarios can cause data loss even with SC enabled:</p>

        <div class="card">
            <h4>Incorrect Roster Management</h4>
            <p>Reducing the roster by <code>replication-factor</code> or more nodes at a time may result in 
            record data loss. Always follow the safe add/remove procedures — remove one node at a time
            and wait for migrations.</p>
        </div>

        <div class="card">
            <h4>Partial Storage Erasure</h4>
            <p>If some sectors or portions of a drive are erased (e.g., malicious action or partial drive failure) 
            on RF or more nodes, Aerospike <strong>cannot detect the loss</strong>. Records may be silently lost.</p>
        </div>

        <div class="card">
            <h4>Simultaneous Server Restarts</h4>
            <p>By default, writes are buffered before flushing to disk. If RF nodes crash within 
            <code>flush-max-ms</code> of each other, buffered writes may be lost. Mitigate with 
            <code>commit-to-device true</code> or rack-aware multi-AZ deployments.</p>
        </div>

        <div class="card">
            <h4>Storage Hardware Failure</h4>
            <p>When all roster nodes are online but some partition data is missing (e.g., storage wiped 
            or lost while <code>asd</code> was down), partitions become <code>dead_partitions</code>. 
            Use <code>revive</code> or restore from backup.</p>
        </div>

        <h3>Per-Record Consistency</h3>
        <div class="info-box">
            SC guarantees are <strong>per-record only</strong>. There are no multi-record transaction semantics.
            Each write is atomic and isolated, but there's no way to atomically update multiple records.
            (Aerospike Database 8+ introduces multi-record transactions for SC namespaces.)
        </div>
        """
    },
    {
        "id": 23,
        "title": "SC Error Codes",
        "short": "Error Codes",
        "icon": "",
        "category": "reference",
        "content": f"""
        <h3>SC-Specific Error Codes</h3>
        <p>Understanding error codes is crucial for proper SC application development.</p>

        <h3>Data Unavailability Errors</h3>
        <table class="comparison-table">
            <tr><th>Error</th><th>Meaning</th><th>Action</th></tr>
            <tr>
                <td><code>PARTITION_UNAVAILABLE</code></td>
                <td>Server's cluster doesn't have the data partition</td>
                <td>Wait for cluster recovery or check roster</td>
            </tr>
            <tr>
                <td><code>INVALID_NODE_ERROR</code></td>
                <td>Client can't find a node for this partition</td>
                <td>Check cluster connectivity, validate roster</td>
            </tr>
            <tr>
                <td><code>TIMEOUT</code></td>
                <td>Operation timed out - may be network partition</td>
                <td>Check <code>InDoubt</code> flag, read to verify</td>
            </tr>
            <tr>
                <td><code>CONNECTION_ERROR</code></td>
                <td>Network issue - partition may be happening</td>
                <td>Persists until partition heals</td>
            </tr>
            <tr>
                <td><code>FORBIDDEN</code></td>
                <td>Writes blocked (usually clock skew)</td>
                <td>Check clock synchronization immediately</td>
            </tr>
        </table>

        <h3>The InDoubt Flag</h3>
        <p>All error returns include an <code>InDoubt</code> field:</p>
        <ul>
            <li><code>InDoubt = false</code> - Write was definitely NOT applied</li>
            <li><code>InDoubt = true</code> - Write MAY or MAY NOT have been applied</li>
        </ul>

        <div class="exercise-box">
            <h4>Exercise: Handle InDoubt Properly</h4>
            <p>When you receive an <code>InDoubt = true</code> error:</p>
            
            <ol>
                <li>Read the record to check its current state:
                    <pre><code>SELECT *, generation FROM test WHERE PK='your_key'</code></pre>
                </li>
                <li>Compare with expected state</li>
                <li>Decide whether to retry the write based on the read result</li>
            </ol>
            
            <div class="info-box">
                The InDoubt flag helps reduce unnecessary reads in high-stress situations.
                If <code>InDoubt = false</code>, you know the write failed - no need to read.
            </div>
        </div>

        <h3>When INVALID_NODE_ERROR Occurs</h3>
        <ul>
            <li>Seed node addresses are incorrect</li>
            <li>Client can't connect to any seed nodes</li>
            <li>Partition map doesn't contain the requested partition</li>
            <li>Roster is misconfigured</li>
            <li>Dead or unavailable partitions exist</li>
        </ul>

        <div class="exercise-box">
            <h4>Exercise: Diagnose Error Conditions</h4>
            <p>Check for common error causes in <strong>ASADM</strong>:</p>
            
            <ol>
                <li>Check partition availability:
                    <pre><code>show stat namespace like 'dead|unavailable' -flip</code></pre>
                </li>
                <li>Check clock skew:
                    <pre><code>show stat service like clock_skew -flip</code></pre>
                </li>
                <li>Verify roster configuration:
                    <pre><code>show roster</code></pre>
                </li>
            </ol>
        </div>
        """
    },
    {
        "id": 24,
        "title": "Performance Tuning",
        "short": "Performance",
        "icon": "",
        "category": "reference",
        "content": f"""
        <h3>SC Performance Characteristics</h3>
        <p>SC mode has similar performance to AP mode with these settings:</p>
        <ul>
            <li>Replication factor = 2</li>
            <li>Session Consistency (default)</li>
        </ul>

        <h3>Performance Impact Factors</h3>
        
        <div class="card">
            <h4>Replication Factor &gt; 2</h4>
            <p>Extra "replication advise" packets sent to acting replicas on every write.</p>
            <ul>
                <li>Master doesn't wait for response</li>
                <li>Extra network load</li>
                <li>Minimal latency impact</li>
            </ul>
        </div>

        <div class="card">
            <h4>Linearizable Reads</h4>
            <p>Master must verify state with every acting replica on every read.</p>
            <ul>
                <li>"Regime check" packets sent to all replicas</li>
                <li>Higher latency (~20-50% slower than session reads)</li>
                <li>Extra network load</li>
            </ul>
            <p><strong>Use only when absolutely necessary.</strong></p>
        </div>

        <div class="card">
            <h4>commit-to-device</h4>
            <p>Flush to storage on every write.</p>
            <ul>
                <li>Significant performance penalty for high-throughput SSD</li>
                <li>No penalty for PMem storage</li>
                <li>No penalty for shared memory storage (7.0.0+)</li>
            </ul>
        </div>

        <h3>Availability vs Performance</h3>
        <table class="comparison-table">
            <tr><th>Configuration</th><th>Copies Needed</th><th>Availability in Failure</th></tr>
            <tr>
                <td>RF=2, 2 nodes</td>
                <td>2</td>
                <td>None (both required)</td>
            </tr>
            <tr>
                <td>RF=2, 3+ nodes</td>
                <td>2</td>
                <td>1 node can fail</td>
            </tr>
            <tr>
                <td>RF=3, 5+ nodes</td>
                <td>3</td>
                <td>2 nodes can fail</td>
            </tr>
        </table>

        <div class="info-box">
            <strong>Why 3 copies during failure?</strong><br>
            During master promotion, SC requires: failed copy + new master + prospective replica.
            Without a third potential copy, partition may remain unavailable.
        </div>

        <h3>Optimization Recommendations</h3>
        <ul>
            <li>Use Session Consistency by default (98% of use cases)</li>
            <li>Reserve Linearizable for critical cross-client consistency needs</li>
            <li>Consider rack-aware deployment to allow skipping commit-to-device</li>
            <li>Use RF=2 for performance, RF=3 for critical availability</li>
            <li>Monitor latency metrics and adjust client timeouts accordingly</li>
        </ul>
        """
    },
    {
        "id": 25,
        "title": "Quiescing Nodes",
        "short": "Quiesce",
        "icon": "",
        "category": "operations",
        "content": f"""
        <p>
            Quiescing enables smooth master handoff before removing a node from the cluster,
            preventing transaction timeouts during maintenance operations.
        </p>

        <h3>What is Quiescing?</h3>
        <p>
            When a node is quiesced, it's placed at the end of every partition's succession list.
            This causes the quiesced node to hand off master status to a non-quiesced node.
        </p>
        
        <div class="info-box">
            <strong>Key Benefits:</strong>
            <ul>
                <li>Prevents "master gap" - time when no master is available</li>
                <li>Transactions are proxied during handoff instead of timing out</li>
                <li>Quiesced node keeps data for faster re-sync when it returns</li>
            </ul>
        </div>

        <h3>Quiesce Procedure</h3>

        <div class="exercise-box">
            <h4>Step 1: Verify Cluster is Stable</h4>
            <p>Check no migrations are in progress:</p>
            <pre><code>Admin> info network</code></pre>
            <p>Ensure all nodes show same cluster key and Migrations = 0</p>
        </div>

        <div class="exercise-box">
            <h4>Step 2: Issue Quiesce Command</h4>
            <p>Quiesce the node you want to remove:</p>
            <pre><code>Admin+> manage quiesce with &lt;node-ip-or-name&gt;</code></pre>
            
            <p>Verify with:</p>
            <pre><code>Admin+> show statistics like pending_quiesce</code></pre>
            <p>Should show <code>pending_quiesce=true</code> for the target node.</p>
        </div>

        <div class="exercise-box">
            <h4>Step 3: Trigger Recluster</h4>
            <p>This performs the master handoff:</p>
            <pre><code>Admin+> manage recluster</code></pre>
            
            <p>Verify with:</p>
            <pre><code>Admin+> show statistics like quiesce</code></pre>
            <p>Check <code>effective_is_quiesced=true</code> and <code>nodes_quiesced=1</code></p>
        </div>

        <div class="exercise-box">
            <h4>Step 4: Wait for Proxy Completion</h4>
            <p>Check traffic has moved away from quiesced node:</p>
            <pre><code>Admin+> show latencies</code></pre>
            <p>ops/sec should be 0 for the quiesced node.</p>
            
            <p>Check proxies have completed:</p>
            <pre><code>Admin+> show statistics like client_proxy</code></pre>
            <p>Counters should stop incrementing.</p>
        </div>

        <div class="exercise-box">
            <h4>Step 5: Stop the Node</h4>
            <p>Now safe to stop the quiesced node:</p>
            <pre><code>systemctl stop aerospike</code></pre>
            <p>Or for Docker: <code>docker stop &lt;container&gt;</code></p>
        </div>

        <h3>Undoing a Quiesce</h3>
        <p>If you quiesced the wrong node:</p>
        <pre><code>Admin+> manage quiesce undo with &lt;node&gt;</code></pre>

        <div class="warning-box">
            <strong>Important Notes:</strong>
            <ul>
                <li>Quiescing affects ALL namespaces on the node</li>
                <li>Cannot quiesce individual namespaces</li>
                <li>If all nodes are quiesced, recluster is ignored</li>
                <li>For RF1 namespaces, wait for migrations before stopping</li>
            </ul>
        </div>

        <h3>Quiescing for Extra Durability</h3>
        <p>
            In RF2 clusters, quiescing before node removal ensures two full copies exist
            when the node is removed. This provides protection if another node fails
            before the first returns.
        </p>

        <h3>Try It: Simulate Node Maintenance</h3>
        <p>Use the Manage Cluster button to scale down - it will automatically quiesce nodes!</p>
        """
    },
    {
        "id": 26,
        "title": "Rack Awareness for SC",
        "short": "Rack Awareness",
        "icon": "",
        "category": "operations",
        "content": f"""
        <h3>Why Rack Awareness?</h3>
        <p>Rack awareness places master and replica copies on separate racks (typically different 
        Availability Zones). This reduces the chance of RF nodes failing simultaneously and enables 
        rack-local reads to cut cross-zone network costs.</p>

        <h3>How Racks Work in SC</h3>
        <p>In SC mode, rack information is carried <strong>on the roster</strong> as <code>node-id@rack-id</code> pairs.
        The rack-id in the config file populates the <code>observed_nodes</code> list, which you then 
        stage as the roster.</p>

        <h3>Step 1: Configure rack-id on Each Node</h3>
        <pre><code># In aerospike.conf (each node)
namespace test {{
    replication-factor 2
    strong-consistency true
    rack-id 101          # Set per-node rack identity
    
    storage-engine device {{
        file /opt/aerospike/data/test.dat
        filesize 4G
    }}
}}</code></pre>

        <div class="info-box">
            <strong>Note:</strong> In SC mode, the <code>rack-id</code> config is only used to populate
            the <code>observed_nodes</code> list. The actual rack assignment comes from what is set
            in the roster at the time of <code>recluster</code>.
        </div>

        <h3>Step 2: Set the Roster with Rack IDs</h3>
        <pre><code># In ASADM:
enable

# Stage observed nodes (includes @rack-id automatically)
manage roster stage observed ns test

# Apply
manage recluster

# Verify racks
show racks</code></pre>

        <h3>Dynamic Rack Reassignment</h3>
        <p>You can change rack assignments at runtime without restarting nodes:</p>
        <pre><code># Assign nodes to rack 101
manage config namespace test param rack-id to 101 with &lt;node1_ip&gt; &lt;node2_ip&gt;

# Assign other nodes to rack 102
manage config namespace test param rack-id to 102 with &lt;node3_ip&gt;

# Re-roster and recluster to apply
manage roster stage observed ns test
manage recluster</code></pre>

        <h3>Rack-Aware Reads (Client Configuration)</h3>
        <p>Clients can prefer reading from the local rack to reduce cross-zone traffic:</p>
        <pre><code># Python example
read_policy = {{
    'read_mode_sc': aerospike.POLICY_READ_MODE_SC_ALLOW_REPLICA,
    'replica': aerospike.POLICY_REPLICA_PREFER_RACK
}}

# Set rack ID when connecting
config = {{
    'hosts': [('node1', 3000)],
    'policies': {{'read': read_policy}},
    'rack_id': 101,
    'rack_aware': True
}}</code></pre>

        <div class="info-box">
            <strong>Best Practice:</strong> Use <code>ALLOW_REPLICA</code> read mode with 
            <code>PREFER_RACK</code> to get rack-local reads. This prevents read timeouts 
            during node failures and reduces cross-AZ network costs.
        </div>

        <h3>Active Rack (Database 7.2.0+)</h3>
        <p>The <code>active-rack</code> feature designates one rack to hold <strong>all master partitions</strong>. 
        This concentrates write processing on specific nodes for workload optimization.</p>
        <pre><code># In aerospike.conf
namespace test {{
    strong-consistency true
    rack-id 1
    active-rack 1        # All masters go to rack 1 nodes
}}</code></pre>
        <p>After configuration, re-roster and recluster. Verify with <code>show pmap</code> — 
        all Primary partitions should be on the active-rack nodes.</p>

        <div class="warning-box">
            <strong>Requirements:</strong>
            <ul>
                <li>All nodes must agree on the same active rack value</li>
                <li>Number of racks must be ≤ replication-factor</li>
                <li><code>active-rack = 0</code> disables the feature (rack 0 cannot be active)</li>
            </ul>
        </div>
        """
    },
    {
        "id": 27,
        "title": "Partition Regimes & Hybrid Clock",
        "short": "Regimes & Clock",
        "icon": "",
        "category": "concepts",
        "content": f"""
        <h3>How SC Orders Writes</h3>
        <p>Aerospike uses a <strong>hybrid clock</strong> per record to ensure correct ordering, 
        even across cluster changes and split-brain scenarios.</p>

        <h3>The Record Clock</h3>
        <p>Each record stores a 56-bit clock composed of three parts:</p>
        <table class="comparison-table">
            <tr><th>Component</th><th>Bits</th><th>Purpose</th></tr>
            <tr>
                <td>Last Update Time (LUT)</td>
                <td>40 bits</td>
                <td>Wall-clock timestamp of the write</td>
            </tr>
            <tr>
                <td>Partition Regime</td>
                <td>6 bits</td>
                <td>Increments on every master handoff for this partition</td>
            </tr>
            <tr>
                <td>Record Generation</td>
                <td>10 bits</td>
                <td>Write count for the record</td>
            </tr>
        </table>

        <p>The combination of regime + LUT + generation provides an unambiguous ordering 
        of every version of every record, even during cluster transitions.</p>

        <h3>What is a Partition Regime?</h3>
        <p>When a master handoff occurs (e.g., node failure, recluster), the <strong>regime</strong> for 
        that partition is incremented. This means:</p>
        <ul>
            <li>Old master writes have a lower regime than new master writes</li>
            <li>During a split-brain, only the sub-cluster with quorum can increment the regime</li>
            <li>Any stale writes from an old master are superseded by the higher regime</li>
        </ul>

        <div class="info-box">
            <strong>Why 6 bits?</strong> 6 bits provides ~64 regime changes. With a heartbeat interval of 
            150ms × timeout of 10 = 1.5s per cluster change cycle, 6 bits covers about 27 seconds 
            of clock resolution — the same window as the clock skew safety threshold.
        </div>

        <h3>How Linearizable Reads Use Regimes</h3>
        <p>When a linearizable read is requested:</p>
        <ol>
            <li>The master sends "regime check" packets to all replicas</li>
            <li>If all regimes agree, the read is current — return it</li>
            <li>If regimes disagree, a cluster change may be in progress — the client retries</li>
        </ol>

        <h3>How Session Consistency Uses Regimes</h3>
        <p>The client SDK stores the partition regime in its local partition table:</p>
        <ul>
            <li>On each read, the client records the regime it saw</li>
            <li>If a subsequent read returns a <em>lower</em> regime, the client rejects it</li>
            <li>This prevents reading from a stale master during master overhang</li>
        </ul>

        <div class="exercise-box">
            <h4>Exercise: View Partition Map</h4>
            <p>Check the partition distribution in <strong>ASADM</strong>:</p>
            <pre><code>show pmap</code></pre>
            <p>Each node shows Primary (master) and Secondary (replica) partition counts. 
            During a cluster change, you may see Unavailable counts temporarily.</p>
        </div>
        """
    },
    {
        "id": 28,
        "title": "Full vs Subset Partitions",
        "short": "Partition Subsets",
        "icon": "",
        "category": "concepts",
        "content": f"""
        <h3>Full and Subset Partitions</h3>
        <p>In steady state, partitions are <strong>full</strong> — they contain all relevant data.
        During cluster changes (rolling upgrades, node failures), some partitions become <strong>subsets</strong>.</p>

        <h3>When Subsets Occur</h3>
        <p>Consider a 5-node cluster with RF=2, where partition <em>q</em> has:</p>
        <ul>
            <li>Node A = roster-master (full)</li>
            <li>Node B = roster-replica (full)</li>
        </ul>

        <p><strong>Rolling upgrade scenario:</strong></p>
        <ol>
            <li>Node A goes down for upgrade → Node B promotes to master, Node C becomes alternate replica (<strong>subset</strong>)</li>
            <li>Node A returns (with stale data = <strong>subset</strong>), Node B goes down for its upgrade</li>
            <li>Now: Node A (roster-master, <strong>subset</strong>) + Node C (alternate replica, <strong>subset</strong>)</li>
        </ol>

        <div class="info-box">
            <strong>Key rule:</strong> In a super-majority sub-cluster (fewer than RF nodes missing), 
            a combination of subset partitions is sufficient because every write was committed to 
            at least RF nodes, and at most one node was down at any time. All changes are 
            present across the remaining nodes.
        </div>

        <h3>Impact on Reads</h3>
        <ul>
            <li>When master has a <strong>full</strong> partition — reads are served directly</li>
            <li>When master has a <strong>subset</strong> — each read must be resolved record-by-record 
            against other subset nodes, adding temporary overhead</li>
            <li><strong>Write overhead is never increased</strong> — Aerospike always writes to all copies</li>
        </ul>

        <h3>Partition Availability Rules (Refined)</h3>
        <table class="comparison-table">
            <tr><th>Scenario</th><th>Partition Available?</th></tr>
            <tr>
                <td>Both roster-master and roster-replica present, full partition exists</td>
                <td>Yes</td>
            </tr>
            <tr>
                <td>Majority sub-cluster with roster-master or roster-replica + full partition</td>
                <td>Yes</td>
            </tr>
            <tr>
                <td>Half the roster + roster-master present + full partition</td>
                <td>Yes</td>
            </tr>
            <tr>
                <td>Super-majority (fewer than RF nodes missing) + subset partitions</td>
                <td>Yes</td>
            </tr>
        </table>

        <h3>Evade Flag (E-Flag)</h3>
        <p>Certain nodes are excluded from majority/super-majority counting:</p>
        <ul>
            <li>Nodes with empty drives or brand-new nodes (no data)</li>
            <li>Nodes that had an unclean shutdown (unless <code>commit-to-device</code> is enabled)</li>
        </ul>
        <p>These nodes have the "evade flag" set until they are properly inducted with synchronized data.</p>
        """
    },
    {
        "id": 29,
        "title": "Node ID Assignment",
        "short": "Node IDs",
        "icon": "",
        "category": "setup",
        "content": f"""
        <h3>Why Assign Node IDs?</h3>
        <p>By default, Aerospike generates node IDs from the server's MAC address and fabric port.
        For SC clusters, <strong>manually assigning node IDs is recommended</strong> because:</p>
        <ul>
            <li>Hardware-generated IDs change if you replace hardware</li>
            <li>Readable IDs make roster management easier</li>
            <li>Cloud environments (AWS) benefit from stable IDs tied to EBS volumes</li>
        </ul>

        <h3>Configuring Node IDs</h3>
        <pre><code># In aerospike.conf (service stanza)
service {{
    node-id a1       # 1-16 character hex value
    cluster-name mydc
}}</code></pre>

        <div class="info-box">
            <strong>Valid node-id values:</strong> 1 to 16 hexadecimal characters.
            <code>01</code>, <code>B2</code>, <code>beef</code> are valid.
            <code>fred</code> is NOT valid (not hex).
            Duplicate node-ids are rejected — the second node cannot join.
        </div>

        <h3>Changing Node IDs on an Existing SC Cluster</h3>
        <p>To convert from auto-generated to assigned IDs without data unavailability:</p>
        <ol>
            <li>Update one server's config with the new <code>node-id</code></li>
            <li>Restart that server</li>
            <li>Update and commit the roster with the new node ID</li>
            <li>Repeat for the next server</li>
        </ol>

        <div class="warning-box">
            <strong>Important:</strong>
            <ul>
                <li>Change one node at a time — do NOT change all at once</li>
                <li>You don't have to wait for data migration to finish</li>
                <li>But you <strong>must</strong> validate and apply the new roster before moving to the next node</li>
                <li><code>node-id</code> and <code>node-id-interface</code> are mutually exclusive</li>
            </ul>
        </div>

        <h3>Viewing Node IDs</h3>
        <pre><code># In ASADM
show roster

# The Node ID column shows each node's ID
# In asinfo
asinfo -v "node"</code></pre>
        """
    }
]


# =============================================================================
# API ROUTES
# =============================================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main tutorial page."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "lessons": LESSONS
    })


@app.get("/api/lessons")
async def get_lessons():
    """Get all lessons."""
    return {"lessons": LESSONS}


@app.get("/api/lessons/{lesson_id}")
async def get_lesson(lesson_id: int):
    """Get a specific lesson."""
    if 0 <= lesson_id < len(LESSONS):
        return {"lesson": LESSONS[lesson_id]}
    return {"error": "Lesson not found"}


@app.get("/api/cluster/status")
async def get_cluster_status():
    """Get cluster status with diagnostics."""
    try:
        container = detect_container()
        if not container:
            return {"status": "error", "message": "No AeroLab container detected"}

        # Count running aerolab containers
        container_count = 0
        container_names = []
        try:
            count_result = subprocess.run(
                ['docker', 'ps', '--filter', 'name=aerolab-', '--format', '{{.Names}}'],
                capture_output=True, text=True, timeout=5
            )
            if count_result.returncode == 0:
                container_names = [n.strip() for n in count_result.stdout.strip().split('\n') if n.strip()]
                container_count = len(container_names)
        except Exception:
            pass

        # Get namespace info
        ns_result = subprocess.run(
            ['docker', 'exec', container, 'asinfo', '-v', 'namespace/test'],
            capture_output=True, text=True, timeout=5
        )

        # Get cluster_size from statistics
        cluster_size = 0
        try:
            cs_result = subprocess.run(
                ['docker', 'exec', container, 'asinfo', '-v', 'statistics'],
                capture_output=True, text=True, timeout=5
            )
            if cs_result.returncode == 0:
                for item in cs_result.stdout.strip().split(';'):
                    if '=' in item:
                        k, v = item.split('=', 1)
                        if k.strip() == 'cluster_size':
                            cluster_size = int(v.strip())
                            break
        except Exception:
            pass

        # Collect warnings from recent logs
        warnings = []
        try:
            log_result = subprocess.run(
                ['docker', 'exec', container, 'tail', '-100', '/var/log/aerospike.log'],
                capture_output=True, text=True, timeout=5
            )
            if log_result.returncode == 0:
                seen = set()
                for line in log_result.stdout.strip().split('\n'):
                    if 'WARNING' in line or 'FAILED' in line:
                        # Deduplicate by core message
                        core = line.split(')', 1)[-1].strip() if ')' in line else line
                        if core not in seen:
                            seen.add(core)
                            warnings.append(line.strip())
        except Exception:
            pass

        # Build diagnostics
        diagnostics = []
        if cluster_size < container_count and container_count > 1:
            diagnostics.append(
                f"Cluster not fully formed: Aerospike sees {cluster_size} node(s) but {container_count} containers are running. "
                "Check heartbeat/fabric network config (address must be 'any', not 'local')."
            )
        node_count = max(cluster_size, container_count)

        if ns_result.returncode == 0:
            info = ns_result.stdout.strip()
            params = {}
            for item in info.split(';'):
                if '=' in item:
                    k, v = item.split('=', 1)
                    params[k] = v

            ns_cluster = int(params.get('ns_cluster_size', 0))
            dead = int(params.get('dead_partitions', 0))
            unavail = int(params.get('unavailable_partitions', 0))

            if dead > 0:
                diagnostics.append(f"{dead} dead partitions detected — potential data loss.")
            if unavail > 0:
                diagnostics.append(f"{unavail} unavailable partitions — some data is unreachable.")
            if ns_cluster == 0 and cluster_size > 0:
                diagnostics.append("Roster not set. Run 'manage roster' in ASADM to activate SC.")

            return {
                "status": "ok",
                "container": container,
                "strong_consistency": params.get('strong-consistency', 'false') == 'true',
                "replication_factor": params.get('replication-factor', 'N/A'),
                "cluster_size": node_count,
                "aerospike_cluster_size": cluster_size,
                "container_count": container_count,
                "ns_cluster_size": ns_cluster,
                "dead_partitions": dead,
                "unavailable_partitions": unavail,
                "objects": int(params.get('objects', 0)),
                "tombstones": int(params.get('tombstones', 0)),
                "diagnostics": diagnostics,
                "warnings": warnings[-10:]  # last 10 unique warnings
            }
        else:
            return {"status": "error", "message": ns_result.stderr, "diagnostics": diagnostics, "warnings": warnings[-10:]}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# =============================================================================
# CLUSTER SETUP API
# =============================================================================

@app.get("/api/setup/check-prerequisites")
async def check_prerequisites():
    """Check if Docker and AeroLab are available."""
    result = {
        "docker": {"installed": False, "running": False, "version": None},
        "aerolab": {"installed": False, "version": None},
        "existing_cluster": None,
        "feature_key": False
    }
    
    # Check Docker installed
    try:
        docker_version = subprocess.run(
            ['docker', '--version'],
            capture_output=True, text=True, timeout=5
        )
        if docker_version.returncode == 0:
            result["docker"]["installed"] = True
            result["docker"]["version"] = docker_version.stdout.strip()
    except FileNotFoundError:
        result["docker"]["installed"] = False
    except Exception as e:
        print(f"Docker version check error: {e}")
    
    # Check Docker running
    if result["docker"]["installed"]:
        try:
            docker_ping = subprocess.run(
                ['docker', 'info'],
                capture_output=True, text=True, timeout=10
            )
            result["docker"]["running"] = docker_ping.returncode == 0
        except Exception as e:
            print(f"Docker info check error: {e}")
            result["docker"]["running"] = False
    
    # Check AeroLab installed
    try:
        aerolab_version = subprocess.run(
            ['aerolab', 'version'],
            capture_output=True, text=True, timeout=5
        )
        if aerolab_version.returncode == 0:
            result["aerolab"]["installed"] = True
            result["aerolab"]["version"] = aerolab_version.stdout.strip()
    except FileNotFoundError:
        result["aerolab"]["installed"] = False
    except Exception as e:
        print(f"AeroLab version check error: {e}")
    
    # Check for existing cluster
    try:
        container = detect_container()
        if container:
            result["existing_cluster"] = container
    except Exception as e:
        print(f"Container detection error: {e}")
    
    # Check for feature key file
    feature_key_paths = [
        os.path.join(BASE_DIR, '..', 'aerolab-setup', 'features.conf'),
        os.path.join(BASE_DIR, '..', 'features.conf'),
        os.path.expanduser('~/features.conf'),
    ]
    for path in feature_key_paths:
        try:
            if os.path.exists(path):
                result["feature_key"] = os.path.abspath(path)
                break
        except Exception:
            pass
    
    return result


@app.post("/api/setup/create-cluster")
async def create_cluster(request: Request):
    """Create a new SC cluster using AeroLab (non-streaming fallback)."""
    # This endpoint is kept for compatibility but we prefer WebSocket streaming
    return {"success": False, "error": "Please use the WebSocket endpoint for cluster creation"}


@app.websocket("/ws/setup/create-cluster")
async def create_cluster_ws(websocket: WebSocket):
    """Create a new SC cluster using AeroLab with real-time streaming."""
    await websocket.accept()
    
    async def send_log(message: str):
        await websocket.send_json({"type": "log", "data": message})
    
    async def send_step(step: str, status: str, message: str = None):
        await websocket.send_json({"type": "step", "step": step, "status": status, "message": message})
    
    async def send_result(success: bool, message: str):
        await websocket.send_json({"type": "result", "success": success, "message": message})
    
    try:
        # Wait for configuration from client
        config_msg = await websocket.receive_json()
        cluster_name = config_msg.get("cluster_name", "mydc")
        node_count = config_msg.get("node_count", 1)
        feature_key_path = config_msg.get("feature_key_path")
        
        async def run_cmd_streaming(cmd, step_name):
            """Run command and stream output in real-time."""
            await send_step(step_name, "running")
            await send_log(f"$ {' '.join(cmd)}")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            
            # Stream output line by line
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                decoded = line.decode('utf-8', errors='replace').rstrip()
                if decoded:
                    await send_log(decoded)
            
            await process.wait()
            return process.returncode
        
        # Step 1: Configure AeroLab backend
        returncode = await run_cmd_streaming(
            ['aerolab', 'config', 'backend', '-t', 'docker'],
            "Configuring AeroLab backend..."
        )
        if returncode != 0:
            await send_step("Configuring AeroLab backend...", "error")
            await send_result(False, "Failed to configure backend")
            return
        await send_step("Configuring AeroLab backend...", "done")
        
        # Step 2: Check if cluster exists
        await send_step("Checking for existing cluster...", "running")
        await send_log(f"$ aerolab cluster list")
        
        result = subprocess.run(['aerolab', 'cluster', 'list'], capture_output=True, text=True, timeout=30)
        if result.stdout:
            await send_log(result.stdout.strip())
        
        if cluster_name in result.stdout:
            await send_step("Checking for existing cluster...", "skip", f"Cluster '{cluster_name}' exists")
            await send_log(f"Cluster '{cluster_name}' already exists, configuring SC...")
            
            # Just configure SC if cluster exists
            returncode = await run_cmd_streaming(
                ['aerolab', 'conf', 'sc', '-n', cluster_name],
                "Configuring Strong Consistency..."
            )
            await send_step("Configuring Strong Consistency...", "done" if returncode == 0 else "error")
            await send_result(returncode == 0, f"Cluster '{cluster_name}' configured for SC")
            return
        
        await send_step("Checking for existing cluster...", "done")
        
        # Step 3: Create cluster
        cmd = ['aerolab', 'cluster', 'create', '-n', cluster_name, '-c', str(node_count)]
        if feature_key_path and os.path.exists(feature_key_path):
            cmd.extend(['-f', feature_key_path])
        
        returncode = await run_cmd_streaming(cmd, f"Creating {node_count}-node cluster...")
        if returncode != 0:
            await send_step(f"Creating {node_count}-node cluster...", "error")
            await send_result(False, "Failed to create cluster")
            return
        await send_step(f"Creating {node_count}-node cluster...", "done")
        
        # Step 4: Configure SC
        returncode = await run_cmd_streaming(
            ['aerolab', 'conf', 'sc', '-n', cluster_name],
            "Configuring Strong Consistency..."
        )
        if returncode != 0:
            await send_step("Configuring Strong Consistency...", "error")
            await send_result(False, "Failed to configure SC")
            return
        await send_step("Configuring Strong Consistency...", "done")
        
        # Step 5: Wait for cluster to be ready
        await send_step("Waiting for cluster to be ready...", "running")
        await send_log("Waiting for Aerospike to start...")
        
        import time
        for i in range(15):
            await asyncio.sleep(2)
            container = detect_container()
            if container:
                test = subprocess.run(
                    ['docker', 'exec', container, 'asinfo', '-v', 'status'],
                    capture_output=True, text=True, timeout=5
                )
                if test.returncode == 0 and 'ok' in test.stdout.lower():
                    await send_log(f"Aerospike ready after {(i+1)*2}s")
                    break
            await send_log(f"Waiting... ({(i+1)*2}s)")
        
        await send_step("Waiting for cluster to be ready...", "done")
        
        # Step 6: Install Python client
        await send_step("Installing Python client...", "running")
        container = detect_container()
        if container:
            # First install pip if needed
            await send_log("Installing pip...")
            subprocess.run(
                ['docker', 'exec', container, 'apt-get', 'update', '-qq'],
                capture_output=True, text=True, timeout=60
            )
            subprocess.run(
                ['docker', 'exec', container, 'apt-get', 'install', '-y', 'python3-pip', '-qq'],
                capture_output=True, text=True, timeout=120
            )
            
            # Install aerospike Python client
            await send_log("Installing aerospike Python client...")
            install_result = subprocess.run(
                ['docker', 'exec', container, 'pip3', 'install', 'aerospike', '--break-system-packages', '-q'],
                capture_output=True, text=True, timeout=120
            )
            if install_result.returncode == 0:
                await send_log("Aerospike Python client installed successfully")
            else:
                await send_log(f"Python client install note: {install_result.stderr[:100] if install_result.stderr else 'completed'}")
        await send_step("Installing Python client...", "done")
        
        await send_result(True, f"SC cluster '{cluster_name}' created successfully!")
        
    except WebSocketDisconnect:
        pass
    except Exception as e:
        import traceback
        await send_log(f"Error: {str(e)}")
        await send_result(False, str(e))


@app.post("/api/setup/destroy-cluster")
async def destroy_cluster(request: Request):
    """Destroy an existing cluster."""
    try:
        body = await request.json()
        cluster_name = body.get("cluster_name", "mydc")
        
        result = subprocess.run(
            ['aerolab', 'cluster', 'destroy', '-n', cluster_name, '-f'],
            capture_output=True, text=True, timeout=60
        )
        
        if result.returncode == 0:
            return {"success": True, "message": f"Cluster '{cluster_name}' destroyed"}
        else:
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.websocket("/ws/cluster/scale")
async def scale_cluster_ws(websocket: WebSocket):
    """Scale cluster up or down with live logging."""
    await websocket.accept()
    
    async def send_log(message: str):
        await websocket.send_json({"type": "log", "data": message})
    
    async def send_status(message: str):
        await websocket.send_json({"type": "status", "data": message})
    
    async def send_complete(success: bool, message: str = ""):
        await websocket.send_json({"type": "complete", "success": success, "message": message})
    
    async def run_cmd_logged(cmd: list) -> tuple:
        """Run a command and stream output to WebSocket."""
        await send_log(f"$ {' '.join(cmd)}")
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            
            output = ""
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                decoded = line.decode().rstrip()
                output += decoded + "\n"
                await send_log(decoded)
            
            await process.wait()
            return process.returncode, output
        except Exception as e:
            await send_log(f"Error: {str(e)}")
            return 1, str(e)
    
    try:
        # Get scaling parameters
        data = await websocket.receive_json()
        action = data.get("action")  # 'scale_up' or 'scale_down'
        current_count = data.get("current_count", 1)
        target_count = data.get("target_count", 1)
        cluster_name = "mydc"  # Default AeroLab cluster name
        
        await send_status(f"{'Adding' if action == 'scale_up' else 'Removing'} node...")
        await send_log(f"=== Cluster Scaling: {current_count} → {target_count} nodes ===")
        await send_log("")
        
        if action == 'scale_up':
            # Scale up: Add nodes using aerolab
            nodes_to_add = target_count - current_count
            await send_log(f"Adding {nodes_to_add} node(s) to cluster...")
            await send_log("")
            
            # Step 1: Use aerolab cluster grow with features file
            await send_status("Growing cluster...")
            
            # Find features file
            feature_key_path = None
            possible_paths = [
                './aerolab-setup/features.conf',
                '/Users/ssuman/stronconsistancy/aerolab-setup/features.conf',
                os.path.expanduser('~/features.conf')
            ]
            for p in possible_paths:
                if os.path.exists(p):
                    feature_key_path = p
                    break
            
            grow_cmd = ['aerolab', 'cluster', 'grow', '-n', cluster_name, '-c', str(nodes_to_add)]
            if feature_key_path:
                grow_cmd.extend(['-f', feature_key_path])
                await send_log(f"Using features file: {feature_key_path}")
            
            returncode, _ = await run_cmd_logged(grow_cmd)
            
            if returncode != 0:
                await send_log("")
                await send_log("ERROR: Failed to add nodes")
                await send_complete(False, "Failed to add nodes")
                return
            
            await send_log("")
            await send_log("Nodes added successfully")
            
            # Step 2: Wait for nodes to start
            await send_status("Waiting for nodes to start...")
            await send_log("")
            await send_log("Waiting for new nodes to start Aerospike...")
            await asyncio.sleep(5)
            
            # Step 3: Configure SC on ALL nodes (including new ones)
            # Use timeout to prevent hanging
            await send_status("Configuring Strong Consistency...")
            await send_log("")
            await send_log("=== Configuring SC on all nodes ===")
            await send_log("This may take 30-60 seconds...")
            
            try:
                process = await asyncio.create_subprocess_exec(
                    'aerolab', 'conf', 'sc', '-n', cluster_name,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT
                )
                
                try:
                    # Wait with timeout
                    stdout, _ = await asyncio.wait_for(process.communicate(), timeout=90)
                    await send_log(stdout.decode() if stdout else "SC configuration complete")
                    returncode = process.returncode
                except asyncio.TimeoutError:
                    await send_log("WARNING: SC configuration timed out, continuing...")
                    process.kill()
                    returncode = 1
            except Exception as e:
                await send_log(f"SC configuration error: {e}")
                returncode = 1
            
            if returncode != 0:
                await send_log("Note: SC configuration had issues, will try manual roster update")
            
            # Step 4: Wait for cluster to reform
            await send_status("Waiting for cluster to form...")
            await send_log("")
            await send_log("Waiting for cluster to reform with new nodes...")
            await asyncio.sleep(5)
            
            # Step 5: Update SC roster
            await send_status("Updating SC roster...")
            await send_log("")
            await send_log("=== Updating Strong Consistency Roster ===")
            
            container = detect_container()
            if container:
                # Stage observed nodes to pending roster
                await send_log("Staging observed nodes to roster...")
                result = subprocess.run(
                    ['docker', 'exec', container, 'asadm', '-e', 
                     'enable; manage roster stage observed ns test'],
                    capture_output=True, text=True, timeout=30
                )
                await send_log(result.stdout if result.stdout else "Roster staged")
                
                # Trigger recluster
                await send_log("")
                await send_log("Triggering recluster...")
                result = subprocess.run(
                    ['docker', 'exec', container, 'asadm', '-e', 
                     'enable; manage recluster'],
                    capture_output=True, text=True, timeout=30
                )
                await send_log(result.stdout if result.stdout else "Recluster triggered")
                
                # Show final roster
                await send_log("")
                await send_log("Verifying roster...")
                result = subprocess.run(
                    ['docker', 'exec', container, 'asadm', '-e', 'show roster'],
                    capture_output=True, text=True, timeout=30
                )
                await send_log(result.stdout if result.stdout else "Roster verified")
            
            await send_log("")
            await send_log(f"✓ Cluster successfully scaled to {target_count} nodes")
            await send_complete(True)
            
        else:
            # Scale down: Remove nodes with proper quiescing
            nodes_to_remove = current_count - target_count
            await send_log(f"Removing {nodes_to_remove} node(s) from cluster...")
            await send_log("")
            
            # Get list of containers for this cluster
            result = subprocess.run(
                ['docker', 'ps', '--filter', f'name=aerolab-{cluster_name}', '--format', '{{.Names}}'],
                capture_output=True, text=True
            )
            containers = [c.strip() for c in result.stdout.strip().split('\n') if c.strip()]
            containers.sort()  # Sort to get consistent ordering
            
            if len(containers) <= nodes_to_remove:
                await send_log("ERROR: Cannot remove that many nodes")
                await send_complete(False, "Not enough nodes to remove")
                return
            
            # Containers to remove (last ones in sorted order)
            containers_to_remove = containers[-nodes_to_remove:]
            container = containers[0]  # First container to run commands on
            
            for node_container in containers_to_remove:
                node_num = node_container.split('_')[-1]
                node_name = f"mydc-{node_num}"
                
                await send_log(f"=== Removing node: {node_container} ===")
                await send_log("")
                
                # Step 1: Quiesce the node
                await send_status(f"Quiescing node {node_num}...")
                await send_log("Step 1: Quiescing node for smooth master handoff...")
                result = subprocess.run(
                    ['docker', 'exec', container, 'asadm', '-e', 
                     f'enable; manage quiesce with {node_name}'],
                    capture_output=True, text=True, timeout=30
                )
                await send_log(result.stdout if result.stdout else "Quiesce command sent")
                
                # Step 2: Trigger recluster to perform master handoff
                await send_log("")
                await send_log("Step 2: Triggering recluster for master handoff...")
                result = subprocess.run(
                    ['docker', 'exec', container, 'asadm', '-e', 
                     'enable; manage recluster'],
                    capture_output=True, text=True, timeout=30
                )
                await send_log(result.stdout if result.stdout else "Recluster triggered")
                
                # Step 3: Wait for proxies to complete
                await send_status(f"Waiting for handoff...")
                await send_log("")
                await send_log("Step 3: Waiting for master handoff and proxy completion...")
                await asyncio.sleep(5)
                
                # Check quiesce status
                result = subprocess.run(
                    ['docker', 'exec', container, 'asadm', '-e', 
                     'show stat namespace like quiesce'],
                    capture_output=True, text=True, timeout=30
                )
                await send_log(result.stdout if result.stdout else "Quiesce status checked")
                
                # Step 4: Stop the node
                await send_status(f"Stopping node {node_num}...")
                await send_log("")
                await send_log(f"Step 4: Stopping node {node_container}...")
                subprocess.run(['docker', 'stop', node_container], capture_output=True, timeout=60)
                await send_log(f"Node {node_container} stopped")
                
                # Step 5: Remove the container
                await send_log(f"Removing container {node_container}...")
                subprocess.run(['docker', 'rm', node_container], capture_output=True, timeout=30)
                await send_log(f"Container {node_container} removed")
                await send_log("")
            
            # Step 6: Wait for cluster to stabilize
            await send_status("Stabilizing cluster...")
            await send_log("Waiting for cluster to stabilize...")
            await asyncio.sleep(3)
            
            # Step 7: Update roster
            await send_status("Updating roster...")
            await send_log("")
            await send_log("=== Updating Strong Consistency Roster ===")
            container = detect_container()
            if container:
                await send_log("Staging observed nodes to roster...")
                result = subprocess.run(
                    ['docker', 'exec', container, 'asadm', '-e', 
                     'enable; manage roster stage observed ns test'],
                    capture_output=True, text=True, timeout=30
                )
                await send_log(result.stdout if result.stdout else "Roster staged")
                
                await send_log("")
                await send_log("Triggering recluster...")
                result = subprocess.run(
                    ['docker', 'exec', container, 'asadm', '-e', 
                     'enable; manage recluster'],
                    capture_output=True, text=True, timeout=30
                )
                await send_log(result.stdout if result.stdout else "Recluster complete")
                
                # Wait for migrations
                await send_log("")
                await send_log("Waiting for migrations to complete...")
                await asyncio.sleep(3)
                
                # Check final status
                result = subprocess.run(
                    ['docker', 'exec', container, 'asadm', '-e', 
                     'show stat service like migrate_partitions_remaining'],
                    capture_output=True, text=True, timeout=30
                )
                await send_log(result.stdout if result.stdout else "Migrations checked")
            
            await send_log("")
            await send_log(f"✓ Cluster successfully scaled to {target_count} nodes")
            await send_complete(True)
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        import traceback
        await send_log(f"Error: {str(e)}")
        await send_complete(False, str(e))


@app.post("/api/setup/upload-feature-key")
async def upload_feature_key(request: Request):
    """Save uploaded feature key content."""
    try:
        from fastapi import Form, File, UploadFile
        
        body = await request.json()
        content = body.get("content", "")
        
        if not content:
            return {"success": False, "error": "No content provided"}
        
        # Save to aerolab-setup directory
        feature_key_path = os.path.join(BASE_DIR, '..', 'aerolab-setup', 'features.conf')
        os.makedirs(os.path.dirname(feature_key_path), exist_ok=True)
        
        with open(feature_key_path, 'w') as f:
            f.write(content)
        
        return {"success": True, "path": os.path.abspath(feature_key_path)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def detect_container():
    """Detect running AeroLab container."""
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


# =============================================================================
# WEBSOCKET TERMINAL WITH PTY SUPPORT
# =============================================================================

import pty
import select
import termios
import struct
import fcntl


class PtyProcess:
    """Wrapper for PTY-based process."""
    def __init__(self, fd, pid):
        self.fd = fd
        self.pid = pid
        self.returncode = None
    
    def write(self, data):
        os.write(self.fd, data)
    
    def read(self, size=1024):
        return os.read(self.fd, size)
    
    def terminate(self):
        try:
            os.kill(self.pid, 15)  # SIGTERM
        except ProcessLookupError:
            pass
    
    def poll(self):
        try:
            pid, status = os.waitpid(self.pid, os.WNOHANG)
            if pid != 0:
                self.returncode = os.WEXITSTATUS(status) if os.WIFEXITED(status) else -1
        except ChildProcessError:
            self.returncode = -1
        return self.returncode
    
    def fileno(self):
        return self.fd
    
    def close(self):
        try:
            os.close(self.fd)
        except OSError:
            pass


def create_pty_process(cmd):
    """Create a process with a pseudo-terminal."""
    pid, fd = pty.fork()
    
    if pid == 0:
        # Child process
        os.execvp(cmd[0], cmd)
    else:
        # Parent process
        # Set non-blocking
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        return PtyProcess(fd, pid)


class TerminalManager:
    """Manage terminal sessions."""
    
    def __init__(self):
        self.processes = {}
    
    def create_terminal_sync(self, terminal_type: str, container: str):
        """Create a new terminal session with PTY support."""
        if terminal_type == "aql":
            cmd = ['docker', 'exec', '-it', container, 'aql']
        elif terminal_type == "asadm":
            cmd = ['docker', 'exec', '-it', container, 'asadm']
        elif terminal_type == "python":
            # Python REPL with aerospike client pre-imported
            # Handle case where aerospike module may not be installed
            # AeroLab uses port 3100 by default
            python_init = """
try:
    import aerospike
    config = {"hosts": [("127.0.0.1", 3100)]}
    client = aerospike.client(config).connect()
    print("\\033[32m✓ Python client connected\\033[0m")
    print("  Client object: \\033[36mclient\\033[0m")
except ModuleNotFoundError:
    print("=" * 50)
    print("Aerospike Python client not installed!")
    print("=" * 50)
    print("")
    print("To install, run in Shell terminal:")
    print("  apt-get update && apt-get install -y python3-pip")
    print("  pip3 install aerospike --break-system-packages")
    print("")
    print("Then reconnect to this Python terminal.")
    print("=" * 50)
except Exception as e:
    print(f"Connection error: {e}")
    print("Make sure the cluster is running.")
"""
            cmd = ['docker', 'exec', '-it', container, 'python3', '-i', '-c', python_init]
        else:
            cmd = ['docker', 'exec', '-it', container, '/bin/bash']
        
        return create_pty_process(cmd)


terminal_manager = TerminalManager()


@app.websocket("/ws/terminal/{terminal_type}")
async def terminal_websocket(websocket: WebSocket, terminal_type: str):
    """WebSocket endpoint for terminal sessions with PTY support."""
    await websocket.accept()
    
    container = detect_container()
    if not container:
        await websocket.send_text(json.dumps({
            "type": "error",
            "data": "No AeroLab container detected. Please start your cluster first."
        }))
        await websocket.close()
        return
    
    # Create PTY process
    process = terminal_manager.create_terminal_sync(terminal_type, container)
    if not process:
        await websocket.send_text(json.dumps({
            "type": "error", 
            "data": "Failed to create terminal session."
        }))
        await websocket.close()
        return
    
    async def read_output():
        """Read output from PTY and send to websocket."""
        try:
            while True:
                # Check if there's data to read
                readable, _, _ = select.select([process.fd], [], [], 0.1)
                if readable:
                    try:
                        data = process.read(4096)
                        if data:
                            await websocket.send_text(json.dumps({
                                "type": "output",
                                "data": data.decode('utf-8', errors='replace')
                            }))
                    except OSError:
                        break
                else:
                    # Check if process is still running
                    if process.poll() is not None:
                        break
                    await asyncio.sleep(0.05)
        except Exception as e:
            pass
    
    # Start reading output
    output_task = asyncio.create_task(read_output())
    
    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            
            if data["type"] == "input":
                try:
                    process.write(data["data"].encode())
                except (BrokenPipeError, OSError):
                    break
            elif data["type"] == "resize":
                # Handle terminal resize
                try:
                    cols = data.get("cols", 80)
                    rows = data.get("rows", 24)
                    winsize = struct.pack('HHHH', rows, cols, 0, 0)
                    fcntl.ioctl(process.fd, termios.TIOCSWINSZ, winsize)
                except Exception:
                    pass
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        output_task.cancel()
        try:
            process.terminate()
            process.close()
        except Exception:
            pass


# =============================================================================
# AI CHAT (Gemini)
# =============================================================================

import pathlib
import httpx

GEMINI_API_KEY_FILE = os.path.join(os.path.dirname(BASE_DIR), ".gemini_api_key")

DOCS_CONTENT: str | None = None

def _load_docs() -> str:
    global DOCS_CONTENT
    if DOCS_CONTENT is not None:
        return DOCS_CONTENT

    project_root = os.path.dirname(BASE_DIR)
    parts = []
    for name in sorted(pathlib.Path(project_root).glob("strong-consistancydocs*.md")):
        parts.append(name.read_text(encoding="utf-8", errors="replace"))

    # Include cluster config files so the AI knows the current setup
    config_files = [
        os.path.join(project_root, "aerolab-setup", "aerospike.conf"),
        os.path.join(project_root, "features.conf"),
    ]
    for cfg_path in config_files:
        if os.path.isfile(cfg_path):
            try:
                content = open(cfg_path, encoding="utf-8", errors="replace").read().strip()
                if content:
                    label = os.path.basename(cfg_path)
                    parts.append(f"=== Current Cluster Config: {label} ===\n{content}")
            except Exception:
                pass

    DOCS_CONTENT = "\n\n---\n\n".join(parts) if parts else ""
    return DOCS_CONTENT


def _read_api_key() -> str | None:
    try:
        if os.path.exists(GEMINI_API_KEY_FILE):
            return open(GEMINI_API_KEY_FILE).read().strip() or None
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY")


def _save_api_key(key: str):
    with open(GEMINI_API_KEY_FILE, "w") as f:
        f.write(key.strip())


@app.get("/api/admin/apikey")
async def get_api_key_status():
    key = _read_api_key()
    return {"configured": bool(key), "masked": f"{key[:4]}...{key[-4:]}" if key and len(key) > 8 else None}


@app.post("/api/admin/apikey")
async def set_api_key(request: Request):
    body = await request.json()
    key = body.get("api_key", "").strip()
    if not key:
        return {"success": False, "error": "API key is required"}
    _save_api_key(key)
    return {"success": True}


@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message", "").strip()
    lesson_context = body.get("lesson_context", "")

    if not user_message:
        return {"error": "Message is required"}

    api_key = _read_api_key()
    if not api_key:
        return {"error": "Gemini API key not configured. Click the gear icon in the chat to set it up."}

    docs = _load_docs()

    system_prompt = (
        "You are an expert assistant for the Aerospike Strong Consistency (SC) tutorial. "
        "Answer questions about Aerospike Strong Consistency using the reference documentation provided below. "
        "The documentation also includes the current cluster configuration files (aerospike.conf and features.conf) "
        "so you know exactly how the user's cluster is set up. Use this config context when relevant. "
        "Be concise, accurate, and practical. Use code examples when helpful. "
        "If the user's question relates to the current lesson, tailor your answer to that context.\n\n"
    )

    if lesson_context:
        system_prompt += f"The user is currently viewing: {lesson_context}\n\n"

    system_prompt += f"=== Reference Documentation ===\n{docs}\n"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": system_prompt + "\n\nUser question: " + user_message}]}
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2048
        }
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()

        answer = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "Sorry, I could not generate a response.")
        )
        return {"answer": answer}
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            return {"error": "Invalid API key or request. Please check your Gemini API key."}
        return {"error": f"Gemini API error: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"Failed to reach Gemini: {str(e)}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

