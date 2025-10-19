import sys
import os
import re

from lib.common  import Common
from lib.report  import Report
from VisitsMonth import VisitsMonth
from VisitsDay   import VisitsDay

arguments = Common.getArguments()
log_file  = arguments['log-file']
since     = arguments['since']
until     = arguments['until']

md = f"""
---
mainfont: "Liberation Mono"
fontsize: 14pt
---
# ITSUKI IRRATIAKO<br>ERREPORTE SISTEMA  
<div style="page-break-after: always;"></div>
"""

# Hilabeteko bisitak

since_d = re.sub(r"\-[0-9]+\s+[0-9]+:[0-9]+:[0-9]+$", '', since)

r           = Report(log_file)
mont_data   = r.get(since, until, 'basic')
month_image = VisitsMonth(log_file).save(since, until, 'basic')

width = r"{ width=100% }"
md    = f"""{md}
## {since_d}

Konexioak:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **{mont_data['visits']}**  
Bisitari bakarrak: **{mont_data['visits_unique']}** 
![]({month_image}){width}
<div style="page-break-after: always;"></div>
"""

# Eguneko bisitak

since_ts = Common.getTimestampFromDateString(since)
until_ts = Common.getTimestampFromDateString(until)
interval = 3600 * 24

month_visite_uniques = 0
for i in range(since_ts, until_ts, interval):
    _since   = Common.getDateStringFromTimestamp(i)
    _until   = Common.getDateStringFromTimestamp(i+interval-1)
    _since_d = re.sub(r"\s+[0-9]+:[0-9]+:[0-9]+$", '', _since)

    day_data  = r.get(_since, _until, 'basic')
    day_image = VisitsDay(log_file).save(_since, _until, 'basic')

    month_visite_uniques = month_visite_uniques + day_data['visits_unique']

    md = f"""{md}
## {_since_d}

Konexioak:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **{day_data['visits']}**  
Bisitari bakarrak: **{day_data['visits_unique']}** 
![]({day_image}){width}
<div style="page-break-after: always;"></div>
    """

rest_month_visit = month_visite_uniques - mont_data['visits_unique']
md = f"""{md}
## OHARRAK

### BISITARI BAKARREN KALKULUA

Hilabetearen bisitari bakarren kalkulua ez dator bat eguneko bisitari bakarren batuketarekin.

**Zergatik?**

Egun ezberdinetan bisitari berberak irratia entzutera bueltatu direlako.

Beraz, honako formula hau erabiliko dugu, bueltan etorri diren bisitari kopurua kalkulatzeko:

Hilabetean eguneko bisita bakarren batura: **{month_visite_uniques}**  
Hilabeteko bisitak bakarrak:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **{mont_data['visits_unique']}**  
{month_visite_uniques} - {mont_data['visits_unique']} = **{rest_month_visit}**

Beraz, kenduketa eginda esan genezake bisitari bakar guztietatik (**{mont_data['visits_unique']}**), **{rest_month_visit}** berriz bueltatu direla **itsuki irratia** entzutera.
"""

with open(f"report/{since_d}.md", "w") as file:
    file.write(md)

command = f"/usr/bin/pandoc report/{since_d}.md -f markdown --pdf-engine=weasyprint -o report/{since_d}.pdf"
os.system(command)

sys.exit()