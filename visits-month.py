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
since_date    = re.sub(r"\-[0-9]+\s+[^$]+$", '', since)
until         = arguments['until']

since_ts      = Common.getTimestampFromDateString(since)
until_ts      = Common.getTimestampFromDateString(until)

data          = []
interval      = 3600 * 24

for i in range(since_ts, until_ts, interval):
    _since = datetime.fromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S')
    _until = datetime.fromtimestamp(i+interval-1).strftime('%Y-%m-%d %H:%M:%S')

    output = Report.get(log_file, _since, _until, 'basic')
    print(output)
    data.append(output)

# Load into DataFrame
df = pd.DataFrame(data)

# Convert "since" to datetime for plotting
df["since"] = pd.to_datetime(df["since"])

# Set index to datetime if desired
df.set_index("since", inplace=True)

plt.figure(figsize=(12,6))
plt.plot(df.index, df["visits"],        marker="o", label="Konexioak")
plt.plot(df.index, df["visits_unique"], marker="s", label="Bisitari bakarrak")
plt.title(f"{since_date} hilabeteko bisitak")

# Add value labels with white background
for i, v in enumerate(df["visits"]):
    if v > 0:
        plt.text(df.index[i], v + 10, str(v), ha='center', va='bottom', fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=1.0, edgecolor='none'))

for i, v in enumerate(df["visits_unique"]):
    if v > 0:
        plt.text(df.index[i], v - 15, str(v), ha='center', va='top', fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=1.0, edgecolor='none'))

plt.legend()
plt.grid(True)

plt.gca().yaxis.set_major_locator(MultipleLocator(200))
plt.ylim(bottom=0)

plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

plt.xlim(df.index.min(), df.index.max())

plt.xticks(rotation=-45, ha='left')
plt.tight_layout()
plt.show()