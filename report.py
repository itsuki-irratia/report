#!/usr/bin/python3
# -*- coding: utf-8 -*-

# example: python3 report.py --log-file="09.log" --since="2025-09-01 00:00:00" --until="2025-09-01 23:59:59" --output-mode="basic"

import sys
import json
from datetime   import datetime

from lib.common import Common
from lib.log    import Log

from lib.visit  import Visit
from lib.device import Device
from lib.app    import App
from lib.geo    import Geo

arguments     = Common.getArguments()
output_mode   = arguments['output-mode']
since         = Common.getDateStringTimestamp(arguments['since'])
until         = Common.getDateStringTimestamp(arguments['until'])
logs          = Log.getLines(arguments['log-file'])
logs          = Log.getByDates(logs, since, until, output_mode)

visits        = Visit.get(logs)
visits_unique = Visit.getUnique(logs)

result = {
    "since":         arguments['since'],
    "until":         arguments['until'],
    "visits":        visits,
    "visits_unique": visits_unique,
}

if(output_mode == 'devices'):
    result['devices'] = Device.gets(logs)

elif(output_mode == 'apps'):
    result['apps']    = App.gets(logs)

elif(output_mode == 'geos'):
    result['geos_city']    = Geo.getCities(logs)
    result['geos_region']  = Geo.getRegions(logs)
    result['geos_country'] = Geo.getCountries(logs)

elif(output_mode == 'full'):
    result['visits_ogg']   = Visit.getOgg(logs)
    result['visits_mp3']   = Visit.getMp3(logs)
    result['devices']      = Device.gets(logs)
    result['apps']         = App.gets(logs)
    result['geos_city']    = Geo.getCities(logs)
    result['geos_region']  = Geo.getRegions(logs)
    result['geos_country'] = Geo.getCountries(logs)


print(json.dumps(result, indent=4))
sys.exit()
