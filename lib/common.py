import sys
import re
from datetime import datetime
from zoneinfo import ZoneInfo

class Common:

    @staticmethod
    def getArguments():
        result    = {}
        arguments = sys.argv[1:]
        for argument in arguments:
            m = re.search(r"\-\-([^=]+)=([^$]+)$", argument)
            if m:
                result[m.group(1)] = m.group(2)
        return result

    @staticmethod
    def getTimestamp(item):
        return int(re.sub(r"\.[0-9]+$", '', str(item)))

    @staticmethod
    def getTimestampFromDateString(i):
        dt = datetime.strptime(i, "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo("Europe/Madrid"))
        i  = int(dt.timestamp())
        return i
