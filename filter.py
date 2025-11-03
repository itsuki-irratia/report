import sys
import re
import json
from lib.common import Common

arguments = Common.getArguments()
since     = Common.getTimestampFromDateString(arguments['since'])
until     = Common.getTimestampFromDateString(arguments['until'])

log_file  = arguments['log-file']
with open(log_file, 'r', encoding='utf-8') as f:
    content = f.read()

lines = re.split(r"\n", content)
log_lines = [item for item in lines if item.strip() != '']

result = []
for line in log_lines:
    ts = Common.getTimestamp(json.loads(line)['ts'])
    if ts >= since and ts <= until:
        result.append(line)

data_sorted = sorted(result, key=lambda x: json.loads(x)['ts'])

for line in data_sorted:
    print(line)