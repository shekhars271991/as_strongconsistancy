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
    // Restore sidebar collapse state
    if (localStorage.getItem('sc-sidebar') === 'collapsed') {
        const sb = document.getElementById('sidebar');
        if (sb) sb.classList.add('collapsed');
    }

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
    
    // Initialize code tabs (AQL vs Python)
    initCodeTabs();
    
    // Apply syntax highlighting
    applySyntaxHighlighting();
    
    // Add copy buttons to all code blocks
    addCopyButtons();
}

// =============================================================================
// COPY BUTTONS FOR CODE BLOCKS
// =============================================================================

// =============================================================================
// CODE TABS (AQL vs Python)
// =============================================================================

function initCodeTabs() {
    // Find all code tab containers
    document.querySelectorAll('.code-tabs').forEach(container => {
        const buttons = container.querySelectorAll('.code-tab-btn');
        const contents = container.querySelectorAll('.code-tab-content');
        
        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                const lang = btn.dataset.lang;
                
                // Update button states
                buttons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Update content visibility
                contents.forEach(c => {
                    c.classList.remove('active');
                    if (c.dataset.lang === lang) {
                        c.classList.add('active');
                    }
                });
                
                // Re-add buttons after tab switch
                setTimeout(() => addCopyButtons(), 50);
            });
        });
    });
}

// Apply syntax highlighting with highlight.js
function applySyntaxHighlighting() {
    if (typeof hljs === 'undefined') {
        console.warn('highlight.js not loaded');
        return;
    }
    
    // Highlight Python code blocks
    document.querySelectorAll('.code-tab-content[data-lang="python"] pre code').forEach(block => {
        // Add language class if not present
        if (!block.classList.contains('language-python')) {
            block.classList.add('language-python');
        }
        hljs.highlightElement(block);
    });
    
    // Highlight AQL as SQL (closest match)
    document.querySelectorAll('.code-tab-content[data-lang="aql"] pre code').forEach(block => {
        if (!block.classList.contains('language-sql')) {
            block.classList.add('language-sql');
        }
        hljs.highlightElement(block);
    });
    
    // Highlight standalone code blocks
    document.querySelectorAll('.lesson-content pre code:not(.hljs)').forEach(block => {
        // Detect language from content
        const content = block.textContent;
        if (content.includes('import ') || content.includes('def ') || content.includes('client.')) {
            block.classList.add('language-python');
        } else if (content.includes('SELECT') || content.includes('INSERT') || content.includes('DELETE')) {
            block.classList.add('language-sql');
        } else if (content.includes('asadm') || content.includes('aerolab') || content.includes('docker')) {
            block.classList.add('language-bash');
        }
        hljs.highlightElement(block);
    });
}

function addCopyButtons() {
    // Find all pre elements in lesson content
    const codeBlocks = document.querySelectorAll('.lesson-content pre');
    
    codeBlocks.forEach(pre => {
        // Skip if already has a copy button
        if (pre.querySelector('.copy-btn')) return;
        
        // Create button container
        const btnContainer = document.createElement('div');
        btnContainer.className = 'code-btn-container';
        
        // Create copy button
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <span>Copy</span>
        `;
        
        copyBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            const code = pre.querySelector('code');
            const text = code ? code.textContent : pre.textContent;
            
            try {
                await navigator.clipboard.writeText(text.trim());
                copyBtn.classList.add('copied');
                copyBtn.querySelector('span').textContent = 'Copied!';
                copyBtn.querySelector('svg').innerHTML = `<polyline points="20 6 9 17 4 12"></polyline>`;
                
                setTimeout(() => {
                    copyBtn.classList.remove('copied');
                    copyBtn.querySelector('span').textContent = 'Copy';
                    copyBtn.querySelector('svg').innerHTML = `
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    `;
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        });
        
        btnContainer.appendChild(copyBtn);
        
        // Check if this is a Python code block (inside python tab or has python class)
        const codeEl = pre.querySelector('code');
        const isPython = pre.closest('.code-tab-content[data-lang="python"]') ||
                        (codeEl && codeEl.className && codeEl.className.includes('python')) ||
                        pre.classList.contains('python-code');
        
        if (isPython) {
            // Add execute button for Python code
            const execBtn = document.createElement('button');
            execBtn.className = 'exec-btn';
            execBtn.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
                <span>Run</span>
            `;
            
            execBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                const code = pre.querySelector('code');
                const text = code ? code.textContent : pre.textContent;
                
                executeInPythonTerminal(text.trim(), execBtn);
            });
            
            btnContainer.appendChild(execBtn);
        }
        
        pre.appendChild(btnContainer);
    });
}

// Execute code in Python terminal
function executeInPythonTerminal(code, btn) {
    // Switch to Python terminal if not already there
    if (currentTerminalType !== 'python') {
        // Click the Python tab
        const pythonTab = document.querySelector('.terminal-tab[data-terminal="python"]');
        if (pythonTab) {
            pythonTab.click();
            // Wait for connection then send code
            setTimeout(() => sendCodeToTerminal(code, btn), 1500);
        }
    } else {
        sendCodeToTerminal(code, btn);
    }
}

function sendCodeToTerminal(code, btn) {
    if (!terminalSocket || terminalSocket.readyState !== WebSocket.OPEN) {
        alert('Python terminal not connected. Please wait and try again.');
        return;
    }
    
    // Show running state
    btn.classList.add('running');
    btn.querySelector('span').textContent = 'Running...';
    
    // Split code into lines and send each line with Enter
    const lines = code.split('\n');
    let delay = 0;
    
    lines.forEach((line, index) => {
        setTimeout(() => {
            // Send line + Enter
            terminalSocket.send(JSON.stringify({
                type: 'input',
                data: line + '\r'
            }));
            
            // Reset button after last line
            if (index === lines.length - 1) {
                setTimeout(() => {
                    btn.classList.remove('running');
                    btn.classList.add('executed');
                    btn.querySelector('span').textContent = 'Done!';
                    btn.querySelector('svg').innerHTML = `<polyline points="20 6 9 17 4 12"></polyline>`;
                    
                    setTimeout(() => {
                        btn.classList.remove('executed');
                        btn.querySelector('span').textContent = 'Run';
                        btn.querySelector('svg').innerHTML = `<polygon points="5 3 19 12 5 21 5 3"></polygon>`;
                    }, 2000);
                }, 500);
            }
        }, delay);
        delay += 100; // Small delay between lines
    });
}

// Make loadLesson available globally
window.loadLesson = loadLesson;

// =============================================================================
// TERMINAL
// =============================================================================

