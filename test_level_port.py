#!/usr/bin/env python3
"""
NetHack Level Test Script

This script runs NetHack in test mode (-t) to check level generation
for levels from 2 to 30. It monitors the paniclog for errors and
returns an error code if any are found.
"""

import os
import sys
import subprocess
import re
import time
from pathlib import Path

# Configuration
def find_nethack_executable():
    """Find the NetHack executable in common locations"""
    # Common locations on Windows
    windows_paths = [
        r".\binary\Debug\x64\NetHack.exe",
        r".\nethack.exe",
        r".\build\nethack.exe",
        r".\binary\nethack.exe",
        r"..\binary\nethack.exe",
        r"..\nethack.exe",
        r".\src\nethack.exe",
    ]
    
    # Check if we're on Windows
    if os.name == 'nt':
        for path in windows_paths:
            if os.path.exists(path):
                print(f"Found NetHack at: {path}")
                return path
        
        # Try to find in current directory or subdirectories
        for root, dirs, files in os.walk('.', topdown=True, followlinks=False):
            # Limit depth to prevent excessive searching
            if root.count(os.sep) > 3:
                dirs.clear()  # Don't go deeper
                continue
                
            for file in files:
                if file.lower() in ('nethack.exe', 'nethackw.exe'):
                    path = os.path.join(root, file)
                    print(f"Found NetHack at: {path}")
                    return path
    
    # Default to "nethack" and let the system find it
    return "nethack"

def find_paniclog():
    """Find the paniclog file in common locations"""
    # Common locations on Windows
    if os.name == 'nt':
        # Try user's NetHack directory first
        user_dir = os.path.join(os.path.expanduser("~"), "NetHack", "3.7")
        paniclog = os.path.join(user_dir, "paniclog")
        if os.path.exists(user_dir):
            return paniclog
        
        # Try current directory
        if os.path.exists("paniclog"):
            return "paniclog"
    
    # Default location
    return os.path.join(os.path.expanduser("~"), "NetHack", "3.7", "paniclog")

NETHACK_EXECUTABLE = find_nethack_executable()
PANICLOG = find_paniclog()
MAX_LEVEL = 30
START_LEVEL = 2
VERBOSE = False  # Set to True for verbose output

def clear_paniclog():
    """Clear the paniclog file if it exists"""
    if os.path.exists(PANICLOG):
        try:
            os.remove(PANICLOG)
            print(f"Cleared paniclog at: {PANICLOG}")
            return True
        except Exception as e:
            print(f"Warning: Could not clear paniclog: {e}")
            return False
    return True

def read_paniclog():
    """Read the contents of the paniclog file"""
    if os.path.exists(PANICLOG):
        try:
            with open(PANICLOG, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Warning: Could not read paniclog: {e}")
            return ""
    return ""

def run_nethack_test(level):
    """Run NetHack in test mode for a specific level"""
    try:
        # Clear the paniclog before each test
        clear_paniclog()
        
        # Prepare command
        cmd = [NETHACK_EXECUTABLE, "-t", str(level)]
        
        print(f"Testing level {level} generation...")
        if VERBOSE:
            print(f"Running command: {' '.join(cmd)}")
        
        # Run NetHack in test mode
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30  # Timeout after 30 seconds
        )
        
        # Wait a moment for the paniclog to be written
        time.sleep(0.5)
        
        # Read the paniclog
        paniclog_content = read_paniclog()
        
        if VERBOSE:
            print(f"Paniclog content for level {level}:")
            print(paniclog_content)
        
        # Check for success
        if "Test Successful" in paniclog_content:
            # Count lines in paniclog
            line_count = len(paniclog_content.strip().split('\n'))
            if line_count == 1:
                return None  # Success
            else:
                return f"Found 'Test Successful' but paniclog contains {line_count} lines"
        else:
            return f"No 'Test Successful' message found in paniclog"
            
    except subprocess.TimeoutExpired:
        return f"Timeout while testing level {level}"
    except Exception as e:
        return f"Exception: {str(e)}"

def main():
    global VERBOSE, START_LEVEL, MAX_LEVEL
    
    # Parse command line arguments
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in ['-v', '--verbose']:
            VERBOSE = True
            print("Verbose mode enabled")
        elif sys.argv[i] in ['-s', '--start']:
            if i + 1 < len(sys.argv):
                START_LEVEL = int(sys.argv[i + 1])
                i += 1
            else:
                print("Error: --start requires a level number")
                return 1
        elif sys.argv[i] in ['-e', '--end']:
            if i + 1 < len(sys.argv):
                MAX_LEVEL = int(sys.argv[i + 1])
                i += 1
            else:
                print("Error: --end requires a level number")
                return 1
        elif sys.argv[i] in ['-l', '--level']:
            if i + 1 < len(sys.argv):
                START_LEVEL = MAX_LEVEL = int(sys.argv[i + 1])
                i += 1
            else:
                print("Error: --level requires a level number")
                return 1
        i += 1
    
    print("Starting NetHack level test...")
    print(f"Using NetHack executable: {NETHACK_EXECUTABLE}")
    print(f"Using paniclog: {PANICLOG}")
    print(f"Testing levels {START_LEVEL} to {MAX_LEVEL}")
    
    # Check if the executable exists
    if not os.path.exists(NETHACK_EXECUTABLE):
        print(f"ERROR: NetHack executable not found at {NETHACK_EXECUTABLE}")
        print("Please specify the path to the NetHack executable:")
        print("  1. Edit this script and update the NETHACK_EXECUTABLE variable")
        print("  2. Or place the script in the same directory as the NetHack executable")
        return 1
    
    # Run tests for each level
    errors = []
    for level in range(START_LEVEL, MAX_LEVEL + 1):
        error = run_nethack_test(level)
        if error:
            errors.append((level, error))
    
    # Report results
    if errors:
        print(f"\nTest FAILED with {len(errors)} errors:")
        for level, error in errors:
            print(f"Level {level}: {error}")
        return 1
    else:
        print(f"\nTest PASSED! All levels from {START_LEVEL} to {MAX_LEVEL} generated successfully.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
