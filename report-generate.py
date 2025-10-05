#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from datetime   import datetime
from lib.common import Common

python_bin    = "/usr/bin/python3"
script_folder = os.path.dirname(os.path.abspath(__file__))
command       = f"{python_bin} \"{script_folder}/report.py\""

arguments     = Common.getArguments()
log_file      = arguments['log-file']
since         = arguments['since']
until         = arguments['until']
since_ts      = Common.getDateStringTimestamp(arguments['since'])
until_ts      = Common.getDateStringTimestamp(arguments['until'])

interval = 3600
for i in range(since_ts, until_ts, interval):
    _since = Common.getTimestampDateString(i)
    _until = Common.getTimestampDateString(i+interval-1)

    command = f"{command} --log-file=\"{log_file}\" --since=\"{_since}\" --until=\"{_until}\" --output-mode=\"basic\""
    output  = os.popen(command).read().strip()
    print(command)
    print(output)
    print('-----------')

command = f"{python_bin} \"{script_folder}/report.py\" --log-file=\"{log_file}\" --since=\"{since}\" --until=\"{until}\" --output-mode=\"basic\""
output  = os.popen(command).read().strip()
print(output)