const TERM_THEMES = {
    dark: {
        background: '#0d1117',
        foreground: '#e6edf3',
        cursor: '#58a6ff',
        cursorAccent: '#0d1117',
        selectionBackground: 'rgba(88, 166, 255, 0.3)',
        selectionInactiveBackground: 'rgba(88, 166, 255, 0.15)',
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
    light: {
        background: '#ffffff',
        foreground: '#1f2328',
        cursor: '#0969da',
        cursorAccent: '#ffffff',
        selectionBackground: 'rgba(9, 105, 218, 0.2)',
        selectionInactiveBackground: 'rgba(9, 105, 218, 0.1)',
        black: '#1f2328',
        red: '#cf222e',
        green: '#1a7f37',
        yellow: '#9a6700',
        blue: '#0969da',
        magenta: '#8250df',
        cyan: '#1b7c83',
        white: '#f6f8fa',
        brightBlack: '#6e7781',
        brightRed: '#a40e26',
        brightGreen: '#2da44e',
        brightYellow: '#bf8700',
        brightBlue: '#218bff',
        brightMagenta: '#a475f9',
        brightCyan: '#3192aa',
        brightWhite: '#ffffff'
    }
};

function getActiveTermTheme() {
    return document.documentElement.classList.contains('light') ? TERM_THEMES.light : TERM_THEMES.dark;
}

function sendTermResize(term, socket) {
    if (socket && socket.readyState === WebSocket.OPEN && term) {
        socket.send(JSON.stringify({ type: 'resize', cols: term.cols, rows: term.rows }));
    }
}

function fitAndResize() {
    if (fitAddon) { fitAddon.fit(); sendTermResize(terminal, terminalSocket); }
}

function cmFitAndResize() {
    if (cmFitAddon) { cmFitAddon.fit(); sendTermResize(cmTerminal, cmTerminalSocket); }
}

function enableTermCopyPaste(term, getSocket) {
    // Auto-copy on selection (like iTerm / gnome-terminal)
    term.onSelectionChange(() => {
        const sel = term.getSelection();
        if (sel) {
            navigator.clipboard.writeText(sel).catch(() => {});
        }
    });

    // Cmd/Ctrl+C: copy if selection exists, otherwise send SIGINT
    // Cmd/Ctrl+V: paste from clipboard
    term.attachCustomKeyEventHandler(ev => {
        if (ev.type !== 'keydown') return true;
        const isMac = navigator.platform.toUpperCase().includes('MAC');
        const mod = isMac ? ev.metaKey : ev.ctrlKey;

        if (mod && ev.key === 'c' && term.hasSelection()) {
            navigator.clipboard.writeText(term.getSelection()).catch(() => {});
            term.clearSelection();
            return false;
        }
        if (mod && ev.key === 'v') {
            navigator.clipboard.readText().then(text => {
                if (text) {
                    const ws = getSocket();
                    if (ws && ws.readyState === WebSocket.OPEN) {
                        ws.send(JSON.stringify({ type: 'input', data: text }));
                    }
                }
            }).catch(() => {});
            return false;
        }
        return true;
    });
}

function initTerminal() {
    terminal = new Terminal({
        theme: getActiveTermTheme(),
        fontFamily: '"IBM Plex Mono", Consolas, monospace',
        fontSize: 13,
        lineHeight: 1.35,
        letterSpacing: 0,
        cursorBlink: true,
        cursorStyle: 'bar',
        scrollback: 1000,
        tabStopWidth: 8,
        convertEol: true,
        allowProposedApi: true
    });
    
    fitAddon = new window.FitAddon.FitAddon();
    terminal.loadAddon(fitAddon);
    
    terminal.open(document.getElementById('terminal'));
    try { terminal.loadAddon(new window.WebglAddon.WebglAddon()); } catch(e) { console.warn('WebGL addon failed, using DOM renderer:', e); }
    enableTermCopyPaste(terminal, () => terminalSocket);
    
    // Fit terminal after a short delay to ensure container is sized
    setTimeout(fitAndResize, 100);
    
    // Handle window resize with debounce
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(fitAndResize, 100);
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
    
    // Copy terminal button
    document.getElementById('copy-terminal').addEventListener('click', function() {
        copyTerminalContent(terminal, this);
    });

    // Clear terminal button
    document.getElementById('clear-terminal').addEventListener('click', () => {
        terminal.clear();
    });
    
    // Reconnect button
    document.getElementById('reconnect-terminal').addEventListener('click', () => {
        connectTerminal(currentTerminalType);
    });
    
    // Toggle minimize/maximize terminal
    const toggleBtn = document.getElementById('toggle-terminal');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            const panel = document.querySelector('.terminal-panel');
            if (!panel) return;
            
            const isMinimized = panel.classList.toggle('minimized');
            toggleBtn.title = isMinimized ? 'Maximize' : 'Minimize';
            
            // Toggle icon visibility
            const iconMin = toggleBtn.querySelector('.icon-minimize');
            const iconMax = toggleBtn.querySelector('.icon-maximize');
            if (iconMin && iconMax) {
                iconMin.style.display = isMinimized ? 'none' : 'block';
                iconMax.style.display = isMinimized ? 'block' : 'none';
            }
            
            // Refit and focus terminal when maximized
            if (!isMinimized) {
                setTimeout(() => {
                    fitAndResize();
                    if (terminal) terminal.focus();
                }, 100);
            }
        });
    }
}

// Global function to toggle terminal (can be called from anywhere)
window.toggleTerminal = function() {
    const toggleBtn = document.getElementById('toggle-terminal');
    if (toggleBtn) toggleBtn.click();
};

