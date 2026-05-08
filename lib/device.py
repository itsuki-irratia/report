import re
import json
import os

OTHERS_FILE = 'lib/device.others.json'

class Device:

    @staticmethod
    def get(user_agent, log):
        if re.search(r"iphone|iOS|ipad",  user_agent, re.IGNORECASE):
            return 'ios'
        elif re.search(r"android",        user_agent, re.IGNORECASE):
            return 'Android'
        elif re.search(r"bot",            user_agent, re.IGNORECASE):
            return 'bot'
        elif re.search(r"firefox",        user_agent, re.IGNORECASE):
            return 'Firefox'
        elif re.search(r"chrome",         user_agent, re.IGNORECASE):
            return 'Chrome'
        elif re.search(r"safari",         user_agent, re.IGNORECASE) or \
             re.search(r"macintosh",      user_agent, re.IGNORECASE):
            return 'Safari'
        elif re.search(r"WhatsApp",       user_agent, re.IGNORECASE):
            return 'WhatsApp'
        elif re.search(r"facebook",       user_agent, re.IGNORECASE):
            return 'Facebook'
        elif re.search(r"RadioGarden",    user_agent, re.IGNORECASE):
            return 'RadioGarden'
        elif re.search(r"Go-http-client", user_agent, re.IGNORECASE):
            return 'Go-http-client'
        elif re.search(r"Lavf",           user_agent, re.IGNORECASE):
            return 'lavf'
        else:
            others = json.load(open(OTHERS_FILE)) if os.path.exists(OTHERS_FILE) else []
            if user_agent not in others:
                others.append(user_agent)
                json.dump(others, open(OTHERS_FILE, 'w'), indent=2)
            return 'web / other'

    @staticmethod
    def gets(logs):
        devices = {}
        for log in logs:
            device = log['device']
            if device in devices:
                devices[device] = devices[device] + 1
            else:
                devices[device] = 1
        return devices

    @staticmethod
    def getDurations(logs):
        durations = {}
        for log in logs:
            device = log['device']
            durations[device] = durations.get(device, 0) + log.get('duration', 0)
        return durations