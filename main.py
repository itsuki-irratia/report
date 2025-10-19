import sys

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
mainfont: "Courier New"
fontsize: 11pt
geometry: margin=2cm
---
# ITSUKI IRRATIAKO<br>ERREPORTE SISTEMA
Noiztik:&nbsp;&nbsp; **{since}**  
Noiz arte: **{until}**  

"""

# Hilabeteko bisitak

r           = Report(log_file)
mont_data   = r.get(since, until, 'basic')
month_image = VisitsMonth(log_file).save(since, until, 'basic')

md = f"""{md}
Konexioak:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **{mont_data['visits']}**  
Bisitari bakarrak: **{mont_data['visits_unique']}** 
![]({month_image})

"""

# Eguneko bisitak

since_ts = Common.getTimestampFromDateString(since)
until_ts = Common.getTimestampFromDateString(until)

interval = 3600 * 24

for i in range(since_ts, until_ts, interval):
    _since   = Common.getDateStringFromTimestamp(i)
    _until   = Common.getDateStringFromTimestamp(i+interval-1)

    day_data  = r.get(_since, _until, 'basic')
    day_image = VisitsDay(log_file).save(_since, _until, 'basic')
    md = f"""{md}
Konexioak:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **{day_data['visits']}**  
Bisitari bakarrak: **{day_data['visits_unique']}** 
![]({day_image})

    """

with open("report.md", "w") as file:
    file.write(md)

sys.exit()