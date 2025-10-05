import re

class Visit:

    @staticmethod
    def get(logs):
        count = 0
        for log in logs:
            if re.search(r"^\/itsuki\.(ogg|mp3|opus|aac)", log['uri']):
                count = count + 1

        return count

    @staticmethod
    def getUnique(logs):
        count = 0
        ips   = {}
        for log in logs:
            if log['remote_ip'] in ips:
                ips[log['remote_ip']] = ips[log['remote_ip']] + 1
            else:
                ips[log['remote_ip']] = 1
                count = count + 1
        return count

    @staticmethod
    def getOgg(logs):
        count = 0
        for log in logs:
            if re.search(r"^\/itsuki\.(ogg|opus)", log['uri']):
                count = count + 1
        return count

    @staticmethod
    def getMp3(logs):
        count = 0
        for log in logs:
            if re.search(r"^\/itsuki\.(mp3|aac)", log['uri']):
                count = count + 1
        return count