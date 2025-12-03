import sys
import os
import re
import calendar
from collections import OrderedDict

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
    year          = int(re.search(r"^([0-9]{4})", since).group(1))
    month         = int(re.search(r"^[0-9]{4}\-([0-9]{2})", since).group(1))
    day           = int(re.search(r"^[0-9]{4}\-[0-9]{2}\-([0-9]{2})", since).group(1))
    _, month_days = calendar.monthrange(year, month)

    # Hilabeteko bisitak
    mont_data     = r.get(since, until, 'basic')
    duration_data = Visit.duration2Human(mont_data['duration'])
    month_image   = VisitsMonth(log_file).save(since, until, 'basic')
    md            = Md.visistsMonth(since_d, mont_data, duration_data, month_image, width)

    # Eguneko bisitak

    month_visite_uniques = 0

    for i in range(day, month_days + 1):
        _day   = str(i).zfill(2)
        _since = f"{year}-{month}-{_day} 00:00:00"
        _until = f"{year}-{month}-{_day} 23:59:59"

        print(f"{_since} {_until}")

        day_data             = r.get(_since, _until, 'basic')
        day_image            = VisitsDay(log_file).save(_since, _until, 'basic')
        month_visite_uniques = month_visite_uniques + day_data['unique']

        md                   = f"""{md}
## BISITAK: {since_d}
        """
        md                   = f"""{md}
{Md.visistsDay(f"{since_d}-{_day}", day_data, day_image, width)}
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
## GEOLOKALIZAZIOA 
### HERRIAK
![]({city_image}){width}
<div style="page-break-after: always;"></div>
### ESKUALDEAK
![]({region_image}){width}
<div style="page-break-after: always;"></div>
### HERRIALDEAK
![]({country_image}){width}
<div style="page-break-after: always;"></div>
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
## GAILUAK
![]({devices_image}){width}
<div style="page-break-after: always;"></div>
    """
    """
    pprint(geos_city)
    pprint(geos_region)
    pprint(geos_country)
    """
    return md

def _Intro():
    md = f"""
# ITSUKI IRRATIAREN<br>BISITA TXOSTENA<br>{since_d}
<div style="page-break-after: always;"></div>
    """
    return md

def _Outro():
    md = f"""
## KODEA
https://github.com/itsuki-irratia/report
    """
    return md

md = f"""
{_Intro()}
{_Visits()}
{_Geos()}
{_Devices()}
{_Outro()}
"""

with open(f"report/{since_d}.md", "w") as file:
    file.write(md)

command = f"/usr/bin/pandoc report/{since_d}.md -f markdown --pdf-engine=weasyprint --css=md.css -o report/{since_d}.pdf"
os.system(command)

sys.exit()