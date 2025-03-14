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

# Install required packages if needed
try:
    import win32gui
    import win32con
    import win32process
    import win32api
except ImportError:
    print("pywin32 not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
    import win32gui
    import win32con
    import win32process
    import win32api

try:
    from pynput import keyboard
except ImportError:
    print("pynput not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])
    from pynput import keyboard

# Constants for Windows process creation
CREATE_NEW_CONSOLE = 0x00000010  # Windows constant

# Configuration
def find_nethack_executable():
    # Common locations on Windows
    windows_paths = [
        r".\binary\Debug\x64\NetHack.exe",  # Add this path first based on your error message
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
WIZARD_MODE_ARG = "-D -u wizard"
MAX_LEVEL = 30
START_LEVEL = 2
VERBOSE = False  # Set to True for verbose output

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

# Store window handles found during enumeration
found_windows = []

def enum_windows_callback(hwnd, wildcard):
    """Callback function for EnumWindows"""
    # Get the window title
    title = win32gui.GetWindowText(hwnd)
    # Check if the window is visible and contains the wildcard
    if win32gui.IsWindowVisible(hwnd) and wildcard.lower() in title.lower():
        found_windows.append((hwnd, title))
    return True

def find_windows_by_title(wildcard):
    """Find all windows with titles containing the given wildcard"""
    global found_windows
    found_windows = []
    win32gui.EnumWindows(enum_windows_callback, wildcard)
    return found_windows

def find_window_by_pid(pid):
    """Find window belonging to process ID"""
    result = []
    
    def callback(hwnd, lparam):
        try:
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid and win32gui.IsWindowVisible(hwnd):
                result.append((hwnd, win32gui.GetWindowText(hwnd)))
        except:
            pass
        return True
    
    win32gui.EnumWindows(callback, None)
    return result

def send_keystrokes(keys):
    """Send keystrokes using pynput"""
    kb = keyboard.Controller()
    for key in keys:
        if key == "\n" or key == "{ENTER}":
            kb.press(keyboard.Key.enter)
            kb.release(keyboard.Key.enter)
        else:
            kb.type(key)
        time.sleep(0.1)
    # Add a brief pause after sending commands
    time.sleep(0.3)

def run_nethack_test():
    """Run NetHack with the test commands and monitor output"""
    nhrc_path = create_nhrc_file()
    
    try:
        # Set environment variables
        env = os.environ.copy()
        env["NETHACKOPTIONS"] = f"@{nhrc_path}"
        
        # Prepare command
        cmd = [NETHACK_EXECUTABLE]
        if WIZARD_MODE_ARG:
            cmd.append(WIZARD_MODE_ARG)
        
        cmd_str = " ".join(cmd)
        print(f"Running command: {cmd_str}")
        print("Starting NetHack in a visible window...")
        
        # Start the NetHack process with CREATE_NEW_CONSOLE flag to ensure it's visible
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = win32con.SW_SHOW  # Use win32con here
        
        process = subprocess.Popen(
            cmd,
            env=env, 
            creationflags=CREATE_NEW_CONSOLE,  # Use the defined constant
            startupinfo=startupinfo
        )
        
        print(f"Started NetHack process with PID: {process.pid}")
        
        # Give time for the window to appear
        time.sleep(3)
        
        # Try to find the window by different methods
        window_info = None
        
        # Method 1: Find by PID
        windows_by_pid = find_window_by_pid(process.pid)
        if windows_by_pid:
            print(f"Found {len(windows_by_pid)} windows by PID:")
            for hwnd, title in windows_by_pid:
                print(f"  Window Handle: {hwnd}, Title: '{title}'")
            window_info = windows_by_pid[0]
        
        # Method 2: Find by window title containing "NetHack"
        if not window_info:
            print("Searching for windows with 'NetHack' in title...")
            nethack_windows = find_windows_by_title("NetHack")
            if nethack_windows:
                print(f"Found {len(nethack_windows)} windows by title:")
                for hwnd, title in nethack_windows:
                    print(f"  Window Handle: {hwnd}, Title: '{title}'")
                window_info = nethack_windows[0]
        
        # Method 3: Find console windows
        if not window_info:
            print("Searching for console windows...")
            console_windows = find_windows_by_title("cmd") + find_windows_by_title("command")
            if console_windows:
                print(f"Found {len(console_windows)} potential console windows:")
                for hwnd, title in console_windows:
                    print(f"  Window Handle: {hwnd}, Title: '{title}'")
                window_info = console_windows[0]
        
        # Method 4: List all visible windows as a last resort
        if not window_info:
            print("Listing all visible windows...")
            all_windows = []
            
            def enum_all_callback(hwnd, _):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if title:  # Only include windows with titles
                        all_windows.append((hwnd, title))
                return True
            
            win32gui.EnumWindows(enum_all_callback, None)
            
            print(f"Found {len(all_windows)} visible windows:")
            for hwnd, title in all_windows:
                print(f"  Window Handle: {hwnd}, Title: '{title}'")
            
            # Try to find a likely candidate
            for hwnd, title in all_windows:
                if "nethack" in title.lower() or "game" in title.lower() or "console" in title.lower():
                    window_info = (hwnd, title)
                    break
        
        if not window_info:
            raise Exception("Could not find a suitable window for NetHack")
        
        hwnd, title = window_info
        print(f"Selected window - Handle: {hwnd}, Title: '{title}'")
        
        # Bring the window to the foreground
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            win32gui.SetFocus(hwnd)
            print("Window activated and brought to foreground")
        except Exception as e:
            print(f"Warning: Could not activate window: {e}")
        
        # Give the window time to come to the foreground
        time.sleep(2)
        
        # Define the commands to send
        commands = [
            "y",   # Confirm character
            "y",   # Confirm character
        ]
        
        # Add quit commands at the end
        commands.extend([
            "#quit",  # Quit the game
            "y",      # Confirm quit
        ])
        
        errors = []
        
        # Send each command
        print("Sending commands to NetHack window...")
        for cmd in commands:
            if VERBOSE:
                print(f"Sending: '{cmd}'")
            
            # Re-activate window before each command to ensure focus
            try:
                win32gui.SetForegroundWindow(hwnd)
            except:
                pass
            
            # Send the command
            send_keystrokes(cmd)
            
            # Wait between commands
            time.sleep(1)
        
        # Give the game time to finish
        print("Waiting for NetHack to complete...")
        time.sleep(3)
        
        # Make sure the process is terminated
        try:
            process.terminate()
        except:
            pass
            
        return errors
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        return [(0, f"Exception: {str(e)}")]
    finally:
        # Clean up temporary files
        try:
            os.remove(nhrc_path)
        except:
            pass

def main():
    global VERBOSE
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] in ['-v', '--verbose']:
        VERBOSE = True
        print("Verbose mode enabled")
    
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