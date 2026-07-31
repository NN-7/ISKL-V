
# ISKL-V

Information  
Stealer  
Key  
Logger  
Virus

A virus that is designed to steal as much information as possible before being discovered, and delete the victim's system as soon as it is discovered.

> NOTE: This is for educational and testing purposes only! I am very interested in computer viruses and cybersecurity, so I decided to make this project to see what I can do. This is not to be used on any system which does not belong to you and that you are not willing to have ruined. Please only test on VMs. Once completed, running it once means your data is doomed. By studying/inspecting my program, you agree that you are solely responsible for any damage you caused by being irresponsible. Do not use for wrongdoing. I am not responsible for wrongdoing of others.

This project is licensed under the MIT License. See the LICENSE file for the full text of the license.

## Features

- Version for Windows **IN PROGRESS**
- Version for Linux **AFTER WINDOWS VERSION FINISHED**

- Server (server.py) **NOT COMPLETED**
  - Can receive any amount of any type of file (can be in combination!) and organize them by file type and IP that sent them. ✔
  - Can receive ZIP files, unpack them, and organize their contents by MIME file type. ✔
  - Can organize files by their paths on the origin computer. TODO
  - Can organize computers by MAC address. ✔
  - Can organize computers by geographic location. ✔
- Command Reciever (command_reciever.py) **COMPLETED**
  - Can send computers commands to be executed in their shell. ✔
  - Can execute destruction remotely. ✔
  - Can make sure the computer is still infected. ✔
  - Client for sending commands ✔
- Starter (main.py) **NOT COMPLETED**
  - Downloads the scripts if they aren't available locally. ✔
  - Starts the virus scripts. ✔
  - Can support any number of scripts. ✔
  - Works on Windows. ✔
  - Makes the virus restart with admin privileges whenever the computer is restarted. ✔
  - Can make requests on Tor to avoid any information being intercepted. ✔
    - E.g. the victim checking the router/using network monitoring software to see where the virus is getting/sending files from/to.
- File stealer (file_stealer.py) **NOT COMPLETED**
  - Searches your entire systems for any file type(s) you want (.txt by default). ✔
  - Sends your found files to a specified URL. ✔
  - Has an option to send a bunch of lone files in one request or to pack them into a ZIP and send them, all automatically. ✔
  - Can restart searching from where it stopped after computer shutdown. TODO
  - Can steal chrome & firefox passwords & cookies. ✔
- Keylogger (keylogger.py) **COMPLETED**
  - Logs all key presses and what window was focused when the keys were pressed. ✔
  - Sends a log of the keys logged every specified amount of seconds in the background while new key presses are being logged. ✔
  - Deletes the part of the log that was sent after the fact so nothing is sent twice. ✔
  - Example of a log can be found in /examples/keylogger-log. ✔
- Screenshotter (Screenshotter.py) **COMPLETED**
  - takes screenshots of your entire computer including all monitors every X seconds and sends them once Y screenshots have been taken. ✔
  - Deletes all screenshots sent after the fact so nothing is sent twice. ✔
- Destruction mechanism (Destroyer.py) **NOT COMPLETED**
  - A library that all the scripts can use. ✔
  - Completely delete all files and partitions **IN PROGRESS**
  - Modifies windows registries to make your computer boot only to recovery environment TODO
  - Modifies windows recovery environment to delete and overwrite your drives, making your files unusable. Boots to recovery when it is discovered. ✔
  - Display a windows loading screen while wiping files in windows RE to make victim think windows is being loaded. ✔
  - Methods to check a variety of ways the victim may be messing with the virus. ✔
    - An attempt to close one of the scripts is made ✔
    - An attempt to view/edit one of the scripts is made ✔
    - The files were edited somehow ✔
  - Ability for attacker to trigger whenever ✔
- EXE Bundler (bundler.py) **NOT COMPLETED**
  - Makes all virus scripts bear the system process logo in order to camouflage better ✔
  - Bundles additional data into script EXEs ✔
  - Dynamically allows user to add any other files they want to their script ✔
  - Combine starter.py EXE with the target program TODO
    - Meant to attach itself to a software the victim downloads, and starts itself along with the wanted software so nothing looks wierd. The virus is hidden within the wanted .exe and infects the computer when you launch what you actually wanted.

## OTHER TODO

- Files should be able to verify their integrity and that nothing was changed.

- List of all computers infected on server.

- Think of more things to add.

## Weaknesses in the virus

- Copying of script files
  - If the victim copies one of the files, changes their name during the copy and opens them the virus has no way of knowing. (E.g. 'copy c:/file.txt c:/folder/abcd.txt')
  - Possibly solvable by checking if the directory of the scripts or any other sensitive virus files is open, but this can be bypassed by using cmd or another to copy the files.
- Safe mode
  - If the victim launches their system in safe mode the virus will not activate since safe mode disables task scheduler.
  - Possibly solvable by setting the virus to launch in a registry like winlogon, but this is very commonly used by many viruses/ransomware so maybe another registry is better suited.
- Disconnecting computer from power when booting to RE.
- While dism is working, it is visible in Task Manager and could take up a chunk of resources.

## Libraries/Programs used in this project
- Programs
  - PyInstaller
  - Tor
- Libraries
  - os
  - sys
  - ctypes
  - requests
  - subprocess
  - zipfile
  - getmac
  - platform
  - time
  - uvicorn
  - mimetypes
  - fastapi
  - contextlib
  - typing
  - datetime
  - threading
  - secrets
  - keyboard
  - pyautogui
  - mss
  - tempfile
  - shutil
  - socket