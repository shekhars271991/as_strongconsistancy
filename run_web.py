#!/usr/bin/env python3
"""
Aerospike Strong Consistency Tutorial - Web UI

Run this script to start the web-based tutorial.

Usage:
    python run_web.py                 # Start on http://localhost:8000
    python run_web.py --port 3000     # Use different port
"""

import argparse
import uvicorn
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser(
        description='Aerospike Strong Consistency Tutorial - Web UI'
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=8000,
        help='Port to listen on (default: 8000)'
    )
    parser.add_argument(
        '--reload',
        action='store_true',
        help='Enable auto-reload for development'
    )
    
    args = parser.parse_args()
    
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║         🚀 Aerospike Strong Consistency Tutorial                 ║
║                                                                  ║
║   Starting web server at: http://{args.host}:{args.port}               ║
║                                                                  ║
║   Make sure your AeroLab cluster is running!                     ║
║   Run: aerolab cluster list                                      ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "web.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()