function initTerminalTabs() {
    document.querySelectorAll('.terminal-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const terminalType = tab.dataset.terminal;
            
            // Auto-maximize if minimized
            const panel = document.querySelector('.terminal-panel');
            if (panel && panel.classList.contains('minimized')) {
                panel.classList.remove('minimized');
                const toggleBtn = document.getElementById('toggle-terminal');
                if (toggleBtn) {
                    toggleBtn.title = 'Minimize';
                    const iconMin = toggleBtn.querySelector('.icon-minimize');
                    const iconMax = toggleBtn.querySelector('.icon-maximize');
                    if (iconMin) iconMin.style.display = 'block';
                    if (iconMax) iconMax.style.display = 'none';
                }
            }

            // Update active tab
            document.querySelectorAll('.terminal-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Switch terminal
            currentTerminalType = terminalType;
            connectTerminal(terminalType);
            
            // Refit and focus terminal after tab switch
            setTimeout(() => {
                fitAndResize();
                if (terminal) terminal.focus();
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
        terminal.clear();
        terminal.focus();
        fitAndResize();
    };
    
    terminalSocket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.type === 'output') {
            terminal.write(message.data);
            // Feed output to the AI monitoring buffer
            if (typeof captureTerminalLine === 'function') {
                const lines = message.data.split(/[\r\n]+/);
                for (const line of lines) captureTerminalLine(line);
            }
        } else if (message.type === 'error') {
            terminal.writeln(`\r\n\x1b[31m${message.data}\x1b[0m`);
            if (typeof captureTerminalLine === 'function') {
                captureTerminalLine(message.data);
            }
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
            text.textContent = currentTerminalType === 'bash'
                ? 'Local Terminal'
                : `Connected to ${currentTerminalType.toUpperCase()}`;
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
        // Determine current node count from cluster status
        const currentNodes = currentNodeCount || 1;
        
        html += `
            <div class="setup-step">
                <h3>Cluster Configuration</h3>
                <div class="setup-form">
                    <div class="form-group">
                        <label for="cluster-name">Cluster Name</label>
                        <input type="text" id="cluster-name" value="mydc" placeholder="mydc" ${hasCluster ? 'disabled' : ''}>
                    </div>
                    <div class="form-group">
                        <label for="node-count">Number of Nodes ${hasCluster ? `<span style="color: var(--text-muted);">(current: ${currentNodes})</span>` : ''}</label>
                        <select id="node-count" onchange="onNodeCountChange(${currentNodes}, ${hasCluster ? 'true' : 'false'})">
                            <option value="1" ${currentNodes === 1 ? 'selected' : ''}>1 node (development)</option>
                            <option value="2" ${currentNodes === 2 ? 'selected' : ''}>2 nodes</option>
                            <option value="3" ${currentNodes === 3 ? 'selected' : ''}>3 nodes (recommended)</option>
                            <option value="4" ${currentNodes === 4 ? 'selected' : ''}>4 nodes</option>
                            <option value="5" ${currentNodes === 5 ? 'selected' : ''}>5 nodes (max)</option>
                        </select>
                    </div>
                </div>
            </div>
        `;
        
        if (hasCluster) {
            html += `
                <div class="setup-actions" id="setup-actions">
                    <button class="btn btn-outline" onclick="destroyCluster('${hasCluster.replace('aerolab-', '').replace('_1', '')}')">
                        Destroy Cluster
                    </button>
                    <button class="btn btn-primary" id="scale-btn" onclick="scaleFromDropdown(${currentNodes})" style="display: none;">
                        Scale Cluster
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

let currentNodeCount = 0;
let isScaling = false;

async function checkClusterStatus() {
    const statusEl = document.getElementById('cluster-status');
    const setupBtn = document.getElementById('setup-cluster-btn');
    
    try {
        const response = await fetch('/api/cluster/status');
        const data = await response.json();
        
        if (data.status === 'ok') {
            const nodes = parseInt(data.cluster_size) || parseInt(data.ns_cluster_size) || 0;
            const roster = parseInt(data.ns_cluster_size) || 0;
            currentNodeCount = nodes || 1;
            const hasIssues = (data.diagnostics && data.diagnostics.length > 0) ||
                              data.dead_partitions > 0 || data.unavailable_partitions > 0;
            const indicatorClass = hasIssues ? 'warning' : 'ok';
            
            let statusText = `SC: ${data.strong_consistency ? '✓' : '✗'} | RF: ${data.replication_factor} | Nodes: ${nodes}`;
            if (roster !== nodes && roster > 0) {
                statusText += ` (Roster: ${roster})`;
            }
            
            statusEl.innerHTML = `
                <div class="status-indicator ${indicatorClass}"></div>
                <span>${statusText}</span>
            `;
            statusEl.style.cursor = 'pointer';
            statusEl.onclick = () => openClusterManagement();
            
            if (setupBtn) {
                setupBtn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg> Manage Cluster';
                setupBtn.onclick = () => openClusterManagement();
            }
        } else {
            currentNodeCount = 0;
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

// Handle node count dropdown change
function onNodeCountChange(currentNodes, hasCluster) {
    const select = document.getElementById('node-count');
    const scaleBtn = document.getElementById('scale-btn');
    const newCount = parseInt(select.value);
    
    if (hasCluster && scaleBtn) {
        if (newCount !== currentNodes) {
            scaleBtn.style.display = 'inline-flex';
            scaleBtn.textContent = newCount > currentNodes 
                ? `Scale Up to ${newCount} nodes` 
                : `Scale Down to ${newCount} nodes`;
        } else {
            scaleBtn.style.display = 'none';
        }
    }
}

// Scale cluster from dropdown selection
function scaleFromDropdown(currentNodes) {
    const select = document.getElementById('node-count');
    const targetCount = parseInt(select.value);
    
    if (targetCount === currentNodes) return;
    
    // Close setup wizard and open cluster management view
    closeSetupWizard();
    openClusterManagement(currentNodes, targetCount);
}

// =============================================================================
// Full Page Cluster Management
// =============================================================================

let cmCurrentNodes = 0;
let cmTerminal = null;
let cmTerminalSocket = null;
let cmFitAddon = null;
let cmSelectedNode = null;
let cmLogViewNode = null;

function openClusterManagement(currentNodes = null, targetNodes = null) {
    const view = document.getElementById('cluster-management-view');
    const appContainer = document.querySelector('.app-container');
    const overlay = document.getElementById('cm-loading-overlay');

    overlay.style.display = 'flex';

    Promise.all([
        fetch('/api/cluster/status').then(r => r.json()),
        fetch('/api/cluster/nodes').then(r => r.json())
    ]).then(([data, nodesData]) => {
            const nodes = nodesData.nodes || [];
            cmCurrentNodes = parseInt(data.cluster_size) || parseInt(data.ns_cluster_size) || 0;

            document.getElementById('cm-current-nodes').textContent = cmCurrentNodes || '-';
            document.getElementById('cm-sc-mode').textContent = data.strong_consistency ? 'Enabled' : 'Disabled';
            document.getElementById('cm-sc-mode').className = 'cm-info-value ' + (data.strong_consistency ? 'success' : 'warning');
            document.getElementById('cm-rf').textContent = data.replication_factor || '-';

            const offlineNodes = nodes.filter(n => n.status !== 'online');
            const deadPartitions = parseInt(data.dead_partitions) || 0;
            const unavailPartitions = parseInt(data.unavailable_partitions) || 0;
            const clusterMismatch = data.aerospike_cluster_size && data.container_count &&
                                    parseInt(data.aerospike_cluster_size) < parseInt(data.container_count);
            const isHealthy = offlineNodes.length === 0 && deadPartitions === 0 &&
                              unavailPartitions === 0 && !clusterMismatch;

            document.getElementById('cm-health').textContent = isHealthy ? 'Healthy' : 'Issues';
            document.getElementById('cm-health').className = 'cm-info-value ' + (isHealthy ? 'success' : 'error');

            const healthBanner = document.getElementById('cm-health-banner');
            if (!isHealthy) {
                healthBanner.style.display = 'flex';
                document.getElementById('cm-health-banner-content').innerHTML = '<em>Analyzing cluster health...</em>';
                if (offlineNodes.length > 0) {
                    const offlineNames = offlineNodes.map(n => n.container).join(', ');
                    data.diagnostics = data.diagnostics || [];
                    data.diagnostics.push(`Aerospike process is DOWN on: ${offlineNames}`);
                }
                getHealthInsight(data);
            } else {
                healthBanner.style.display = 'none';
            }

            const targetSelect = document.getElementById('cm-target-nodes');
            targetSelect.value = targetNodes || cmCurrentNodes || 2;

            view.style.display = 'flex';
            appContainer.style.display = 'none';
            overlay.style.display = 'none';

            if (!cmTerminal) initCmTerminal();
            setTimeout(cmFitAndResize, 200);

            renderNodes(nodes);

            if (targetNodes && targetNodes !== cmCurrentNodes) {
                setTimeout(() => startScaling(), 100);
            }
        })
        .catch(err => {
            console.error('Failed to fetch cluster status:', err);
            view.style.display = 'flex';
            appContainer.style.display = 'none';
            overlay.style.display = 'none';
            if (!cmTerminal) initCmTerminal();
            refreshNodes();
        });
}

function closeClusterManagement() {
    const view = document.getElementById('cluster-management-view');
    const appContainer = document.querySelector('.app-container');

    // Disconnect CM terminal
    if (cmTerminalSocket) {
        cmTerminalSocket.close();
        cmTerminalSocket = null;
    }

    view.style.display = 'none';
    appContainer.style.display = 'flex';

    checkClusterStatus();
    setTimeout(fitAndResize, 100);
}

// ---- CM Terminal ----

function initCmTerminal() {
    cmTerminal = new Terminal({
        theme: getActiveTermTheme(),
        fontFamily: '"IBM Plex Mono", Consolas, monospace',
        fontSize: 13,
        lineHeight: 1.35,
        cursorBlink: true,
        cursorStyle: 'bar',
        scrollback: 1000,
        convertEol: true,
        allowProposedApi: true
    });

    cmFitAddon = new window.FitAddon.FitAddon();
    cmTerminal.loadAddon(cmFitAddon);
    cmTerminal.open(document.getElementById('cm-terminal'));
    try { cmTerminal.loadAddon(new window.WebglAddon.WebglAddon()); } catch(e) { console.warn('WebGL addon failed for CM terminal:', e); }
    enableTermCopyPaste(cmTerminal, () => cmTerminalSocket);

    setTimeout(cmFitAndResize, 100);

    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(cmFitAndResize, 100);
    });

    cmTerminal.onData(data => {
        if (cmTerminalSocket && cmTerminalSocket.readyState === WebSocket.OPEN) {
            cmTerminalSocket.send(JSON.stringify({ type: 'input', data: data }));
        }
    });

    cmTerminal.write('\x1b[2m Select a node above to open a terminal session \x1b[0m');

    document.getElementById('cm-copy-terminal').addEventListener('click', function() {
        copyTerminalContent(cmTerminal, this);
    });
    document.getElementById('cm-clear-terminal').addEventListener('click', () => {
        cmTerminal.clear();
    });
}

function connectCmTerminal(containerName) {
    if (cmTerminalSocket) cmTerminalSocket.close();

    cmTerminal.clear();
    cmTerminal.writeln(`\x1b[36mConnecting to ${containerName}...\x1b[0m`);

    const statusEl = document.getElementById('cm-terminal-status');
    statusEl.querySelector('.status-dot').className = 'status-dot';
    statusEl.querySelector('.status-text').textContent = 'Connecting...';

    updateTabNodeLabel();

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    cmTerminalSocket = new WebSocket(`${protocol}//${window.location.host}/ws/terminal/node/${containerName}`);

    cmTerminalSocket.onopen = () => {
        cmTerminal.clear();
        cmTerminal.focus();
        cmFitAndResize();
        statusEl.querySelector('.status-dot').className = 'status-dot connected';
        statusEl.querySelector('.status-text').textContent = `Connected to ${containerName}`;
    };

    cmTerminalSocket.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.type === 'output') {
            cmTerminal.write(msg.data);
        } else if (msg.type === 'error') {
            cmTerminal.writeln(`\r\n\x1b[31m${msg.data}\x1b[0m`);
        }
    };

    cmTerminalSocket.onclose = () => {
        statusEl.querySelector('.status-dot').className = 'status-dot disconnected';
        statusEl.querySelector('.status-text').textContent = 'Disconnected';
    };

    cmTerminalSocket.onerror = () => {
        statusEl.querySelector('.status-dot').className = 'status-dot disconnected';
        statusEl.querySelector('.status-text').textContent = 'Connection error';
    };
}

function clearCmTerminal() { if (cmTerminal) cmTerminal.clear(); }

function copyTerminalContent(term, btnEl) {
    if (!term) return;
    term.selectAll();
    const text = term.getSelection();
    term.clearSelection();
    if (text) {
        navigator.clipboard.writeText(text).then(() => {
            const orig = btnEl.innerHTML;
            btnEl.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>';
            setTimeout(() => { btnEl.innerHTML = orig; }, 1500);
        }).catch(() => {});
    }
}

function toggleCmTerminal() {
    switchCmTab('terminal');
    setTimeout(() => {
        cmFitAndResize();
        if (cmTerminal) cmTerminal.focus();
    }, 100);
}

// ---- Nodes ----

async function refreshNodes() {
    const grid = document.getElementById('cm-nodes-grid');
    grid.innerHTML = '<div class="cm-nodes-loading">Loading nodes...</div>';

    try {
        const resp = await fetch('/api/cluster/nodes');
        const data = await resp.json();
        const nodes = data.nodes || [];
        renderNodes(nodes);
    } catch (err) {
        grid.innerHTML = '<div class="cm-nodes-loading">Failed to load nodes</div>';
    }
}

async function refreshClusterHealth() {
    try {
        const [statusResp, nodesResp] = await Promise.all([
            fetch('/api/cluster/status'),
            fetch('/api/cluster/nodes')
        ]);
        const data = await statusResp.json();
        const nodesData = await nodesResp.json();
        const nodes = nodesData.nodes || [];

        cmCurrentNodes = parseInt(data.cluster_size) || parseInt(data.ns_cluster_size) || 0;

        document.getElementById('cm-current-nodes').textContent = cmCurrentNodes || '-';
        document.getElementById('cm-sc-mode').textContent = data.strong_consistency ? 'Enabled' : 'Disabled';
        document.getElementById('cm-sc-mode').className = 'cm-info-value ' + (data.strong_consistency ? 'success' : 'warning');
        document.getElementById('cm-rf').textContent = data.replication_factor || '-';

        const offlineNodes = nodes.filter(n => n.status !== 'online');
        const hasDiagnostics = data.diagnostics && data.diagnostics.length > 0;
        const deadPartitions = parseInt(data.dead_partitions) || 0;
        const unavailPartitions = parseInt(data.unavailable_partitions) || 0;
        const clusterMismatch = data.aerospike_cluster_size && data.container_count &&
                                parseInt(data.aerospike_cluster_size) < parseInt(data.container_count);
        const isHealthy = offlineNodes.length === 0 && deadPartitions === 0 &&
                          unavailPartitions === 0 && !clusterMismatch;

        document.getElementById('cm-health').textContent = isHealthy ? 'Healthy' : 'Issues';
        document.getElementById('cm-health').className = 'cm-info-value ' + (isHealthy ? 'success' : 'error');

        const healthBanner = document.getElementById('cm-health-banner');
        if (!isHealthy) {
            healthBanner.style.display = 'flex';
            document.getElementById('cm-health-banner-content').innerHTML = '<em>Analyzing cluster health...</em>';
            if (offlineNodes.length > 0) {
                const offlineNames = offlineNodes.map(n => n.container).join(', ');
                data.diagnostics = data.diagnostics || [];
                data.diagnostics.push(`Aerospike process is DOWN on: ${offlineNames}`);
            }
            getHealthInsight(data);
        } else {
            healthBanner.style.display = 'none';
        }

        renderNodes(nodes);
    } catch (err) {
        console.error('Failed to refresh cluster health:', err);
    }
}

function renderNodes(nodes) {
    const grid = document.getElementById('cm-nodes-grid');
    if (!nodes.length) {
        grid.innerHTML = '<div class="cm-nodes-loading">No nodes found. Set up a cluster first.</div>';
        return;
    }

    grid.innerHTML = '';
    nodes.forEach(node => {
        const card = document.createElement('div');
        card.className = 'cm-node-card' + (node.status !== 'online' ? ' offline' : '') +
                         (cmSelectedNode === node.container ? ' selected' : '');
        card.onclick = (e) => {
            if (e.target.closest('.cm-node-action-btn')) return;
            selectNode(node.container);
        };

        card.innerHTML = `
            <div class="cm-node-top">
                <div class="cm-node-status ${node.status === 'online' ? '' : 'offline'}"></div>
                ${node.is_principal ? '<span class="cm-node-badge principal">Principal</span>' : ''}
            </div>
            <div class="cm-node-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/>
                    <circle cx="6" cy="6" r="1" fill="currentColor"/><circle cx="6" cy="18" r="1" fill="currentColor"/>
                    <line x1="10" y1="6" x2="18" y2="6" stroke-width="1"/><line x1="10" y1="18" x2="18" y2="18" stroke-width="1"/>
                </svg>
            </div>
            <div class="cm-node-name">Node ${node.node_num}</div>
            <div class="cm-node-container-name">${node.container}</div>
            <div class="cm-node-ip">${node.ip || 'No IP'}</div>
            <div class="cm-node-actions">
                <button class="cm-node-action-btn" onclick="selectNode('${node.container}')" title="Open terminal">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>
                    Terminal
                </button>
                <button class="cm-node-action-btn" onclick="openConfigEditor('${node.container}')" title="Edit config">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
                    Config
                </button>
                <button class="cm-node-action-btn" onclick="viewNodeLogs('${node.container}')" title="View logs">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                    Logs
                </button>
            </div>
        `;
        grid.appendChild(card);
    });
}

// ---- Health Insight (AI) ----

let _healthInsightInFlight = false;

async function getHealthInsight(statusData) {
    if (_healthInsightInFlight) return;

    const banner = document.getElementById('cm-health-banner-content');
    const diagnostics = statusData.diagnostics || [];
    const warnings = statusData.warnings || [];

    if (!diagnostics.length && !warnings.length &&
        !statusData.dead_partitions && !statusData.unavailable_partitions) {
        banner.innerHTML = 'Health issues detected but no details available.';
        return;
    }

    _healthInsightInFlight = true;
    try {
        const resp = await fetch('/api/cluster/health-insight', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ diagnostics, warnings })
        });
        const data = await resp.json();
        const healthBanner = document.getElementById('cm-health-banner');
        if (healthBanner.style.display === 'none') return;
        if (data.insight) {
            banner.innerHTML = '<strong>AI Insight:</strong> ' + data.insight.replace(/\n/g, '<br>');
        } else if (data.error) {
            banner.innerHTML = '<strong>Issues:</strong> ' + diagnostics.join(' · ');
        }
    } catch (err) {
        banner.innerHTML = '<strong>Issues:</strong> ' + diagnostics.join(' · ');
    } finally {
        _healthInsightInFlight = false;
    }
}

// ---- Tab Switching ----

let cmConfigNode = null;

function switchCmTab(tab) {
    document.querySelectorAll('.cm-tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
    document.querySelectorAll('.cm-tab-content').forEach(p => p.classList.remove('active'));
    const panel = document.getElementById('cm-tab-' + tab);
    if (panel) panel.classList.add('active');

    if (tab === 'terminal' && cmFitAddon) {
        setTimeout(cmFitAndResize, 50);
    }
}

function updateTabNodeLabel() {
    const label = document.getElementById('cm-tab-node-label');
    if (label) label.textContent = cmSelectedNode || 'No node selected';
}

function selectNode(containerName) {
    cmSelectedNode = containerName;
    updateTabNodeLabel();

    document.querySelectorAll('.cm-node-card').forEach(c => c.classList.remove('selected'));
    document.querySelectorAll('.cm-node-card').forEach(c => {
        const nameEl = c.querySelector('.cm-node-container-name');
        if (nameEl && nameEl.textContent === containerName) c.classList.add('selected');
    });

    switchCmTab('terminal');
    connectCmTerminal(containerName);
}

// ---- Node Logs (Logs tab) ----

async function viewNodeLogs(containerName) {
    cmLogViewNode = containerName;
    cmSelectedNode = containerName;
    updateTabNodeLabel();

    document.querySelectorAll('.cm-node-card').forEach(c => c.classList.remove('selected'));
    document.querySelectorAll('.cm-node-card').forEach(c => {
        const nameEl = c.querySelector('.cm-node-container-name');
        if (nameEl && nameEl.textContent === containerName) c.classList.add('selected');
    });

    const title = document.getElementById('cm-detail-title');
    const logsEl = document.getElementById('cm-node-logs');

    title.textContent = `Logs — ${containerName}`;
    logsEl.textContent = 'Loading logs...';
    switchCmTab('logs');

    try {
        const resp = await fetch(`/api/cluster/nodes/${containerName}/logs`);
        const data = await resp.json();
        logsEl.textContent = data.logs || 'No logs available.';
        logsEl.scrollTop = logsEl.scrollHeight;
    } catch (err) {
        logsEl.textContent = 'Failed to load logs: ' + err.message;
    }
}

function refreshNodeLogs() {
    if (cmLogViewNode) viewNodeLogs(cmLogViewNode);
}

function closeNodeDetail() {
    switchCmTab('terminal');
}

// ---- Config Editor (Config tab) ----

async function openConfigEditor(containerName) {
    cmConfigNode = containerName;
    cmSelectedNode = containerName;
    updateTabNodeLabel();

    document.querySelectorAll('.cm-node-card').forEach(c => c.classList.remove('selected'));
    document.querySelectorAll('.cm-node-card').forEach(c => {
        const nameEl = c.querySelector('.cm-node-container-name');
        if (nameEl && nameEl.textContent === containerName) c.classList.add('selected');
    });

    const title = document.getElementById('cm-config-title');
    const textarea = document.getElementById('cm-config-textarea');
    const status = document.getElementById('cm-config-status');

    title.textContent = `aerospike.conf — ${containerName}`;
    textarea.value = 'Loading config...';
    textarea.disabled = true;
    status.textContent = '';
    status.className = 'cm-config-status';
    switchCmTab('config');

    try {
        const resp = await fetch(`/api/cluster/nodes/${containerName}/config`);
        const data = await resp.json();
        textarea.value = data.config || '';
        textarea.disabled = false;
        if (data.error) {
            status.textContent = 'Warning: ' + data.error;
            status.className = 'cm-config-status error';
        }
    } catch (err) {
        textarea.value = '';
        status.textContent = 'Failed to load config: ' + err.message;
        status.className = 'cm-config-status error';
    }
}

async function saveNodeConfig() {
    if (!cmConfigNode) return;
    const textarea = document.getElementById('cm-config-textarea');
    const status = document.getElementById('cm-config-status');
    const saveBtn = document.getElementById('cm-config-save');
    const saveBtnHtml = saveBtn.innerHTML;

    const content = textarea.value;
    if (!content.trim()) {
        status.textContent = 'Config cannot be empty';
        status.className = 'cm-config-status error';
        return;
    }

    saveBtn.disabled = true;
    saveBtn.textContent = 'Saving...';
    status.textContent = 'Writing config to ' + cmConfigNode + '...';
    status.className = 'cm-config-status';

    try {
        const saveResp = await fetch(`/api/cluster/nodes/${cmConfigNode}/config`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ config: content })
        });
        const saveData = await saveResp.json();

        if (!saveData.success) {
            status.textContent = 'Save failed: ' + (saveData.error || 'Unknown error');
            status.className = 'cm-config-status error';
            saveBtn.disabled = false;
            saveBtn.innerHTML = saveBtnHtml;
            return;
        }

        status.textContent = 'Config saved. Restarting Aerospike on ' + cmConfigNode + '...';
        status.className = 'cm-config-status';

        const restartResp = await fetch(`/api/cluster/nodes/${cmConfigNode}/restart`, { method: 'POST' });
        const restartData = await restartResp.json();

        if (restartData.success) {
            status.textContent = 'Config saved and Aerospike restarted on ' + cmConfigNode;
            status.className = 'cm-config-status success';
            setTimeout(() => { refreshNodes(); refreshClusterHealth(); }, 3000);
        } else {
            status.textContent = 'Config saved but restart failed: ' + (restartData.error || 'Unknown error');
            status.className = 'cm-config-status error';
        }
    } catch (err) {
        status.textContent = 'Error: ' + err.message;
        status.className = 'cm-config-status error';
    }

    saveBtn.disabled = false;
    saveBtn.innerHTML = saveBtnHtml;
}

