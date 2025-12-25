/**
 * Aerospike SC Tutorial - Frontend JavaScript
 */

// =============================================================================
// STATE
// =============================================================================

let currentLesson = -1;
let terminal = null;
let terminalSocket = null;
let currentTerminalType = 'aql';
let fitAddon = null;

// =============================================================================
// INITIALIZATION
// =============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initTerminal();
    initTerminalTabs();
    checkClusterStatus();
    
    // Refresh cluster status every 30 seconds
    setInterval(checkClusterStatus, 30000);
});

// =============================================================================
// NAVIGATION
// =============================================================================

function initNavigation() {
    // Lesson navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const lessonId = parseInt(item.dataset.lesson);
            loadLesson(lessonId);
        });
    });
    
    // Previous/Next buttons
    document.getElementById('prev-btn').addEventListener('click', () => {
        if (currentLesson > 0) {
            loadLesson(currentLesson - 1);
        }
    });
    
    document.getElementById('next-btn').addEventListener('click', () => {
        if (currentLesson < LESSONS.length - 1) {
            loadLesson(currentLesson + 1);
        } else if (currentLesson === -1) {
            loadLesson(1);
        }
    });
}

function loadLesson(lessonId) {
    if (lessonId < 0 || lessonId >= LESSONS.length) return;
    
    currentLesson = lessonId;
    const lesson = LESSONS[lessonId];
    
    // Update content
    const contentEl = document.getElementById('lesson-content');
    contentEl.innerHTML = `
        <div class="lesson-header">
            <span class="lesson-number">Lesson ${lesson.id}</span>
        </div>
        <h1>${lesson.title}</h1>
        ${lesson.content}
    `;
    
    // Update navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (parseInt(item.dataset.lesson) === lessonId) {
            item.classList.add('active');
        }
    });
    
    // Update breadcrumb
    document.getElementById('current-lesson-title').textContent = lesson.title;
    
    // Update buttons
    document.getElementById('prev-btn').disabled = lessonId === 0;
    document.getElementById('next-btn').disabled = lessonId === LESSONS.length - 1;
    document.getElementById('next-btn').textContent = 
        lessonId === LESSONS.length - 1 ? 'Complete!' : 'Next →';
    
    // Scroll to top
    contentEl.scrollTop = 0;
}

// Make loadLesson available globally
window.loadLesson = loadLesson;

// =============================================================================
// TERMINAL
// =============================================================================

function initTerminal() {
    terminal = new Terminal({
        theme: {
            background: '#0d1117',
            foreground: '#e6edf3',
            cursor: '#58a6ff',
            cursorAccent: '#0d1117',
            selection: 'rgba(88, 166, 255, 0.3)',
            black: '#0d1117',
            red: '#f85149',
            green: '#3fb950',
            yellow: '#d29922',
            blue: '#58a6ff',
            magenta: '#a371f7',
            cyan: '#56d4dd',
            white: '#e6edf3',
            brightBlack: '#6e7681',
            brightRed: '#ff7b72',
            brightGreen: '#56d364',
            brightYellow: '#e3b341',
            brightBlue: '#79c0ff',
            brightMagenta: '#d2a8ff',
            brightCyan: '#76e3ea',
            brightWhite: '#ffffff'
        },
        fontFamily: '"JetBrains Mono", "Fira Code", Consolas, monospace',
        fontSize: 13,
        lineHeight: 1.3,
        letterSpacing: 0,
        cursorBlink: true,
        cursorStyle: 'bar',
        scrollback: 1000,
        tabStopWidth: 8,
        convertEol: true,
        cols: 120,
        rows: 20
    });
    
    fitAddon = new window.FitAddon.FitAddon();
    terminal.loadAddon(fitAddon);
    
    terminal.open(document.getElementById('terminal'));
    
    // Fit terminal after a short delay to ensure container is sized
    setTimeout(() => {
        fitAddon.fit();
    }, 100);
    
    // Handle window resize with debounce
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            fitAddon.fit();
        }, 100);
    });
    
    // Connect to terminal
    connectTerminal(currentTerminalType);
    
    // Terminal input
    terminal.onData(data => {
        if (terminalSocket && terminalSocket.readyState === WebSocket.OPEN) {
            terminalSocket.send(JSON.stringify({
                type: 'input',
                data: data
            }));
        }
    });
    
    // Clear terminal button
    document.getElementById('clear-terminal').addEventListener('click', () => {
        terminal.clear();
    });
    
    // Reconnect button
    document.getElementById('reconnect-terminal').addEventListener('click', () => {
        connectTerminal(currentTerminalType);
    });
}

