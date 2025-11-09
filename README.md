
# ISKL-V

Information  
Stealer  
Key  
Logger  
Virus

A virus that is designed to steal as much information as possible before being discovered, and delete the victim's system as soon as it is discovered.

> NOTE: This is for educational and testing purposes only! I am very interested in computer viruses and cybersecurity so I decided to make this project to see what I can do. This is not to be used on any system which does not belong to you and that you are not willing to have ruined. Please only test on VMs. Once completed, after you run it once your data is doomed.



## Features

- Server (server.py) **NOT COMPLETED**
  - Can receive any amount of any type of file (can be in combination!) and organize them by file type and IP that sent them. ✔
  - Can recieve ZIP files, unpack them, and organize their contents by MIME file type. ✔
  - Can organize files by their paths on the origin computer.
  - Can organize computers by geographic location & MAC address.
  - Can send computers commands to be executed in their shell.
- Starter (main.py) **COMPLETED**
  - Downloads the scripts if they aren't available locally. ✔
  - Starts the virus scripts. ✔
  - Makes the virus restart with admin privileges whenever the computer is restarted. ✔
- File stealer (file_stealer.py) **NOT COMPLETED**
  - Searches your entire systems for any file type(s) you want (.txt by default). ✔
  - Sends your found files to a specified URL. ✔
  - Has an option to send a bunch of lone files .in one request or to pack them into a ZIP and send them, all automatically. ✔
  - Can steal chrome & firefox passwords & cookies.
- Keylogger (keylogger.py) **COMPLETED**
  - Logs all key presses and what window was focused when the keys were pressed. ✔
  - Sends a log of the keys logged every specified amount of seconds in the background while new key presses are being logged. ✔
  - Deletes the part of the log that was sent after the fact so nothing is sent twice. ✔
  - Example of a log can be found in /examples/keylogger-log. ✔
- Screenshotter (Screenshotter.py) **COMPLETED**
  - takes screenshots of your entire computer including all monitors every X seconds and sends them once Y screenshots have been taken. ✔
  - Deletes all screenshots sent after the fact so nothing is sent twice. ✔


## TODO

- Destruction mechanism
  - Some way to completely delete the files and make the partition unusable without admin
  - Should trigger when:
    - An attempt to close one of the scripts is made
    - An attempt to view/edit one of the scripts is made
    - The files were edited somehow
    - You wish to do so from the server

- Files should be able to verify their integrity and that nothing was changed

- Remote CMD access

- List of all computers infected on server

- When I attempted to access google passwords from the script, access was denied. Need to find a way to grab that file.

- Steal browser cookies using the file stealer to potentially access some accounts

- A mechanism that attaches the virus to any .exe file or similar for Linux and MacOS so it is hidden within the .exe and infects the computer when you launch the .exe

- Think of more things to add.