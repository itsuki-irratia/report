import sys
import json
import re
from datetime import datetime

from .common import Common
from .device import Device
from .app import App
from .geo import Geo

class Log:
    
    @staticmethod
    def getLines(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()

        log_lines = re.split(r"\n", content)
        log_lines = [item for item in log_lines if item != '']
        return log_lines

    @staticmethod
    def prepareLog(log, output_mode):
        log_json  = json.loads(log)

        request   = log_json['request']
        remote_ip = request['remote_ip']
        ts        = Common.getTimestamp(log_json['ts'])
        dt        = datetime.fromtimestamp(ts)
        uri       = request['uri']
        headers   = request['headers']

        try:
            user_agent = headers['User-Agent'][0]
        except Exception as e:
            user_agent = '-'

        result = {
            "dt":         str(dt),
            "uri":        uri,
            "remote_ip":  remote_ip,
            "user_agent": user_agent
        }

        if output_mode != 'basic':
            result['device'] = Device.get(user_agent)
            result['app']    = App.get(user_agent)
            result['geo']    = Geo.get(remote_ip)

        return result

    @staticmethod
    def getByDates(logs, since, until, output_mode):
        result = []
        for _log in logs:
            log_json  = json.loads(_log)
            request   = log_json['request']
            remote_ip = request['remote_ip']
            uri       = request['uri']

            if Log.isUriAllowed == False:
                continue

            if log_json['status'] != 200:
                continue

            if re.search(r"^192\.168\.", remote_ip):
                continue

            ts = Common.getTimestamp(log_json['ts'])

            if ts>=since and ts<=until:
                _log = Log.prepareLog(_log, output_mode)
                result.append(_log)

        return result

    @staticmethod
    def isUriAllowed(uri):
        allowed = ['/itsuki.ogg', '/itsuki.mp3', '/itsuki.opus', '/itsuki.aac']
        if uri in allowed:
            return True
        return False