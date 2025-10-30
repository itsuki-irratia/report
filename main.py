import sys
import os
import re
from collections import OrderedDict

from pprint      import pprint
from lib.common  import Common
from lib.visit   import Visit
from lib.report  import Report
from VisitsMonth import VisitsMonth
from VisitsDay   import VisitsDay
from Geos        import Geos
from Devices     import Devices
from lib.md      import Md

arguments = Common.getArguments()
log_file  = arguments['log-file']
since     = arguments['since']
until     = arguments['until']
since_d   = re.sub(r"\-[0-9]+\s+[0-9]+:[0-9]+:[0-9]+$", '', since)
r         = Report(log_file)
width     = r"{ width=100% }"

def _Visits():
    # Hilabeteko bisitak
    mont_data     = r.get(since, until, 'basic')
    duration_data = Visit.duration2Human(mont_data['duration'])
    month_image   = VisitsMonth(log_file).save(since, until, 'basic')

    md            = Md.visistsMonth(since_d, mont_data, duration_data, month_image, width)

    # Eguneko bisitak

    since_ts             = Common.getTimestampFromDateString(since)
    until_ts             = Common.getTimestampFromDateString(until)
    interval             = 3600 * 24

    month_visite_uniques = 0

    for i in range(since_ts, until_ts, interval):
        _since               = Common.getDateStringFromTimestamp(i)
        _until               = Common.getDateStringFromTimestamp(i+interval-1)
        _since_d             = re.sub(r"\s+[0-9]+:[0-9]+:[0-9]+$", '', _since)

        day_data             = r.get(_since, _until, 'basic')
        day_image            = VisitsDay(log_file).save(_since, _until, 'basic')
        month_visite_uniques = month_visite_uniques + day_data['unique']

        md                   = f"""{md}
{Md.visistsDay(since_d, day_data, day_image, width)}
        """

    rest_month_visit = month_visite_uniques - mont_data['unique']
    md = f"""{md}
{Md.notes(month_visite_uniques, mont_data, rest_month_visit)}
    """
    return md

def _Geos():
    geo_data      = r.get(since, until, 'geos')
    geos_city     = OrderedDict(sorted(geo_data['geos_city'].items(),    key=lambda x: x[1], reverse=True)[:20])
    geos_region   = OrderedDict(sorted(geo_data['geos_region'].items(),  key=lambda x: x[1], reverse=True)[:20])
    geos_country  = OrderedDict(sorted(geo_data['geos_country'].items(), key=lambda x: x[1], reverse=True)[:20])

    city_image    = Geos().save('city',    since_d, geos_city)
    region_image  = Geos().save('region',  since_d, geos_region)
    country_image = Geos().save('country', since_d, geos_country)

    md = f"""
![]({city_image}){width}
<div style="page-break-after: always;"></div>
![]({region_image}){width}
<div style="page-break-after: always;"></div>
![]({country_image}){width}
    """
    """
    pprint(geos_city)
    pprint(geos_region)
    pprint(geos_country)
    """
    return md

def _Devices():
    devices_data  = r.get(since, until, 'devices')['devices']
    devices_data  = OrderedDict(sorted(devices_data.items(), key=lambda x: x[1], reverse=True))
    devices_image = Devices().save(since_d, devices_data)

    md = f"""
![]({devices_image}){width}
<div style="page-break-after: always;"></div>
    """
    """
    pprint(geos_city)
    pprint(geos_region)
    pprint(geos_country)
    """
    return md

def _Outro():
    pass

md = f"""
{_Visits()}
{_Geos()}
{_Devices()}
"""

#md = f"""
#{Md.intro()}
#{_Visits()}
#{_Geos()}
#{_Devices()}
#{_Outro()}
#"""

with open(f"report/{since_d}.md", "w") as file:
    file.write(md)

command = f"/usr/bin/pandoc report/{since_d}.md -f markdown --pdf-engine=weasyprint -o report/{since_d}.pdf"
os.system(command)

sys.exit()