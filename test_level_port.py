#!/usr/bin/env python3
"""
NetHack Level Port Test Script

This script runs NetHack in wizard mode, creates a test character,
and uses #wizlevelport to check every level from 2 to 30.
It monitors for error messages and returns an error code if any are found.
"""

import os
import sys
import subprocess
import tempfile
import re
import time
from pathlib import Path

# Configuration
# Try to find NetHack executable in common locations
def find_nethack_executable():
    # Common locations on Windows
    windows_paths = [
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

NETHACK_EXECUTABLE = find_nethack_executable()
WIZARD_MODE_ARG = "-D"
MAX_LEVEL = 30
START_LEVEL = 2

# Error patterns to look for
ERROR_PATTERNS = [
    r"error",
    r"panic",
    r"Segmentation fault",
    r"Bus error",
    r"core dumped",
    r"illegal",
    r"invalid",
    r"failed",
    r"cannot",
    r"impossible"
]

def create_nhrc_file():
    """Create a temporary .nethackrc file for testing"""
    nhrc_content = """
OPTIONS=name:Wizard
OPTIONS=role:wizard
OPTIONS=race:human
OPTIONS=gender:male
OPTIONS=align:neutral
OPTIONS=autopickup
OPTIONS=!legacy
OPTIONS=suppress_alert:3.7.0
OPTIONS=windowtype:tty
OPTIONS=menu_headings:inverse
"""
    fd, nhrc_path = tempfile.mkstemp(prefix="nethack_test_", suffix=".nethackrc")
    with os.fdopen(fd, 'w') as f:
        f.write(nhrc_content)
    return nhrc_path

def create_command_script():
    """Create a script with commands to execute in NetHack"""
    commands = [
        "\n",  # Skip intro screen
        "y\n",  # Confirm character
        "#wizwish\n",  # Enter wish
        "blessed greased +2 speed boots\n",  # Wish for speed boots for faster movement
        "#wizwish\n",  # Enter another wish
        "blessed wand of teleportation\n",  # For emergency escape
    ]
    
    # Add level port commands for each level
    for level in range(START_LEVEL, MAX_LEVEL + 1):
        commands.append(f"#wizlevelport\n")
        commands.append(f"{level}\n")
        # Move around a bit to explore the level
        commands.append("k50\n")  # Move up 50 times
        commands.append("h50\n")  # Move left 50 times
        commands.append("j50\n")  # Move down 50 times
        commands.append("l50\n")  # Move right 50 times
        
    # Add quit command
    commands.append("#quit\n")
    commands.append("y\n")  # Confirm quit
    
    fd, cmd_path = tempfile.mkstemp(prefix="nethack_commands_", suffix=".txt")
    with os.fdopen(fd, 'w') as f:
        f.writelines(commands)
    return cmd_path

def run_nethack_test():
    """Run NetHack with the test commands and monitor output"""
    nhrc_path = create_nhrc_file()
    cmd_path = create_command_script()
    
    try:
        # Set environment variables
        env = os.environ.copy()
        env["NETHACKOPTIONS"] = f"@{nhrc_path}"
        
        # Prepare command
        cmd = [NETHACK_EXECUTABLE]
        if WIZARD_MODE_ARG:
            cmd.append(WIZARD_MODE_ARG)
            
        print(f"Running command: {' '.join(cmd)}")
        
        # Run NetHack with commands piped to stdin
        with open(cmd_path, 'r') as cmd_file:
            process = subprocess.Popen(
                cmd,
                stdin=cmd_file,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True,
                bufsize=1
            )
            
            # Process output in real-time
            errors = []
            current_level = START_LEVEL
            
            # Read output line by line
            for line in process.stdout:
                # Check for level change indicators
                level_match = re.search(r"Dlvl:(\d+)", line)
                if level_match:
                    current_level = int(level_match.group(1))
                
                # Check for error patterns
                for pattern in ERROR_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        errors.append((current_level, line.strip()))
                        print(f"ERROR on level {current_level}: {line.strip()}")
            
            # Wait for process to complete
            process.wait()
            
            # Check stderr for any errors
            stderr_output = process.stderr.read()
            if stderr_output:
                for line in stderr_output.splitlines():
                    for pattern in ERROR_PATTERNS:
                        if re.search(pattern, line, re.IGNORECASE):
                            errors.append((current_level, line.strip()))
                            print(f"STDERR ERROR: {line.strip()}")
            
            return errors
    
    finally:
        # Clean up temporary files
        try:
            os.remove(nhrc_path)
            os.remove(cmd_path)
        except:
            pass

def main():
    print("Starting NetHack level port test...")
    print(f"Using NetHack executable: {NETHACK_EXECUTABLE}")
    
    # Check if the executable exists
    if not os.path.exists(NETHACK_EXECUTABLE):
        print(f"ERROR: NetHack executable not found at {NETHACK_EXECUTABLE}")
        print("Please specify the path to the NetHack executable:")
        print("  1. Edit this script and update the NETHACK_EXECUTABLE variable")
        print("  2. Or place the script in the same directory as the NetHack executable")
        return 1
    
    try:
        errors = run_nethack_test()
        
        if errors:
            print(f"\nTest FAILED with {len(errors)} errors:")
            for level, error in errors:
                print(f"Level {level}: {error}")
            return 1
        else:
            print("\nTest PASSED! All levels checked successfully.")
            return 0
    except FileNotFoundError as e:
        print(f"ERROR: Failed to run NetHack: {e}")
        print("Please ensure NetHack is installed and the path is correct.")
        return 1
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
