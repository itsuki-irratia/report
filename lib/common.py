import sys
import re
from datetime import datetime

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
    def getDateStringTimestamp(date):
        dt    = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        t     = int(dt.timestamp())
        return t

    @staticmethod
    def getTimestampDateString(i):
        s = datetime.fromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S')
        return s
