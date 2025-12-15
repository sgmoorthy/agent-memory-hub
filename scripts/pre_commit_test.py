#!/usr/bin/env python3
"""
Pre-commit test script to validate code before pushing to repository.
Run this script before committing to catch issues early.

Usage:
    python scripts/pre_commit_test.py
"""

import subprocess
import sys
from pathlib import Path

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(message):
    """Print a formatted header."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{message:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"{YELLOW}▶ {description}...{RESET}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"{GREEN}✓ {description} passed{RESET}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}✗ {description} failed{RESET}")
        print(f"{RED}Error output:{RESET}")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    """Run all pre-commit checks."""
    print_header("PRE-COMMIT VALIDATION")
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    
    checks = [
        # 1. Linting
        ("ruff check .", "Linting with Ruff"),
        
        # 2. Security checks
        ("pip-audit", "Security audit with pip-audit"),
        ("bandit -r agent_memory_hub", "Security scan with Bandit"),
        
        # 3. Tests
        ("pytest tests/ -v --tb=short", "Running test suite"),
        
        # 4. Coverage check
        ("pytest --cov=agent_memory_hub --cov-report=term-missing --cov-fail-under=70", 
         "Coverage check (minimum 70%)"),
        
        # 5. Build check
        ("python -m build --outdir dist/", "Building package"),
    ]
    
    results = []
    for cmd, description in checks:
        success = run_command(cmd, description)
        results.append((description, success))
    
    # Summary
    print_header("SUMMARY")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = f"{GREEN}✓ PASS{RESET}" if success else f"{RED}✗ FAIL{RESET}"
        print(f"{status} - {description}")
    
    print(f"\n{BLUE}Results: {passed}/{total} checks passed{RESET}\n")
    
    if passed == total:
        print(f"{GREEN}{'='*60}{RESET}")
        print(f"{GREEN}All checks passed! Safe to commit.{RESET}")
        print(f"{GREEN}{'='*60}{RESET}\n")
        return 0
    else:
        print(f"{RED}{'='*60}{RESET}")
        print(f"{RED}Some checks failed. Please fix before committing.{RESET}")
        print(f"{RED}{'='*60}{RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
