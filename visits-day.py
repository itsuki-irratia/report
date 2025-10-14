import re
import pandas            as     pd
import matplotlib.pyplot as     plt
import matplotlib.dates  as     mdates
from datetime            import datetime
from matplotlib.ticker   import MultipleLocator

from lib.common          import Common
from lib.report          import Report

arguments     = Common.getArguments()
log_file      = arguments['log-file']
since         = arguments['since']
since_date    = re.sub(r"\s+[^$]+$", '', since)
until         = arguments['until']

since_ts      = Common.getTimestampFromDateString(since)
until_ts      = Common.getTimestampFromDateString(until)

data          = []
interval      = 3600

"""
for i in range(since_ts, until_ts, interval):
    _since = datetime.fromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S')
    _until = datetime.fromtimestamp(i+interval-1).strftime('%Y-%m-%d %H:%M:%S')

    output = Report.get(log_file, _since, _until, 'basic')
    print(output)
    data.append(output)
"""

data = [
{'since': '2025-09-30 00:00:00', 'until': '2025-09-30 00:59:59', 'visits': 144, 'visits_unique': 11},
{'since': '2025-09-30 01:00:00', 'until': '2025-09-30 01:59:59', 'visits': 136, 'visits_unique': 4},
{'since': '2025-09-30 02:00:00', 'until': '2025-09-30 02:59:59', 'visits': 136, 'visits_unique': 4},
{'since': '2025-09-30 03:00:00', 'until': '2025-09-30 03:59:59', 'visits': 133, 'visits_unique': 2},
{'since': '2025-09-30 04:00:00', 'until': '2025-09-30 04:59:59', 'visits': 161, 'visits_unique': 30},
{'since': '2025-09-30 05:00:00', 'until': '2025-09-30 05:59:59', 'visits': 141, 'visits_unique': 4},
{'since': '2025-09-30 06:00:00', 'until': '2025-09-30 06:59:59', 'visits': 136, 'visits_unique': 5},
{'since': '2025-09-30 07:00:00', 'until': '2025-09-30 07:59:59', 'visits': 147, 'visits_unique': 9},
{'since': '2025-09-30 08:00:00', 'until': '2025-09-30 08:59:59', 'visits': 139, 'visits_unique': 6},
{'since': '2025-09-30 09:00:00', 'until': '2025-09-30 09:59:59', 'visits': 178, 'visits_unique': 19},
{'since': '2025-09-30 10:00:00', 'until': '2025-09-30 10:59:59', 'visits': 211, 'visits_unique': 51},
{'since': '2025-09-30 11:00:00', 'until': '2025-09-30 11:59:59', 'visits': 187, 'visits_unique': 28},
{'since': '2025-09-30 12:00:00', 'until': '2025-09-30 12:59:59', 'visits': 158, 'visits_unique': 20},
{'since': '2025-09-30 13:00:00', 'until': '2025-09-30 13:59:59', 'visits': 170, 'visits_unique': 21},
{'since': '2025-09-30 14:00:00', 'until': '2025-09-30 14:59:59', 'visits': 147, 'visits_unique': 11},
{'since': '2025-09-30 15:00:00', 'until': '2025-09-30 15:59:59', 'visits': 144, 'visits_unique': 11},
{'since': '2025-09-30 16:00:00', 'until': '2025-09-30 16:59:59', 'visits': 170, 'visits_unique': 36},
{'since': '2025-09-30 17:00:00', 'until': '2025-09-30 17:59:59', 'visits': 141, 'visits_unique': 9},
{'since': '2025-09-30 18:00:00', 'until': '2025-09-30 18:59:59', 'visits': 156, 'visits_unique': 16},
{'since': '2025-09-30 19:00:00', 'until': '2025-09-30 19:59:59', 'visits': 145, 'visits_unique': 10},
{'since': '2025-09-30 20:00:00', 'until': '2025-09-30 20:59:59', 'visits': 142, 'visits_unique': 7},
{'since': '2025-09-30 21:00:00', 'until': '2025-09-30 21:59:59', 'visits': 143, 'visits_unique': 7},
{'since': '2025-09-30 22:00:00', 'until': '2025-09-30 22:59:59', 'visits': 164, 'visits_unique': 34},
{'since': '2025-09-30 23:00:00', 'until': '2025-09-30 23:59:59', 'visits': 143, 'visits_unique': 9}    
]

# Load into DataFrame
df = pd.DataFrame(data)

# Convert "since" to datetime for plotting
df["since"] = pd.to_datetime(df["since"])

# Set index to datetime if desired
df.set_index("since", inplace=True)

plt.figure(figsize=(12,6))
plt.plot(df.index, df["visits"],        marker="o", label="Konexioak")
plt.plot(df.index, df["visits_unique"], marker="s", label="Bisitari bakarrak")
plt.title(f"{since_date} eguneko bisitak")

# Add value labels with white background
for i, v in enumerate(df["visits"]):
    if v > 0:
        plt.text(df.index[i], v - 20, str(v), ha='center', va='bottom', fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=1.0, edgecolor='none'))

for i, v in enumerate(df["visits_unique"]):
    if v > 0:
        plt.text(df.index[i], v + 20, str(v), ha='center', va='top', fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=1.0, edgecolor='none'))

#plt.xlabel("")
#plt.ylabel("")
plt.legend()
plt.grid(True)

plt.gca().yaxis.set_major_locator(MultipleLocator(25))
plt.ylim(bottom=0)

# Your existing x-axis formatting
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))  # or 1, 6, etc.
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

plt.xticks(rotation=-45)
plt.tight_layout()
plt.show()