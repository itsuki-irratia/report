#!/usr/bin/python3
# -*- coding: utf-8 -*-

# example: python3 report.py --log-file="09.log" --since="2025-09-01 00:00:00" --until="2025-09-01 23:59:59" --output-mode="basic"

import sys
import json
import hashlib
from datetime   import datetime

from lib.common import Common
from lib.log    import Log

from lib.visit  import Visit
from lib.device import Device
from lib.app    import App
from lib.geo    import Geo

class Report:

    def __init__(self, log_file):
        self.log_file = log_file
        self.cache    = None

    def getCache(self):
        if self.cache:
            return self.cache
        return None

    def setCache(self, value):
        self.cache = value
        return True

    def get(self, since, until, output_mode):
        _since = Common.getTimestampFromDateString(since)
        _until = Common.getTimestampFromDateString(until)
        logs   = self.getCache()

        if logs == None:
            logs          = Log.getLines(self.log_file)
            self.setCache(logs)

        logs          = Log.getByDates(logs, _since, _until, output_mode)

        visits        = Visit.get(logs)
        visits_unique = Visit.getUnique(logs)

        result = {
            "since":         since,
            "until":         until,
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

        return result
        """
        print(json.dumps(result, indent=4))
        sys.exit()
        """
