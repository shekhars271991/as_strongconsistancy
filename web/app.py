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
from sc_tutorial.commands.suggested import LESSON_COMMANDS

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

# 2. Create cluster with your feature key
aerolab cluster create -n mydc -c 1 -f features.conf

# 3. Enable Strong Consistency
aerolab conf sc -n mydc</code></pre>

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
        <h3>Step 1: Enable SC in Namespace Configuration</h3>
        <pre><code># In aerospike.conf:

namespace sc_namespace {{
    strong-consistency true     # Enable SC mode
    replication-factor 2        # RF must match cluster size
    default-ttl 0               # Recommended: disable expiration
    nsup-period 0               # Disable supervisor
    
    storage-engine memory {{
        file /opt/aerospike/data/sc.dat
        filesize 2G
    }}
}}</code></pre>

        <h3>Key Configuration Parameters</h3>
        <ul>
            <li><code>strong-consistency true</code> - Enables SC mode</li>
            <li><code>replication-factor N</code> - SC requires nodes ≥ RF (RF=1 for single-node)</li>
            <li><code>default-ttl 0</code> - Disable expiration (recommended)</li>
            <li><code>commit-to-device true</code> - Optional: ensures durability</li>
        </ul>

        <h3>Step 2: Configure the Roster</h3>
        <p>The <strong>ROSTER</strong> is a list of nodes expected in the cluster for an SC namespace.</p>
        
        <pre><code># View roster status
asinfo -v "roster:namespace=test"

# Using asadm (easier)
asadm> manage roster stage observed ns test
asadm> manage recluster</code></pre>

        <div class="info-box">
            <strong>Key Points:</strong>
            <ul>
                <li>Roster is stored persistently in a distributed table</li>
                <li>Nodes not on the roster cannot participate in SC operations</li>
                <li>Changes require a 'recluster' command</li>
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

        <h3>Try These Commands in AQL</h3>
        
        <h4>INSERT Records</h4>
        <pre><code>INSERT INTO test (PK, name, age) VALUES ('user1', 'Alice', 30)
INSERT INTO test (PK, city, score) VALUES ('user2', 'NYC', 95.5)
INSERT INTO test (PK, tags) VALUES ('user3', JSON('["a","b","c"]'))</code></pre>

        <h4>READ Records</h4>
        <pre><code>SELECT * FROM test WHERE PK='user1'
SELECT name, age FROM test WHERE PK='user1'
SELECT *, generation, ttl FROM test WHERE PK='user1'
SELECT count(*) FROM test</code></pre>

        <h4>UPDATE Records</h4>
        <pre><code>UPDATE test SET age=31 WHERE PK='user1'
UPDATE test SET status='active' WHERE PK='user1'</code></pre>

        <h4>DELETE Records</h4>
        <pre><code>DELETE FROM test WHERE PK='user1'</code></pre>
        
        <div class="warning-box">
            Note: In SC mode, deletes create <strong>tombstones</strong>!
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

        <h3>Demo: Session Consistency</h3>
        <pre><code># Write and immediately read
INSERT INTO test (PK, counter) VALUES ('session_test', 0)
SELECT * FROM test WHERE PK='session_test'

# Update and verify
UPDATE test SET counter=1 WHERE PK='session_test'
SELECT *, generation FROM test WHERE PK='session_test'</code></pre>

        <div class="info-box">
            Linearizable reads are ~20-50% slower due to replica verification.
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
        <p>Multiple clients incrementing a counter will never lose updates:</p>
        <pre><code># Initialize counter
INSERT INTO test (PK, counter) VALUES ('counter', 0)

# Increment (do this from multiple terminals!)
UPDATE test SET counter = counter + 1 WHERE PK='counter'

# Check final value
SELECT counter, generation FROM test WHERE PK='counter'</code></pre>

        <div class="success-box">
            SC guarantees: Final counter = number of successful increments
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

        <h3>Demo: Watch Generation Increment</h3>
        <pre><code># Create record
INSERT INTO test (PK, balance) VALUES ('account1', 1000)
SELECT *, generation FROM test WHERE PK='account1'

# Update multiple times
UPDATE test SET balance=1100 WHERE PK='account1'
SELECT balance, generation FROM test WHERE PK='account1'

