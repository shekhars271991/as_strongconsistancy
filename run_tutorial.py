#!/usr/bin/env python3
"""
Aerospike Strong Consistency Tutorial - Entry Point

Run this script to start the interactive tutorial.

Usage:
    python run_tutorial.py                    # Run full tutorial
    python run_tutorial.py --lessons 0        # Run specific lesson(s)
    python run_tutorial.py --non-interactive  # Non-interactive mode
    python run_tutorial.py --help             # Show help
"""

import argparse
import sys

from sc_tutorial import StrongConsistencyTutorial


def main():
    parser = argparse.ArgumentParser(
        description='Aerospike Strong Consistency Tutorial',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python run_tutorial.py                     # Run full interactive tutorial
  python run_tutorial.py --lessons 0         # AeroLab setup only
  python run_tutorial.py --lessons 3 4 5     # Run lessons 3, 4, and 5
  python run_tutorial.py --non-interactive   # Run without pauses
  python run_tutorial.py --namespace test    # Use different namespace
        '''
    )
    
    parser.add_argument(
        '--lessons', '-l',
        nargs='+',
        help='Run specific lessons (e.g., --lessons 0 1 2)'
    )
    parser.add_argument(
        '--non-interactive', '-n',
        action='store_true',
        help='Run without interactive pauses'
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Aerospike host (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=3100,
        help='Aerospike port (default: 3100)'
    )
    parser.add_argument(
        '--namespace', '-ns',
        default='test',
        help='Namespace to use (default: test)'
    )
    parser.add_argument(
        '--skip-sc-check',
        action='store_true',
        help='Skip Strong Consistency verification'
    )
    
    args = parser.parse_args()
    
    # Create tutorial
    tutorial = StrongConsistencyTutorial(
        hosts=[(args.host, args.port)],
        namespace=args.namespace,
        interactive=not args.non_interactive
    )
    
    # If only running lesson 0 (setup), skip SC check
    skip_check = args.skip_sc_check or (args.lessons and '0' in args.lessons and len(args.lessons) == 1)
    
    tutorial.run_tutorial(lessons=args.lessons, skip_sc_check=skip_check)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nTutorial terminated.")
        sys.exit(0)

