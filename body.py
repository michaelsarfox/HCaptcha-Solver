import urllib.parse
import requests
import motion
import random
import time
import json

def get_hsw(jwt):
    response = requests.get("http://127.0.0.1:5000/get_hsw/?jwt=" + jwt)
    if response.status_code != 200:
        print("[ERROR]: Failed to generate hsw")
        exit(0)
    return response.json()["data"]

def generate_motion_data(site_host, event, answers = None):
    frame_data, timestamp = motion.get_frame_data(event, answers)
    return {
        **frame_data,
        "topLevel": motion.get_top_level_data(site_host, timestamp)
    }

def generate_pdc():
    return {"s": time.time_ns() * 1000, "n": 0, "p": 1, "gcs": random.randint(40, 110)}

def create_challenge_body(captcha, config, rq_data):
    body = {
        "v": captcha.version,
        "sitekey": captcha.site_key,
        "host": captcha.site_host,
        "hl": "en",
        "motionData": json.dumps(generate_motion_data(captcha.site_host, "START")),
        "pdc": generate_pdc(),
        "n": get_hsw(config["req"]),
        "c": json.dumps(config)
    }
    if rq_data:
        body["rqdata"] = rq_data
    return urllib.parse.urlencode(body)

def create_refresh_body(captcha, config, challenge, rq_data):
    body = {
        "v": captcha.version,
        "sitekey": captcha.site_key,
        "host": captcha.site_host,
        "hl": "en",
        "a11y_tfe": True,
        "action": "challenge-refresh",
        "extraData": json.dumps(challenge),
        "motionData": json.dumps(generate_motion_data(captcha.site_host)),
        "pdc": generate_pdc(),
        "old_ekey": challenge["key"],
        "n": get_hsw(config["req"]),
        "c": json.dumps(config)
    }
    if rq_data:
        body["rqdata"] = rq_data
    return urllib.parse.urlencode(body)

def create_submission_body(captcha, config, answers):
    return {
        "answers": answers,
        "job_mode": "text_free_entry",
        "motionData": json.dumps(generate_motion_data(captcha.site_host)),
        "n": get_hsw(config["req"]),
        "serverdomain": captcha.site_host,
        "sitekey": captcha.site_key,
        "v": captcha.version,
        "c": json.dumps(config)
    }

if __name__ == "__main__":
    data  = generate_motion_data("discord.com", "START")
    print(data)