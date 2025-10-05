import re

class App:

    @staticmethod
    def get(user_agent):
        if re.search(r"instagram", user_agent, re.IGNORECASE):
            return 'instagram'
        if re.search(r"facebook", user_agent, re.IGNORECASE):
            return 'facebook'
        elif re.search(r"whatsapp", user_agent, re.IGNORECASE):
            return 'whatsapp'
        elif re.search(r"telegram", user_agent, re.IGNORECASE):
            return 'telegram'
        else:
            return 'web / other'

    @staticmethod
    def gets(logs):
        apps = {}
        for log in logs:
            app = log['app']
            if app in apps:
                apps[app] = apps[app] + 1
            else:
                apps[app] = 1
        return apps