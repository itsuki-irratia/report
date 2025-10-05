import sys
import os
import re
import json
import pandas            as pd
import matplotlib.pyplot as plt
import numpy             as np
from lib.common          import Common

python_bin    = "/usr/bin/python3"
script_folder = os.path.dirname(os.path.abspath(__file__))
command       = f"{python_bin} \"{script_folder}/report.py\""

arguments     = Common.getArguments()
log_file      = arguments['log-file']
since         = arguments['since']
since_date    = re.sub(r"\-[0-9]{2}\s+[^$]+$", '', since)
until         = arguments['until']
chart         = arguments['chart']

chart_title = 'Erabiltzaileak'
if chart == 'geos_country':
    chart_title = f"{chart_title} herrialdeko"
elif chart == 'geos_region':
    chart_title = f"{chart_title} eskualdeko"
elif chart == 'geos_city':
    chart_title = f"{chart_title} herriko"

command       = f"{command} --log-file=\"{log_file}\" --since=\"{since}\" --until=\"{until}\" --output-mode=\"geos\""
data          = json.loads(os.popen(command).read().strip())

s = pd.Series(data[chart])
s = s.sort_values(ascending=True).tail(10)

# Dynamically scale figure size depending on number of items
fig_height = max(5, len(s) * 0.3)   # 0.3 inch per bar, minimum 5
fig_width = 12                      # wide enough for readability

ax = s.plot(kind="barh", figsize=(fig_width, fig_height), color="steelblue")

#plt.xlabel("Erabiltzaileak")
plt.ylabel(chart.capitalize())
plt.title(f"{since_date}")

# Define x-axis ticks every 200 up to the max value
max_val = s.max()
#plt.xticks(np.arange(0, max_val + 200, 200), rotation=-45)

# Add labels: inside in white if > 200, else outside in black
for i, (device, value) in enumerate(s.items()):
    if value > 200:
        ax.text(value - (max_val * 0.02), i, str(value),
                va='center', ha='right', color='white',
                fontsize=10, fontweight='bold')
    else:
        ax.text(value + 5, i, str(value),
                va='center', ha='left', color='black',
                fontsize=10)

plt.tight_layout()

# Show on screen
plt.show()

# Save high-resolution image
#plt.savefig("chart.png", dpi=300, bbox_inches="tight")
