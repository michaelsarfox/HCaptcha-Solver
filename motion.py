from python_ghost_cursor import path
import random
import time
import util

def get_screen_properties():
    return {
        "availWidth": 2560,
        "availHeight": 1032,
        "width": 2560,
        "height": 1080,
        "colorDepth": 24,
        "pixelDepth": 24,
        "availLeft": 0,
        "availTop": 0,
        "onchange": None,
        "isExtended": True
    }

def get_navigation_properties():
    return {
        "vendorSub": "",
        "productSub": "20030107",
        "vendor": "Google Inc.",
        "maxTouchPoints": 0,
        "scheduling": {},
        "userActivation": {},
        "doNotTrack": None,
        "geolocation": {},
        "connection": {},
        "pdfViewerEnabled": True,
        "webkitTemporaryStorage": {},
        "hardwareConcurrency": 12,
        "cookieEnabled": True,
        "appCodeName": "Mozilla",
        "appName": "Netscape",
        "appVersion": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "platform": "Win32",
        "product": "Gecko",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "language": "en-US",
        "languages": [
            "en-US",
            "en"
        ],
        "onLine": True,
        "webdriver": False,
        "deprecatedRunAdAuctionEnforcesKAnonymity": True,
        "bluetooth": {},
        "storageBuckets": {},
        "clipboard": {},
        "credentials": {},
        "keyboard": {},
        "managed": {},
        "mediaDevices": {},
        "storage": {},
        "serviceWorker": {},
        "virtualKeyboard": {},
        "wakeLock": {},
        "deviceMemory": 8,
        "userAgentData": {
            "brands": [
            {
                "brand": "Chromium",
                "version": "122"
            },
            {
                "brand": "Not(A:Brand",
                "version": "24"
            },
            {
                "brand": "Google Chrome",
                "version": "122"
            }
            ],
            "mobile": False,
            "platform": "Windows"
        },
        "login": {},
        "ink": {},
        "mediaCapabilities": {},
        "hid": {},
        "locks": {},
        "gpu": {},
        "mediaSession": {},
        "permissions": {},
        "presentation": {},
        "usb": {},
        "xr": {},
        "serial": {},
        "windowControlsOverlay": {},
        "plugins": [
            "internal-pdf-viewer",
            "internal-pdf-viewer",
            "internal-pdf-viewer",
            "internal-pdf-viewer",
            "internal-pdf-viewer"
        ]
    }

def generate_mouse_events(timestamp, start, end):
    events = []
    increment =  16
    for p in path(start, end):
        movement_timestamp = timestamp + increment
        events.append([int(p["x"]), int(p["y"]), movement_timestamp])
        increment += random.randint(16, 101)
    return events, calculate_mean_period(events), timestamp + increment

def generate_key_events(timestamp, answers):
    events, times = [], []
    increment = 2
    for answer in answers.values():
        for char in answer:
            key_timestamp = timestamp + increment
            times.append(key_timestamp)
            events.append([ord(char), key_timestamp])
            increment += random.randint(50, 280)

        key_timestamp = timestamp + increment
        times.append(key_timestamp)
        events.append([13, key_timestamp])
        increment += random.randint(50, 280)
    return events, calculate_mean_period(events), timestamp + increment

def calculate_mean_period(events):
    timestamps = []
    for event in events:
        timestamps.append(event[len(event) - 1])

    differences = []
    for i in range(len(timestamps) - 1):
        differences.append(timestamps[i + 1] - timestamps[i])

    if differences:
        return float("{:.2f}".format(sum(differences) / len(differences), 2))
    return 0

def get_frame_data(event, answers):
    timestamp = int(time.time() * 1000)
    if event == "START":
        movements, mean_period, new_timestamp = generate_mouse_events(timestamp, {'x': 50, 'y': 100}, {'x': 102, 'y': 350})
        return {
            "st": timestamp,
            "dct": timestamp,
            "mm": movements,
            "md-mp": mean_period,
            "md": "",
            "md-mp": "",
            "mu": "",
            "mu-mp": "",
            "v": 1
        }, new_timestamp
    elif event == "REFRESH":
        movements, mean_period, new_timestamp = generate_mouse_events(timestamp, {'x': 65, 'y': 80}, {'x': 30, 'y': 40})
        return {
            "st": timestamp,
            "mm": movements,
            "md-mp": calculate_mean_period(movements),
            "md": "", # WE WILL NEED TO GET WHERE IT CLICKED CORDINATES (maybe? :P)
            "md-mp": "",
            "mu": "",
            "mu-mp": "",
            # REST OF BLAH
        }, new_timestamp
    elif event == "SUBMISSION":
        keys, mean_period, new_timestamp = generate_key_events(timestamp, answers)
        return {
            "st": timestamp,
            "dct": timestamp,
            "kd": keys,
            "kd-mp": mean_period,
            "ku":  keys,
            "ku-mp": mean_period,
            "v": 1
        }, new_timestamp

    # return {
    #    "st": timestamp,
    #    "md": [[28, 24, timestamp + 492]],
    #    "md-mp": 0,
    #    "mu": [[28, 24, timestamp + 492 + 100]],
    #    "mu-mp": 0,
    #    "v": 1
    # }, timestamp + 492 + 100

def get_top_level_data(site_host, previous_timestamp):
    timestamp = previous_timestamp + 1150
    widget = "0" + util.random_string(10)
    movements, _, _ = generate_mouse_events(previous_timestamp + 1, {'x': 200, 'y': 300}, {'x': 100, 'y': 350})
    return {
        "st": timestamp,
        "sc": get_screen_properties(),
        "nv": get_navigation_properties(),
        "dr": "",
        "exec": "false",
        "wn": [[2560, 947, 1, timestamp + 1]],
        "xy": [[0, 0, 1, timestamp + 1]],
        "mm": movements,
        "mm-mp": calculate_mean_period(movements),
        "session": [], # CAPTCHA_KEY
        "widgetList": [widget],
        "href": "https://" + site_host,
        "prev": {
            "escaped": False,
            "passed": False,
            "expiredChallenge": False,
            "expiredResponse": False
        }
    }


# if __name__ == "__main__":
#     movements, new_timestamp = generate_mouse_movements(int(time.time() * 1000), {'x': 200, 'y': 300}, {'x': 100, 'y': 350})
#     print(movements)
#     m = calculate_mean_period(movements)
#     print(m)
#     # data = generate_key_presses(int(time.time() * 1000), {"1": "doggy", "cat": "table"})
#     # print(data)