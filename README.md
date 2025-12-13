
# ISKL-V

Information  
Stealer  
Key  
Logger  
Virus

A virus that is designed to steal as much information as possible before being discovered, and delete the victim's system as soon as it is discovered.

> NOTE: This is for educational and testing purposes only! I am very interested in computer viruses and cybersecurity, so I decided to make this project to see what I can do. This is not to be used on any system which does not belong to you and that you are not willing to have ruined. Please only test on VMs. Once completed, running it once means your data is doomed.



## Features

- Server (server.py) **NOT COMPLETED**
  - Can receive any amount of any type of file (can be in combination!) and organize them by file type and IP that sent them. ✔
  - Can receive ZIP files, unpack them, and organize their contents by MIME file type. ✔
  - Can organize files by their paths on the origin computer.
  - Can organize computers by geographic location & MAC address. ✔
  - Can send computers commands to be executed in their shell.
- Starter (main.py) **NOT COMPLETED**
  - Downloads the scripts if they aren't available locally. ✔
  - Starts the virus scripts. ✔
  - Can support any number of scripts ✔
  - Works on Windows & Linux
  - Makes the virus restart with admin privileges whenever the computer is restarted. ✔
  - Can make requests on Tor/Proxy to avoid any information being intercepted
    - Eg. the victim checking the router to see where the virus is getting its files from
- File stealer (file_stealer.py) **NOT COMPLETED**
  - Searches your entire systems for any file type(s) you want (.txt by default). ✔
  - Sends your found files to a specified URL. ✔
  - Has an option to send a bunch of lone files .in one request or to pack them into a ZIP and send them, all automatically. ✔
  - Can restart searching from where it stopped after computer shutdown.
  - Can steal chrome & firefox passwords & cookies.
- Keylogger (keylogger.py) **COMPLETED**
  - Logs all key presses and what window was focused when the keys were pressed. ✔
  - Sends a log of the keys logged every specified amount of seconds in the background while new key presses are being logged. ✔
  - Deletes the part of the log that was sent after the fact so nothing is sent twice. ✔
  - Example of a log can be found in /examples/keylogger-log. ✔
- Screenshotter (Screenshotter.py) **COMPLETED**
  - takes screenshots of your entire computer including all monitors every X seconds and sends them once Y screenshots have been taken. ✔
  - Deletes all screenshots sent after the fact so nothing is sent twice. ✔
- Destruction mechanism **NOT COMPLETED**
  - Should be a library that all the scripts can use.
  - Some way to completely delete the files and make the partition unusable without admin
    - Probably by deleting the partition and writing a partition over it.
  - Methods to check a variety of ways the victim may be messing with the virus.
    - An attempt to close one of the scripts is made ✔
    - An attempt to view/edit one of the scripts is made ✔
    - The files were edited somehow ✔
    - You wish to do so from the server

## TODO

- Files should be able to verify their integrity and that nothing was changed

- Remote CMD access

- List of all computers infected on server

- Steal browser cookies using the file stealer to potentially access some accounts

- A mechanism that attaches the virus to any .exe file or similar for Linux so it is hidden within the .exe and infects the computer when you launch the .exe

- Think of more things to add.

## Weaknesses in the virus

- Copying of script files
  - If the victim copies one of the files, changes their name and opens them the virus has no way of knowing.
  - Possibly solvable by checking if the directory of the scripts or any other sensitive virus files is open, but this can be bypassed by using cmd or another to copy the files.
- Safe mode
  - If the victim launches their system in safe mode the virus will not activate since safe mode disables task scheduler.
  - Possibly solvable by setting the virus to launch in a registry like winlogon, but this is very commonly used by many viruses/ransomware so maybe another registry is better suited.