function closeConfigEditor() {
    switchCmTab('terminal');
}

// ---- Operation Logs ----

function toggleOpLogs() {
    const logs = document.getElementById('cm-logs');
    logs.style.display = logs.style.display === 'none' ? 'block' : 'none';
}

function clearLogs() {
    document.getElementById('cm-logs').innerHTML = 'Logs cleared.\n';
}

function resetClusterManagement() {
    document.getElementById('cm-status-section').style.display = 'none';
    document.getElementById('cm-scale-btn').disabled = false;
    openClusterManagement();
}

function startScaling() {
    if (isScaling) return;

    const targetCount = parseInt(document.getElementById('cm-target-nodes').value);
    const fromCount = cmCurrentNodes;

    if (targetCount === fromCount) {
        appendLog('Target node count is same as current. No scaling needed.');
        return;
    }

    document.getElementById('cm-status-section').style.display = 'block';
    document.getElementById('cm-from-nodes').textContent = fromCount;
    document.getElementById('cm-to-nodes').textContent = targetCount;
    document.getElementById('cm-op-status').textContent = 'Connecting...';
    document.getElementById('cm-op-status').className = 'cm-op-status';
    document.getElementById('cm-scale-btn').disabled = true;
    // Show operation logs
    document.getElementById('cm-logs').style.display = 'block';
    document.getElementById('cm-logs').innerHTML = '';
    appendLog(`<span class="log-header">=== Cluster Scaling: ${fromCount} → ${targetCount} nodes ===</span>`);
    appendLog('');

    isScaling = true;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws/cluster/scale`);

    ws.onopen = () => {
        ws.send(JSON.stringify({
            action: targetCount > fromCount ? 'scale_up' : 'scale_down',
            current_count: fromCount,
            target_count: targetCount
        }));
    };

    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);

        if (msg.type === 'log') {
            appendLog(formatLogLine(msg.data));
        } else if (msg.type === 'status') {
            document.getElementById('cm-op-status').textContent = msg.data;
        } else if (msg.type === 'complete') {
            const statusEl = document.getElementById('cm-op-status');
            statusEl.textContent = msg.success ? 'Complete!' : 'Failed';
            statusEl.className = 'cm-op-status ' + (msg.success ? 'success' : 'error');
            document.getElementById('cm-scale-btn').disabled = false;

            const dot = document.querySelector('.cm-logs-dot');
            if (dot) dot.classList.add('inactive');

            isScaling = false;
            cmCurrentNodes = targetCount;
            document.getElementById('cm-current-nodes').textContent = targetCount;

            if (msg.success) {
                appendLog('');
                appendLog('<span class="log-success">✓ Scaling operation completed successfully!</span>');
                setTimeout(() => {
                    refreshNodes();
                    refreshClusterHealth();
                    // Hide operation status and logs after a moment
                    setTimeout(() => {
                        document.getElementById('cm-status-section').style.display = 'none';
                        document.getElementById('cm-logs').style.display = 'none';
                    }, 3000);
                }, 2000);
            } else {
                appendLog('');
                appendLog(`<span class="log-error">✗ Scaling failed: ${msg.message || 'Unknown error'}</span>`);
            }
        }
    };

    ws.onerror = () => {
        document.getElementById('cm-op-status').textContent = 'Connection error';
        document.getElementById('cm-op-status').className = 'cm-op-status error';
        document.getElementById('cm-scale-btn').disabled = false;
        isScaling = false;
        appendLog('<span class="log-error">WebSocket connection error</span>');
    };

    ws.onclose = () => {
        if (isScaling) {
            document.getElementById('cm-op-status').textContent = 'Disconnected';
            document.getElementById('cm-scale-btn').disabled = false;
            isScaling = false;
        }
    };
}

function appendLog(line) {
    const logsEl = document.getElementById('cm-logs');
    logsEl.innerHTML += line + '\n';
    logsEl.scrollTop = logsEl.scrollHeight;
}

function formatLogLine(line) {
    let escaped = line.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    if (escaped.match(/^Step \d+:/i)) return `<span class="log-step">${escaped}</span>`;
    if (escaped.startsWith('$')) return `<span class="log-cmd">${escaped}</span>`;
    if (escaped.toLowerCase().includes('done') || escaped.toLowerCase().includes('success') ||
        escaped.toLowerCase().includes('complete') || escaped.toLowerCase().includes('stable'))
        return `<span class="log-success">${escaped}</span>`;
    if (escaped.toLowerCase().includes('error') || escaped.toLowerCase().includes('failed'))
        return `<span class="log-error">${escaped}</span>`;
    if (escaped.toLowerCase().includes('warning') || escaped.toLowerCase().includes('warn'))
        return `<span class="log-warning">${escaped}</span>`;
    if (escaped.startsWith('===')) return `<span class="log-header">${escaped}</span>`;

    return escaped;
}

function closeScaleModal() {
    const el = document.getElementById('scale-modal');
    if (el) el.style.display = 'none';
}

// =============================================================================
// INTERACTIVE GUIDED STEPS
// =============================================================================

const guidedProgress = {};

function completeStep(guideId, stepNum) {
    if (!guidedProgress[guideId]) guidedProgress[guideId] = new Set();
    guidedProgress[guideId].add(stepNum);

    const container = document.querySelector(`.guided-steps[data-guided="${guideId}"]`);
    if (!container) return;

    const steps = container.querySelectorAll('.guided-step');
    let nextActivated = false;

    steps.forEach(step => {
        const num = parseInt(step.dataset.step);

        if (guidedProgress[guideId].has(num)) {
            step.className = 'guided-step completed';
        } else if (!nextActivated) {
            step.className = 'guided-step active';
            nextActivated = true;
            // Smooth-scroll the newly active step into view
            setTimeout(() => {
                step.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 150);
        } else {
            step.className = 'guided-step locked';
        }
    });

    // Check if all steps done
    if (guidedProgress[guideId].size >= steps.length) {
        const summary = document.getElementById(`${guideId}-summary`);
        if (summary) {
            summary.style.display = 'block';
            setTimeout(() => {
                summary.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 200);
        }
    }
}

window.completeStep = completeStep;

// =============================================================================
// THEME TOGGLE
// =============================================================================

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const collapsed = sidebar.classList.toggle('collapsed');
    localStorage.setItem('sc-sidebar', collapsed ? 'collapsed' : 'expanded');
    setTimeout(fitAndResize, 280);
}

function toggleTheme() {
    const root = document.documentElement;
    const isLight = root.classList.toggle('light');
    localStorage.setItem('sc-theme', isLight ? 'light' : 'dark');

    const hljsDark = document.getElementById('hljs-dark');
    const hljsLight = document.getElementById('hljs-light');
    if (hljsDark && hljsLight) {
        hljsDark.disabled = isLight;
        hljsLight.disabled = !isLight;
    }

    if (terminal) {
        terminal.options.theme = getActiveTermTheme();
    }
    if (cmTerminal) {
        cmTerminal.options.theme = getActiveTermTheme();
    }
}

// =============================================================================
// AI CHAT
// =============================================================================

let chatOpen = false;
let chatBusy = false;

function toggleChat() {
    chatOpen = !chatOpen;
    const sidebar = document.getElementById('chat-sidebar');
    const fab = document.getElementById('chat-fab');

    if (chatOpen) {
        sidebar.classList.add('open');
        fab.classList.add('hidden');
        setTimeout(() => {
            document.getElementById('chat-input').focus();
        }, 280);
        checkApiKeyStatus();
    } else {
        sidebar.classList.remove('open');
        fab.classList.remove('hidden');
        closeChatSettings();
    }
}

function clearChat() {
    const messages = document.getElementById('chat-messages');
    messages.innerHTML = `
        <div class="chat-msg assistant">
            <div class="chat-msg-content">
                Chat cleared. Ask me anything about Aerospike Strong Consistency!
            </div>
        </div>
    `;
}

function getChatContext() {
    const cmView = document.getElementById('cluster-management-view');
    if (cmView && cmView.style.display !== 'none') {
        let ctx = 'Cluster Management page (live configs + logs from all nodes)';
        if (cmSelectedNode) ctx += ` — connected to ${cmSelectedNode}`;
        return ctx;
    }
    if (currentLesson >= 0 && currentLesson < LESSONS.length) {
        const l = LESSONS[currentLesson];
        return `Lesson ${l.id}: ${l.title}`;
    }
    return 'Welcome page';
}

function updateChatContext() {
    const label = document.getElementById('chat-context-label');
    if (label) {
        label.textContent = 'Context: ' + getChatContext();
    }
}

function handleChatKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendChatMessage();
    }
    // Auto-resize textarea
    const el = e.target;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 100) + 'px';
}

async function sendChatMessage() {
    if (chatBusy) return;
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;

    const messages = document.getElementById('chat-messages');

    // Add user message
    const userDiv = document.createElement('div');
    userDiv.className = 'chat-msg user';
    userDiv.innerHTML = `<div class="chat-msg-content">${escapeHtml(message)}</div>`;
    messages.appendChild(userDiv);

    // Clear input
    input.value = '';
    input.style.height = 'auto';

    // Add typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-msg assistant';
    typingDiv.id = 'chat-typing';
    typingDiv.innerHTML = '<div class="chat-typing"><span></span><span></span><span></span></div>';
    messages.appendChild(typingDiv);
    messages.scrollTop = messages.scrollHeight;

    chatBusy = true;
    document.getElementById('chat-send-btn').disabled = true;

    try {
        const resp = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                lesson_context: getChatContext()
            })
        });
        const data = await resp.json();

        // Remove typing indicator
        const typing = document.getElementById('chat-typing');
        if (typing) typing.remove();

        // Add assistant response
        const assistantDiv = document.createElement('div');
        assistantDiv.className = 'chat-msg assistant';
        if (data.error) {
            assistantDiv.innerHTML = `<div class="chat-msg-content" style="border-color:var(--accent-error);color:var(--accent-error);">${escapeHtml(data.error)}</div>`;
        } else {
            assistantDiv.innerHTML = `<div class="chat-msg-content">${renderMarkdown(data.answer)}</div>`;
        }
        messages.appendChild(assistantDiv);
    } catch (err) {
        const typing = document.getElementById('chat-typing');
        if (typing) typing.remove();
        const errDiv = document.createElement('div');
        errDiv.className = 'chat-msg assistant';
        errDiv.innerHTML = `<div class="chat-msg-content" style="border-color:var(--accent-error);color:var(--accent-error);">Network error. Please try again.</div>`;
        messages.appendChild(errDiv);
    }

    chatBusy = false;
    document.getElementById('chat-send-btn').disabled = false;
    messages.scrollTop = messages.scrollHeight;
}

function renderMarkdown(text) {
    // Code blocks
    text = text.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
        return `<pre><code>${escapeHtml(code.trim())}</code></pre>`;
    });
    // Inline code
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    // Bold
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    // Italic
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
    // Unordered lists
    text = text.replace(/^[\-\*] (.+)$/gm, '<li>$1</li>');
    text = text.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
    // Ordered lists
    text = text.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
    // Paragraphs (double newline)
    text = text.replace(/\n\n/g, '</p><p>');
    // Single newlines inside paragraphs
    text = text.replace(/\n/g, '<br>');
    return '<p>' + text + '</p>';
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Settings
function openChatSettings() {
    document.getElementById('chat-settings').style.display = 'block';
    document.getElementById('chat-messages').style.display = 'none';
    document.querySelector('.chat-input-area').style.display = 'none';
    checkApiKeyStatus();
}

function closeChatSettings() {
    document.getElementById('chat-settings').style.display = 'none';
    document.getElementById('chat-messages').style.display = 'flex';
    document.querySelector('.chat-input-area').style.display = 'block';
}

async function checkApiKeyStatus() {
    try {
        const resp = await fetch('/api/admin/apikey');
        const data = await resp.json();
        const statusEl = document.getElementById('api-key-status');
        const badge = document.getElementById('chat-badge');
        if (data.configured) {
            statusEl.textContent = `Key configured: ${data.masked}`;
            statusEl.style.color = 'var(--accent-secondary)';
            if (badge) badge.style.display = 'inline';
        } else {
            statusEl.textContent = 'No API key configured.';
            statusEl.style.color = 'var(--accent-warning)';
            if (badge) badge.style.display = 'none';
        }
    } catch (e) {
        // ignore
    }
}

async function saveApiKey() {
    const input = document.getElementById('api-key-input');
    const key = input.value.trim();
    if (!key) return;

    try {
        const resp = await fetch('/api/admin/apikey', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_key: key })
        });
        const data = await resp.json();
        if (data.success) {
            input.value = '';
            checkApiKeyStatus();
            closeChatSettings();
        } else {
            const statusEl = document.getElementById('api-key-status');
            statusEl.textContent = data.error;
            statusEl.style.color = 'var(--accent-error)';
        }
    } catch (e) {
        // ignore
    }
}

// Update chat context whenever lesson changes
const _originalLoadLesson = loadLesson;
window.loadLesson = function(lessonId) {
    _originalLoadLesson(lessonId);
    updateChatContext();
};

// =============================================================================
// TERMINAL OUTPUT MONITORING — Auto-AI on errors & notable output
// =============================================================================

const terminalOutputBuffer = [];
const BUFFER_MAX = 80;
let autoAnalyzeTimer = null;
let lastAnalyzedSnippet = '';
let autoAIEnabled = localStorage.getItem('autoAIEnabled') !== 'false';

function toggleAutoAI() {
    autoAIEnabled = !autoAIEnabled;
    localStorage.setItem('autoAIEnabled', autoAIEnabled);
    updateAutoAIButton();
}

function updateAutoAIButton() {
    const btn = document.getElementById('auto-ai-toggle');
    if (!btn) return;
    btn.classList.toggle('active', autoAIEnabled);
    btn.title = autoAIEnabled ? 'Auto-analysis ON — click to disable' : 'Auto-analysis OFF — click to enable';
}
// Initialize on load
document.addEventListener('DOMContentLoaded', updateAutoAIButton);

const ERROR_PATTERNS = [
    /Error:\s*\(-?\d+\)/i,
    /AEROSPIKE_ERR/i,
    /error\s*code/i,
    /PARTITION_UNAVAILABLE/i,
    /INVALID_NODE_ERROR/i,
    /not found for partition/i,
    /FAIL_FORBIDDEN/i,
    /FORBIDDEN/i,
    /Generation error/i,
    /Traceback \(most recent/i,
    /exception\./i,
    /Connection refused/i,
    /timed?\s*out/i,
    /dead_partitions/i,
    /unavailable_partitions/i,
];

const SUCCESS_PATTERNS = [
    /OK,\s*\d+\s+record/i,
    /Successfully started recluster/i,
    /Pending roster now contains/i,
    /1 row in set/i,
];

function captureTerminalLine(text) {
    const cleaned = text.replace(/\x1b\[[0-9;]*[a-zA-Z]/g, '').trim();
    if (!cleaned || cleaned.length < 3) return;

    terminalOutputBuffer.push(cleaned);
    if (terminalOutputBuffer.length > BUFFER_MAX) {
        terminalOutputBuffer.splice(0, terminalOutputBuffer.length - BUFFER_MAX);
    }

    if (!autoAIEnabled) return;

    clearTimeout(autoAnalyzeTimer);
    autoAnalyzeTimer = setTimeout(() => analyzeRecentOutput(), 1500);
}

function analyzeRecentOutput() {
    const recent = terminalOutputBuffer.slice(-20).join('\n');
    if (!recent || recent === lastAnalyzedSnippet) return;

    let isError = false;
    let isSuccess = false;

    for (const pat of ERROR_PATTERNS) {
        if (pat.test(recent)) { isError = true; break; }
    }
    if (!isError) {
        for (const pat of SUCCESS_PATTERNS) {
            if (pat.test(recent)) { isSuccess = true; break; }
        }
    }

    if (!isError && !isSuccess) return;

    lastAnalyzedSnippet = recent;

    const snippet = terminalOutputBuffer.slice(-15).join('\n');
    autoExplainOutput(snippet, isError);
}

async function autoExplainOutput(snippet, isError) {
    if (chatBusy) return;
    const apiKey = await fetch('/api/admin/apikey').then(r => r.json()).catch(() => null);
    if (!apiKey || !apiKey.configured) return;

    // Open chat panel if closed
    if (!chatOpen) toggleChat();

    const messages = document.getElementById('chat-messages');

    // Show system message about what triggered the auto-analysis
    const sysDiv = document.createElement('div');
    sysDiv.className = 'chat-msg system';
    sysDiv.innerHTML = `<div class="chat-msg-content">${isError ? 'Error detected' : 'Command succeeded'} in ${currentTerminalType.toUpperCase()} terminal — analyzing...</div>`;
    messages.appendChild(sysDiv);

    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-msg assistant';
    typingDiv.id = 'chat-typing';
    typingDiv.innerHTML = '<div class="chat-typing"><span></span><span></span><span></span></div>';
    messages.appendChild(typingDiv);
    messages.scrollTop = messages.scrollHeight;

    chatBusy = true;

    const prompt = isError
        ? `The user just got this output/error in their ${currentTerminalType.toUpperCase()} terminal while learning about Aerospike Strong Consistency. Explain what went wrong, why it happened, and what they should do to fix it. Be concise and helpful.\n\nTerminal output:\n\`\`\`\n${snippet}\n\`\`\``
        : `The user just ran a command in their ${currentTerminalType.toUpperCase()} terminal while learning about Aerospike Strong Consistency. Briefly explain what happened and what they should notice in the output. Be concise.\n\nTerminal output:\n\`\`\`\n${snippet}\n\`\`\``;

    try {
        const resp = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: prompt,
                lesson_context: getChatContext()
            })
        });
        const data = await resp.json();

        const typing = document.getElementById('chat-typing');
        if (typing) typing.remove();

        const assistantDiv = document.createElement('div');
        assistantDiv.className = 'chat-msg assistant';
        if (data.error) {
            assistantDiv.innerHTML = `<div class="chat-msg-content" style="border-color:var(--accent-error);color:var(--accent-error);">${escapeHtml(data.error)}</div>`;
        } else {
            assistantDiv.innerHTML = `<div class="chat-msg-content">${renderMarkdown(data.answer)}</div>`;
        }
        messages.appendChild(assistantDiv);
    } catch (err) {
        const typing = document.getElementById('chat-typing');
        if (typing) typing.remove();
    }

    chatBusy = false;
    messages.scrollTop = messages.scrollHeight;
}

