import re
import pandas            as     pd
import matplotlib.pyplot as     plt
import matplotlib.dates  as     mdates
from matplotlib.ticker   import MultipleLocator
from lib.common          import Common
from lib.report          import Report

class VisitsDay:

    def __init__(self, log_file):
        self.log_file = log_file
        self.interval = 3600
        self.report = Report(log_file)

    def get(self, since, until, output_mode):
        since_date       = re.sub(r"\s+[^$]+$", '', since)
        self.output_file = f"./build/visits-day-{since_date}.svg"

        since_ts = Common.getTimestampFromDateString(since)
        until_ts = Common.getTimestampFromDateString(until)
        data     = []
        used     = []

        # ordu aldaketie dala eta trapitxeue ein bizan dot
        for i in range(since_ts, until_ts, self.interval):
            _since = Common.getDateStringFromTimestamp(i)
            _hour = re.sub(r"[0-9]+\-[0-9]+\-[0-9]+\s+([0-9]+):[0-9]+:[0-9]+", '\\1', _since)
            _until = re.sub(r"\s+[0-9]+:[0-9]+:[0-9]+$", f" {_hour}:59:59", _since)
            if _since in used:
                continue

            output = self.report.get(_since, _until, output_mode)
            print(output)
            data.append(output)
            used.append(_since)

        # Load into DataFrame
        df = pd.DataFrame(data)

        # Convert "since" to datetime for plotting
        df["since"] = pd.to_datetime(df["since"])
        df.set_index("since", inplace=True)

        # ✅ Correctly unpack fig and ax
        fig, ax = plt.subplots(figsize=(12, 6))

        connection, = ax.plot(df.index, df["connections"], marker="o", label="Konexioak")
        unique,     = ax.plot(df.index, df["unique"],      marker="s", label="Bisitari bakarrak")
        #ax.set_title(f"{since_date} eguneko bisitak")
        ax.set_title('')

        # Add value labels with white background
        for i, v in enumerate(df["connections"]):
            if v > 0:
                ax.text(df.index[i], v, str(v), ha='center', va='bottom', fontsize=9,
                        bbox=dict(
                            boxstyle="round,pad=0.3",
                            facecolor='white',
                            alpha=1.0,
                            edgecolor=connection.get_color(),
                            linewidth=2
                        ))

        for i, v in enumerate(df["unique"]):
            if v > 0:
                ax.text(df.index[i], v, str(v), ha='center', va='top', fontsize=9,
                        bbox=dict(
                            boxstyle="round,pad=0.3",
                            facecolor='white',
                            alpha=1.0,
                            edgecolor=unique.get_color(),
                            linewidth=2
                        ))

        ax.legend()
        ax.grid(True)

        ax.yaxis.set_major_locator(MultipleLocator(25))
        ax.set_ylim(bottom=0)

        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

        plt.setp(ax.get_xticklabels(), rotation=-45, ha='right')

        fig.tight_layout()
        plt.close(fig)
        return fig

    def save(self, since, until, output_mode):
        fig = self.get(since, until, output_mode)
        fig.savefig(self.output_file, dpi=600, bbox_inches='tight')
        print(f"VisitsDay: saved: {self.output_file}")
        return self.output_file
