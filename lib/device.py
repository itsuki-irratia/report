import re

class Device:

    @staticmethod
    def get(user_agent):
        if re.search(r"iphone|iOS|ipad", user_agent, re.IGNORECASE):
            return 'ios'
        elif re.search(r"android", user_agent, re.IGNORECASE):
            return 'android'
        elif re.search(r"bot", user_agent, re.IGNORECASE):
            return 'bot'
        elif re.search(r"firefox", user_agent, re.IGNORECASE):
            return 'firefox'
        elif re.search(r"chrome", user_agent, re.IGNORECASE):
            return 'chrome'
        elif re.search(r"safari", user_agent, re.IGNORECASE) and re.search(r"macintosh", user_agent, re.IGNORECASE):
            return 'safari'
        else:
            return 'web / other'
    """
        elif re.search(r"facebook", user_agent, re.IGNORECASE):
            return "web"
        elif re.search(r"whatsapp", user_agent, re.IGNORECASE):
            return "web"
    """

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