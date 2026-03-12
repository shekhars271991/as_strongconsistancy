#!/bin/bash
set -e

CLUSTER_NAME="mydc"
NODE_COUNT=3
NAMESPACE="test"
FEATURE_KEY="features.conf"
CUSTOM_CONF="aerolab-setup/aerospike.conf"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$SCRIPT_DIR"

# ── Helpers ──────────────────────────────────────────────────────────────────

info()  { echo -e "\033[1;34m▸ $*\033[0m"; }
ok()    { echo -e "\033[1;32m✓ $*\033[0m"; }
fail()  { echo -e "\033[1;31m✗ $*\033[0m"; exit 1; }
warn()  { echo -e "\033[1;33m! $*\033[0m"; }

wait_for_port() {
    local host=$1 port=$2 retries=${3:-30}
    for i in $(seq 1 "$retries"); do
        if docker exec "aerolab-${CLUSTER_NAME}_1" asinfo -v status -p "$port" >/dev/null 2>&1; then
            return 0
        fi
        sleep 2
    done
    return 1
}

# ── Pre-flight checks ───────────────────────────────────────────────────────

info "Checking prerequisites..."

command -v aerolab >/dev/null 2>&1 || fail "aerolab not found. Install from https://github.com/aerospike/aerolab"
command -v docker  >/dev/null 2>&1 || fail "docker not found. Install Docker Desktop first."
docker info >/dev/null 2>&1        || fail "Docker daemon is not running."

[ -f "$FEATURE_KEY" ]  || fail "Feature key not found at $FEATURE_KEY"
[ -f "$CUSTOM_CONF" ]  || fail "Aerospike config not found at $CUSTOM_CONF"

ok "Prerequisites OK"

# ── Tear down existing cluster (if any) ─────────────────────────────────────

if aerolab cluster list 2>/dev/null | grep -q "$CLUSTER_NAME"; then
    warn "Cluster '$CLUSTER_NAME' already exists — destroying it first"
    aerolab cluster destroy -n "$CLUSTER_NAME" -f || true
    sleep 3
fi

# ── Configure AeroLab backend ───────────────────────────────────────────────

info "Setting AeroLab backend to Docker..."
aerolab config backend -t docker
ok "Backend set"

# ── Create the Enterprise SC cluster ────────────────────────────────────────

info "Creating ${NODE_COUNT}-node Enterprise cluster '$CLUSTER_NAME'..."
aerolab cluster create \
    -n "$CLUSTER_NAME" \
    -c "$NODE_COUNT" \
    -f "$FEATURE_KEY" \
    --customconf "$CUSTOM_CONF"

ok "Cluster created"

# ── Wait for Aerospike to be ready ──────────────────────────────────────────

info "Waiting for Aerospike nodes to come up..."
if ! wait_for_port localhost 3000; then
    fail "Aerospike did not start within 60 seconds"
fi
sleep 5
ok "Aerospike is running"

# ── Set the roster (required for SC) ────────────────────────────────────────

info "Collecting node IDs for roster..."

NODE_IDS=""
for i in $(seq 1 "$NODE_COUNT"); do
    CONTAINER="aerolab-${CLUSTER_NAME}_${i}"
    NID=$(docker exec "$CONTAINER" asinfo -v "node" 2>/dev/null) || fail "Cannot get node ID from $CONTAINER"
    if [ -z "$NODE_IDS" ]; then
        NODE_IDS="$NID"
    else
        NODE_IDS="${NODE_IDS},${NID}"
    fi
    echo "  Node $i ($CONTAINER): $NID"
done

ok "Found nodes: $NODE_IDS"

info "Setting roster on all nodes for namespace '$NAMESPACE'..."
for i in $(seq 1 "$NODE_COUNT"); do
    CONTAINER="aerolab-${CLUSTER_NAME}_${i}"
    docker exec "$CONTAINER" \
        asinfo -v "roster-set:namespace=${NAMESPACE};nodes=${NODE_IDS}" 2>/dev/null || true
done

info "Triggering recluster on all nodes..."
for i in $(seq 1 "$NODE_COUNT"); do
    CONTAINER="aerolab-${CLUSTER_NAME}_${i}"
    RESULT=$(docker exec "$CONTAINER" asinfo -v "recluster:" 2>/dev/null || true)
    if [ "$RESULT" = "ok" ]; then
        echo "  Recluster accepted by $CONTAINER (principal)"
    fi
done

sleep 5

# ── Verify SC is active ─────────────────────────────────────────────────────

info "Verifying Strong Consistency..."
SC_STATUS=$(docker exec "aerolab-${CLUSTER_NAME}_1" \
    asinfo -v "namespace/${NAMESPACE}" 2>/dev/null | tr ';' '\n' | grep "strong-consistency=" || true)

if echo "$SC_STATUS" | grep -q "true"; then
    ok "Strong Consistency is ENABLED"
else
    warn "Could not confirm SC status: $SC_STATUS"
fi

ROSTER_STATUS=$(docker exec "aerolab-${CLUSTER_NAME}_1" \
    asinfo -v "roster:namespace=${NAMESPACE}" 2>/dev/null || true)
echo "  Roster: $ROSTER_STATUS"

# ── Install Python dependencies ─────────────────────────────────────────────

info "Installing Python dependencies..."
pip install -q -r requirements.txt
ok "Dependencies installed"

# ── Launch the web tutorial ─────────────────────────────────────────────────

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   Aerospike SC Tutorial — Ready!                           ║"
echo "║                                                            ║"
echo "║   Cluster : $CLUSTER_NAME ($NODE_COUNT nodes, SC enabled)              ║"
echo "║   Web UI  : http://localhost:8000                          ║"
echo "║                                                            ║"
echo "║   Press Ctrl+C to stop the server.                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Free port 8000 if something is still using it
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
sleep 1

python run_web.py
