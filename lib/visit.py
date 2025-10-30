import re

class Visit:

    @staticmethod
    def getConnections(logs):
        count = 0
        for log in logs:
            if re.search(r"^\/itsuki\.(ogg|mp3|opus|aac)", log['uri']):
                count = count + 1

        return count

    @staticmethod
    def getUniques(logs):
        result = []
        ips    = {}
        for log in logs:
            if log['remote_ip'] in ips:
                continue
            else:
                result.append(log)
        return result

    @staticmethod
    def countUnique(logs):
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

    def getDuration(logs):
        duration = 0
        for log in logs:
            duration = duration + log['duration']
        return duration

    def duration2Human(seconds):

        hours    = seconds // 3600
        seconds %= 3600
        minutes  = seconds // 60
        seconds %= 60

        result = {
            "hours":   hours,
            "minutes": minutes,
            "seconds": seconds
        }

        return result
