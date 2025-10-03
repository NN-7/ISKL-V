import requests # to send screenshots
import threading # to make screenshot sending repeat in background
import mss # to screenshot
import mss.tools
import os
from contextlib import ExitStack # to close screenshots properly
from datetime import datetime, timezone # to classify screenshots by time sent

URL = 'http://127.0.0.1:8000'
SCREENSHOT_INTERVAL = 15.0 # Interval between taking screenshots (in seconds).
SEND_COUNT = 2 # How many screenshots need to be taken before sending.
screenshots = []
# Make sure the screenshot&send count combo don't make the sending interval
# (screenshot interval * send count) too low so you don't DDOS yourself

def screenshot():
    with mss.mss() as sct:
        time = str(datetime.now(timezone.utc))[:-13].replace(':','.') # get the current utc time, remove milliseconds portion, and switch colons to periods since you cant use colons in file names
        ss = sct.grab(sct.monitors[0])
        screenshot_name = f"screenshot-{time}.png"
        mss.tools.to_png(ss.rgb, ss.size, output=screenshot_name)
        screenshots.append(screenshot_name)
    if len(screenshots) >= SEND_COUNT:
        send_screenshot()
    threading.Timer(SCREENSHOT_INTERVAL, screenshot).start() # make the function run again after the amount of seconds specified in SCREENSHOT_INTERVAL
    
def send_screenshot():
    count = len(screenshots) # Assume new screenshots were added which you haven't sent yet and log how many you're sending so you know how many to remove later
    ss_payload = {} # progressively add more screenshots to the payload
    i = 1
    with ExitStack() as stack:
        for ss in screenshots[:count-1]:
            img = stack.enter_context(open(ss, 'rb')) # open the screenshot in read-only mode binary
            ss_payload["files"] = (ss, img, 'image/png') # make the payload for the screenshot containing its name, the screenshot in binary, and its MIME type and add it to the list of the payload
            i += 1 # add 1 to the counter so the screenshot keys enumerate ex. {'file1:(..),file2:(..), and so on'}
        r = requests.post(URL, files=ss_payload) # POST (send) the screenshot
    if not 300 > r.status_code >= 200:
        pass
    else:
        stack.close()
        for file in screenshots[:count]:
            os.remove(file)
        del screenshots[:count]

screenshot()