import json
import re
from collections import OrderedDict


class Hack:

    EXCLUDED_PATTERNS = [
        r".opus",
        r".aac",
        r"listeners-online.json",
        r"robots.txt",
        r"\"uri\":\"/\"",
        r"itsuki.ogg",
        r".png",
        r"itsuki-stats.json",
        r".ico",
    ]

    @staticmethod
    def shouldSkipLine(line):
        for pattern in Hack.EXCLUDED_PATTERNS:
            if re.search(pattern, line):
                return True

        return False

    @staticmethod
    def getGroupedUrisByIp(log_file):
        grouped = OrderedDict()

        with open(log_file, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if line == '':
                    continue

                if Hack.shouldSkipLine(line):
                    continue

                try:
                    data = json.loads(line)
                    request = data.get('request', {})
                    uri = request.get('uri', '-')
                    remote_ip = request.get('remote_ip', '-')
                    if remote_ip not in grouped:
                        grouped[remote_ip] = []

                    grouped[remote_ip].append(uri)
                except json.JSONDecodeError as error:
                    raise ValueError(f"invalid json on line {line_number}") from error

        result = []
        for remote_ip, uris in grouped.items():
            result.append({
                "IP": remote_ip,
                "uris": uris,
            })

        return result