UPDATE test SET balance=1200 WHERE PK='account1'
SELECT balance, generation FROM test WHERE PK='account1'</code></pre>

        <h3>Conflict Detection</h3>
        <p>Open <strong>two terminals</strong> to simulate concurrent clients:</p>
        <pre><code># Terminal 1: Read record
SELECT *, generation FROM test WHERE PK='account1'

# Terminal 2: Update record
UPDATE test SET balance=999 WHERE PK='account1'

# Terminal 1: Check - generation changed!
SELECT *, generation FROM test WHERE PK='account1'</code></pre>
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

        <h3>Check Error Stats in ASADM</h3>
        <pre><code>show stat namespace like fail_
show stat namespace like fail_generation
show stat namespace like timeout</code></pre>
        """
    },
    {
        "id": 8,
        "title": "Cluster Behavior Under Failure",
        "short": "Cluster",
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

        <h3>Recovery Commands (ASADM)</h3>
        <pre><code># Check partition status
show pmap
show stat namespace like dead_partitions
show stat namespace like unavailable

# View roster
show roster

# Recovery (USE WITH CAUTION!)
asinfo -v 'revive:namespace=test'
manage recluster</code></pre>
        """
    },
    {
        "id": 9,
        "title": "Best Practices",
        "short": "Best Practices",
        "icon": "",
        "category": "reference",
        "content": f"""
        <h3>Configuration</h3>
        <ul>
            <li>Set <code>replication-factor >= cluster size</code> (RF=3 for production)</li>
            <li>Disable expiration (<code>default-ttl 0</code>) for critical data</li>
            <li>Consider <code>commit-to-device</code> for maximum durability</li>
            <li>Use rack-awareness for multi-AZ deployments</li>
        </ul>

        <h3>Operations</h3>
        <ul>
            <li>Use generation checks for concurrent updates</li>
            <li>Handle InDoubt errors properly - read to verify</li>
            <li>Use durable deletes (creates tombstones)</li>
            <li>Prefer Session Consistency unless you need Linearizable</li>
        </ul>

        <h3>Monitoring</h3>
        <ul>
            <li>Watch <code>dead_partitions</code> and <code>unavailable_partitions</code></li>
            <li>Monitor <code>client_write_error</code> and <code>client_read_error</code></li>
            <li>Track <code>fail_generation</code> for conflict rates</li>
            <li>Alert on <code>clock_skew_stop_writes</code></li>
        </ul>

        <h3>Avoid</h3>
        <div class="warning-box">
            <ul>
                <li>Don't use non-durable deletes in production</li>
                <li>Don't enable client retransmit (can cause duplicates)</li>
                <li>Don't ignore InDoubt errors</li>
                <li>Don't switch from AP to SC on existing namespace</li>
            </ul>
        </div>
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


@app.get("/api/commands/{lesson_name}")
async def get_commands(lesson_name: str):
    """Get suggested commands for a lesson."""
    commands = LESSON_COMMANDS.get(lesson_name, LESSON_COMMANDS.get('basic_ops'))
    return {"commands": commands}


@app.get("/api/cluster/status")
async def get_cluster_status():
    """Get cluster status."""
    try:
        container = detect_container()
        if not container:
            return {"status": "error", "message": "No AeroLab container detected"}
        
        # Get namespace info
        result = subprocess.run(
            ['docker', 'exec', container, 'asinfo', '-v', 'namespace/test'],
            capture_output=True, text=True, timeout=5
        )
        
        if result.returncode == 0:
            info = result.stdout.strip()
            params = dict(item.split('=') for item in info.split(';') if '=' in item)
            
            return {
                "status": "ok",
                "container": container,
                "strong_consistency": params.get('strong-consistency', 'false') == 'true',
                "replication_factor": params.get('replication-factor', 'N/A'),
                "ns_cluster_size": params.get('ns_cluster_size', 'N/A'),
                "dead_partitions": int(params.get('dead_partitions', 0)),
                "unavailable_partitions": int(params.get('unavailable_partitions', 0)),
                "objects": int(params.get('objects', 0)),
                "tombstones": int(params.get('tombstones', 0))
            }
        else:
            return {"status": "error", "message": result.stderr}
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

