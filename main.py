import sys

from lib.common  import Common
from VisitsMonth import VisitsMonth
from VisitsDay   import VisitsDay

arguments     = Common.getArguments()
log_file      = arguments['log-file']
since         = arguments['since']
until         = arguments['until']

VisitsMonth(log_file, since, until).save()

sys.exit()

since_ts      = Common.getTimestampFromDateString(arguments['since'])
until_ts      = Common.getTimestampFromDateString(arguments['until'])

interval = 3600 * 24
for i in range(since_ts, until_ts, interval):
    _since = Common.getDateStringFromTimestamp(i)
    _until = Common.getDateStringFromTimestamp(i+interval-1)

    VisitsDay(log_file, _since, _until).save()
