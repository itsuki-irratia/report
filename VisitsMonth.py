import re
import pandas            as     pd
import matplotlib.pyplot as     plt
import matplotlib.dates  as     mdates
from datetime            import datetime
from matplotlib.ticker   import MultipleLocator

from lib.common          import Common
from lib.report          import Report

class VisitsMonth:

    def __init__(self, log_file):
        self.log_file    = log_file
        self.interval    = 3600 * 24
        self.report      = Report(log_file)

    def get(self, since, until, output_mode):
        since_date       = re.sub(r"\s+[^$]+$", '', since)
        self.output_file = f"./build/visits-month-{since_date}.svg"
        since_ts         = Common.getTimestampFromDateString(since)
        until_ts         = Common.getTimestampFromDateString(until)
        data             = []

        for i in range(since_ts, until_ts, self.interval):
            _since = datetime.fromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S')
            _until = datetime.fromtimestamp(i+self.interval-1).strftime('%Y-%m-%d %H:%M:%S')

            output = self.report.get(_since, _until, output_mode)
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
        #plt.show()
        return plt

    def save(self, since, until, output_mode):
        graphic = self.get(since, until, output_mode)
        graphic.savefig(self.output_file, dpi=600, bbox_inches='tight')
        print(f"VisitsMonth: saved: {self.output_file}")
        return self.output_file