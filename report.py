#!/usr/bin/python3
# -*- coding: utf-8 -*-

# example: python3 report.py --log-file="09.log" --since="2025-09-01 00:00:00" --until="2025-09-30 23:59:59" --output-mode="basic"

import sys
import json

from lib.common import Common
from lib.report import Report

arguments     = Common.getArguments()
output_mode   = arguments['output-mode']
since         = Common.getTimestampFromDateString(arguments['since'])
until         = Common.getTimestampFromDateString(arguments['until'])

result        = Report.get(arguments['log-file'], arguments['since'], arguments['until'], output_mode)

print(json.dumps(result, indent=4))
sys.exit()
