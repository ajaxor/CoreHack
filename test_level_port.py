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
NETHACK_EXECUTABLE = "nethack"  # Update this path if needed
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
OPTIONS=suppress_alert:3.6.0
OPTIONS=windowtype:tty
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
    ]
    
    # Add level port commands for each level
    for level in range(START_LEVEL, MAX_LEVEL + 1):
        commands.append(f"#wizlevelport\n")
        commands.append(f"{level}\n")
        commands.append("100\n")  # Look around a bit
        
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
        
        # Run NetHack with commands piped to stdin
        with open(cmd_path, 'r') as cmd_file:
            process = subprocess.Popen(
                [NETHACK_EXECUTABLE, WIZARD_MODE_ARG],
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
    errors = run_nethack_test()
    
    if errors:
        print(f"\nTest FAILED with {len(errors)} errors:")
        for level, error in errors:
            print(f"Level {level}: {error}")
        return 1
    else:
        print("\nTest PASSED! All levels checked successfully.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
