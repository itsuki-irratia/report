import json
import re
from collections import OrderedDict


class Hack:

    EXCLUDED_PATTERNS = [
        r"\.opus",
        r"\.aac",
        r"\.mp3",
        r"\.ogg",
        r"listeners\-online\.json",
        r"robots.txt",
        r"\"uri\":\"/\"",
        r"\.png",
        r"itsuki\-stats\.json",
        r"\.ico",
        r"\/custom\/",
        r"fbclid=",
        r"\/zuzenean"
    ]

    @staticmethod
    def shouldSkipLine(line):
        for pattern in Hack.EXCLUDED_PATTERNS:
            if re.search(pattern, line):
                return True

        return False

    @staticmethod
    def getUserAgent(request):
        headers = request.get('headers', {})
        user_agent = headers.get('User-Agent', '-')

        if isinstance(user_agent, list):
            return user_agent[0] if len(user_agent) > 0 else '-'

        return user_agent or '-'

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
                    user_agent = Hack.getUserAgent(request)
                    if remote_ip not in grouped:
                        grouped[remote_ip] = {
                            'uris': [],
                            'requests': [],
                        }

                    grouped[remote_ip]['uris'].append(uri)
                    grouped[remote_ip]['requests'].append({
                        'uri': uri,
                        'user_agent': user_agent,
                    })
                except json.JSONDecodeError as error:
                    raise ValueError(f"invalid json on line {line_number}") from error

        result = []
        for remote_ip, data in grouped.items():
            result.append({
                "IP": remote_ip,
                "uris": data['uris'],
                "requests": data['requests'],
            })

        return result