function initTerminalTabs() {
    document.querySelectorAll('.terminal-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const terminalType = tab.dataset.terminal;
            
            // Update active tab
            document.querySelectorAll('.terminal-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Switch terminal
            currentTerminalType = terminalType;
            connectTerminal(terminalType);
            
            // Refit terminal after tab switch
            setTimeout(() => {
                if (fitAddon) fitAddon.fit();
            }, 50);
        });
    });
}

function connectTerminal(type) {
    // Close existing connection
    if (terminalSocket) {
        terminalSocket.close();
    }
    
    // Update status and clear terminal
    updateTerminalStatus('connecting');
    terminal.clear();
    terminal.write(`\x1b[36mConnecting to ${type.toUpperCase()}...\x1b[0m`);
    
    // Create new WebSocket connection
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/terminal/${type}`;
    
    terminalSocket = new WebSocket(wsUrl);
    
    terminalSocket.onopen = () => {
        updateTerminalStatus('connected');
        terminal.clear();  // Clear the "connecting" message
    };
    
    terminalSocket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.type === 'output') {
            terminal.write(message.data);
        } else if (message.type === 'error') {
            terminal.writeln(`\r\n\x1b[31m${message.data}\x1b[0m`);
        }
    };
    
    terminalSocket.onclose = () => {
        updateTerminalStatus('disconnected');
    };
    
    terminalSocket.onerror = (error) => {
        updateTerminalStatus('error');
        terminal.writeln(`\r\n\x1b[31mConnection error. Is the Aerospike container running?\x1b[0m`);
    };
}

function updateTerminalStatus(status) {
    const statusEl = document.getElementById('terminal-status');
    const dot = statusEl.querySelector('.status-dot');
    const text = statusEl.querySelector('.status-text');
    
    dot.className = 'status-dot';
    
    switch(status) {
        case 'connected':
            dot.classList.add('connected');
            text.textContent = `Connected to ${currentTerminalType.toUpperCase()}`;
            break;
        case 'disconnected':
            dot.classList.add('disconnected');
            text.textContent = 'Disconnected';
            break;
        case 'connecting':
            text.textContent = 'Connecting...';
            break;
        case 'error':
            dot.classList.add('disconnected');
            text.textContent = 'Connection error';
            break;
    }
}

// =============================================================================
// SETUP WIZARD
// =============================================================================

let setupState = {
    prerequisites: null,
    featureKeyPath: null
};

function openSetupWizard() {
    document.getElementById('setup-modal').style.display = 'flex';
    checkPrerequisites();
}

function closeSetupWizard() {
    document.getElementById('setup-modal').style.display = 'none';
}

// Close modal on overlay click
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        closeSetupWizard();
    }
});

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeSetupWizard();
    }
});

async function checkPrerequisites() {
    const content = document.getElementById('setup-wizard-content');
    content.innerHTML = `
        <div class="setup-step">
            <h3>Checking Prerequisites...</h3>
            <ul class="prereq-list">
                <li class="prereq-item">
                    <span class="prereq-icon status-loading"></span>
                    <div class="prereq-info">
                        <div class="prereq-name">Checking system...</div>
                    </div>
                </li>
            </ul>
        </div>
    `;
    
    try {
        const response = await fetch('/api/setup/check-prerequisites');
        const data = await response.json();
        
        // Validate response structure
        if (!data || !data.docker || !data.aerolab) {
            throw new Error('Invalid response from server');
        }
        
        setupState.prerequisites = data;
        renderPrerequisites(data);
    } catch (error) {
        content.innerHTML = `
            <div class="setup-step">
                <h3>Error</h3>
                <p>Failed to check prerequisites: ${error.message}</p>
                <div class="setup-actions">
                    <button class="btn btn-outline" onclick="closeSetupWizard()">Close</button>
                    <button class="btn btn-primary" onclick="checkPrerequisites()">Retry</button>
                </div>
            </div>
        `;
    }
}

function renderPrerequisites(data) {
    const content = document.getElementById('setup-wizard-content');
    
    // Safely access nested properties
    const docker = data.docker || {};
    const aerolab = data.aerolab || {};
    
    const dockerOk = docker.installed && docker.running;
    const aerolabOk = aerolab.installed;
    const hasCluster = data.existing_cluster;
    const hasFeatureKey = data.feature_key;
    
    let html = `
        <div class="setup-step">
            <h3>Prerequisites</h3>
            <ul class="prereq-list">
                <li class="prereq-item">
                    <span class="prereq-icon status-${dockerOk ? 'ok' : 'error'}"></span>
                    <div class="prereq-info">
                        <div class="prereq-name">Docker</div>
                        <div class="prereq-status ${dockerOk ? 'success' : 'error'}">
                            ${docker.installed 
                                ? (docker.running ? 'Running' : 'Installed but not running') 
                                : 'Not installed'}
                        </div>
                    </div>
                </li>
                <li class="prereq-item">
                    <span class="prereq-icon status-${aerolabOk ? 'ok' : 'error'}"></span>
                    <div class="prereq-info">
                        <div class="prereq-name">AeroLab</div>
                        <div class="prereq-status ${aerolabOk ? 'success' : 'error'}">
                            ${aerolabOk ? aerolab.version : 'Not installed'}
                        </div>
                    </div>
                </li>
                <li class="prereq-item">
                    <span class="prereq-icon status-${hasCluster ? 'ok' : 'info'}"></span>
                    <div class="prereq-info">
                        <div class="prereq-name">Existing Cluster</div>
                        <div class="prereq-status ${hasCluster ? 'success' : ''}">
                            ${hasCluster ? hasCluster : 'None found'}
                        </div>
                    </div>
                </li>
                <li class="prereq-item">
                    <span class="prereq-icon status-${hasFeatureKey ? 'ok' : 'warning'}"></span>
                    <div class="prereq-info">
                        <div class="prereq-name">Feature Key (Enterprise)</div>
                        <div class="prereq-status ${hasFeatureKey ? 'success' : 'warning'}">
                            ${hasFeatureKey ? 'Found' : 'Not found - required for SC'}
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    `;
    
    // Show errors if prerequisites not met
    if (!docker.running) {
        html += `
            <div class="warning-box">
                <strong>Docker Required</strong>
                <p>Please start Docker Desktop and try again.</p>
            </div>
        `;
    }
    
    if (!aerolabOk) {
        html += `
            <div class="warning-box">
                <strong>AeroLab Required</strong>
                <p>Install AeroLab:</p>
                <pre><code>brew install aerospike/tap/aerolab</code></pre>
                <p>Or download from: <a href="https://github.com/aerospike/aerolab/releases" target="_blank">GitHub Releases</a></p>
            </div>
        `;
    }
    
    // Feature key input if not found
    if (!hasFeatureKey) {
        setupState.featureKeyPath = null;
        html += `
            <div class="setup-step">
                <h3>Feature Key</h3>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 12px;">
                    Paste your Aerospike Enterprise feature key below:
                </p>
                <div class="feature-key-upload" id="feature-key-upload">
                    <textarea id="feature-key-input" placeholder="# Aerospike feature key file
# Paste your features.conf content here..."></textarea>
                    <div class="feature-key-hint">
                        Get an evaluation key at <a href="https://aerospike.com/download" target="_blank">aerospike.com/download</a>
                    </div>
                </div>
            </div>
        `;
    } else {
        setupState.featureKeyPath = hasFeatureKey;
    }
    
    // Cluster configuration
    if (dockerOk && aerolabOk) {
        html += `
            <div class="setup-step">
                <h3>Cluster Configuration</h3>
                <div class="setup-form">
                    <div class="form-group">
                        <label for="cluster-name">Cluster Name</label>
                        <input type="text" id="cluster-name" value="mydc" placeholder="mydc">
                    </div>
                    <div class="form-group">
                        <label for="node-count">Number of Nodes</label>
                        <select id="node-count">
                            <option value="1" selected>1 node (development)</option>
                            <option value="2">2 nodes</option>
                            <option value="3">3 nodes (recommended)</option>
                        </select>
                    </div>
                </div>
            </div>
        `;
        
        if (hasCluster) {
            html += `
                <div class="setup-actions">
                    <button class="btn btn-outline" onclick="destroyCluster('${hasCluster.replace('aerolab-', '').replace('_1', '')}')">
                        Destroy Existing
                    </button>
                    <button class="btn btn-primary" onclick="createCluster()">
                        Reconfigure SC
                    </button>
                </div>
            `;
        } else {
            html += `
                <div class="setup-actions">
                    <button class="btn btn-outline" onclick="closeSetupWizard()">Cancel</button>
                    <button class="btn btn-primary" onclick="createCluster()">
                        Create SC Cluster
                    </button>
                </div>
            `;
        }
    } else {
        html += `
            <div class="setup-actions">
                <button class="btn btn-outline" onclick="closeSetupWizard()">Close</button>
                <button class="btn btn-primary" onclick="checkPrerequisites()">Recheck</button>
            </div>
        `;
    }
    
    content.innerHTML = html;
}

async function createCluster() {
    const content = document.getElementById('setup-wizard-content');
    const clusterName = document.getElementById('cluster-name')?.value || 'mydc';
    const nodeCount = document.getElementById('node-count')?.value || '1';
    
    // Get feature key if provided
    let featureKeyPath = setupState.featureKeyPath;
    const featureKeyInput = document.getElementById('feature-key-input');
    
    if (featureKeyInput && featureKeyInput.value.trim()) {
        // Upload feature key first
        content.innerHTML = `
            <div class="setup-step">
                <h3>🔑 Saving Feature Key...</h3>
            </div>
        `;
        
        try {
            const uploadResponse = await fetch('/api/setup/upload-feature-key', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: featureKeyInput.value })
            });
            const uploadData = await uploadResponse.json();
            if (uploadData.success) {
                featureKeyPath = uploadData.path;
            } else {
                throw new Error(uploadData.error);
            }
        } catch (error) {
            content.innerHTML = `
                <div class="setup-step">
                    <h3>❌ Failed to save feature key</h3>
                    <p>${error.message}</p>
                    <div class="setup-actions">
                        <button class="btn btn-primary" onclick="checkPrerequisites()">Back</button>
                    </div>
                </div>
            `;
            return;
        }
    }
    
    // Show progress UI with live logs
    content.innerHTML = `
        <div class="setup-step">
            <h3>Creating SC Cluster</h3>
            <p style="color: var(--text-secondary); margin-bottom: 16px;">
                This may take a minute...
            </p>
            <ul class="progress-steps" id="progress-steps">
                <li class="progress-step" id="step-current">
                    <span class="step-icon running"></span>
                    <span class="step-text active">Starting setup...</span>
                </li>
            </ul>
            <div class="setup-logs-live">
                <div class="logs-header">Live Output</div>
                <pre id="live-logs"></pre>
            </div>
        </div>
    `;
    
    const stepsContainer = document.getElementById('progress-steps');
    const logsContainer = document.getElementById('live-logs');
    const steps = {};
    
    // Connect via WebSocket for streaming
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws/setup/create-cluster`);
    
    ws.onopen = () => {
        // Send configuration
        ws.send(JSON.stringify({
            cluster_name: clusterName,
            node_count: parseInt(nodeCount),
            feature_key_path: featureKeyPath
        }));
    };
    
    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        
        if (msg.type === 'log') {
            // Append log line
            logsContainer.textContent += msg.data + '\n';
            logsContainer.scrollTop = logsContainer.scrollHeight;
        } 
        else if (msg.type === 'step') {
            // Update or add step
            let stepEl = steps[msg.step];
            if (!stepEl) {
                stepEl = document.createElement('li');
                stepEl.className = 'progress-step';
                stepsContainer.appendChild(stepEl);
                steps[msg.step] = stepEl;
            }
            
            const statusIcon = msg.status === 'done' ? 'done' : 
                               msg.status === 'error' ? 'error' : 
                               msg.status === 'skip' ? 'skip' : 'running';
            
            stepEl.innerHTML = `
                <span class="step-icon ${statusIcon}"></span>
                <span class="step-text ${msg.status === 'running' ? 'active' : ''}">${msg.step}${msg.message ? ` - ${msg.message}` : ''}</span>
            `;
            
            // Remove the initial "Starting setup" placeholder
            const placeholder = document.getElementById('step-current');
            if (placeholder) placeholder.remove();
        }
        else if (msg.type === 'result') {
            ws.close();
            
            if (msg.success) {
                content.innerHTML = `
                    <div class="setup-step">
                        <h3>Success!</h3>
                        <p style="color: var(--accent-secondary); margin-bottom: 16px;">
                            ${msg.message}
                        </p>
                        <details class="setup-logs">
                            <summary>View command logs</summary>
                            <pre>${logsContainer.textContent}</pre>
                        </details>
                        <div class="setup-actions">
                            <button class="btn btn-primary" onclick="finishSetup()">
                                Start Tutorial
                            </button>
                        </div>
                    </div>
                `;
                
                checkClusterStatus();
                setTimeout(() => connectTerminal(currentTerminalType), 1000);
            } else {
                content.innerHTML = `
                    <div class="setup-step">
                        <h3>Setup Failed</h3>
                        <p style="color: var(--accent-error);">${msg.message}</p>
                        <details class="setup-logs" open>
                            <summary>Command logs</summary>
                            <pre>${logsContainer.textContent}</pre>
                        </details>
                        <div class="setup-actions">
                            <button class="btn btn-outline" onclick="checkPrerequisites()">Back</button>
                            <button class="btn btn-primary" onclick="createCluster()">Retry</button>
                        </div>
                    </div>
                `;
            }
        }
    };
    
    ws.onerror = (error) => {
        content.innerHTML = `
            <div class="setup-step">
                <h3>Connection Error</h3>
                <p style="color: var(--accent-error);">Failed to connect to setup service</p>
                <div class="setup-actions">
                    <button class="btn btn-outline" onclick="checkPrerequisites()">Back</button>
                    <button class="btn btn-primary" onclick="createCluster()">Retry</button>
                </div>
            </div>
        `;
    };
}

async function destroyCluster(clusterName) {
    if (!confirm(`Are you sure you want to destroy cluster "${clusterName}"? This will delete all data.`)) {
        return;
    }
    
    const content = document.getElementById('setup-wizard-content');
    content.innerHTML = `
        <div class="setup-step">
            <h3>Destroying Cluster...</h3>
        </div>
    `;
    
    try {
        const response = await fetch('/api/setup/destroy-cluster', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cluster_name: clusterName })
        });
        
        const data = await response.json();
        
        if (data.success) {
            checkClusterStatus();
            checkPrerequisites();
        } else {
            content.innerHTML = `
                <div class="setup-step">
                    <h3>Failed</h3>
                    <p>${data.error}</p>
                    <div class="setup-actions">
                        <button class="btn btn-primary" onclick="checkPrerequisites()">Back</button>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        content.innerHTML = `
            <div class="setup-step">
                <h3>Error</h3>
                <p>${error.message}</p>
            </div>
        `;
    }
}

function finishSetup() {
    closeSetupWizard();
    loadLesson(1);
}

// =============================================================================
// CLUSTER STATUS
// =============================================================================

async function checkClusterStatus() {
    const statusEl = document.getElementById('cluster-status');
    const setupBtn = document.getElementById('setup-cluster-btn');
    
    try {
        const response = await fetch('/api/cluster/status');
        const data = await response.json();
        
        if (data.status === 'ok') {
            statusEl.innerHTML = `
                <div class="status-indicator ok"></div>
                <span>
                    SC: ${data.strong_consistency ? '✓' : '✗'} | 
                    RF: ${data.replication_factor} | 
                    Nodes: ${data.ns_cluster_size}
                </span>
            `;
            statusEl.style.cursor = 'default';
            statusEl.onclick = null;
            if (setupBtn) setupBtn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg> Manage Cluster';
        } else {
            statusEl.innerHTML = `
                <div class="status-indicator error"></div>
                <span>No cluster running</span>
            `;
            statusEl.style.cursor = 'pointer';
            statusEl.onclick = openSetupWizard;
            if (setupBtn) setupBtn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg> Setup SC Cluster';
        }
    } catch (error) {
        statusEl.innerHTML = `
            <div class="status-indicator error"></div>
            <span>Cannot reach server</span>
        `;
    }
}

