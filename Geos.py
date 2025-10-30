import re
import pandas            as     pd
import matplotlib.pyplot as     plt
import matplotlib.dates  as     mdates
from datetime            import datetime
from matplotlib.ticker   import MultipleLocator

from lib.common          import Common
from lib.report          import Report

class Geos:

    def __init__(self):
        pass

    def get(self, _type, date, data):
        self.output_file = f"./build/geos-{_type}-{date}.svg"

        print(data)

        s = pd.Series(data)
        s = s.sort_values(ascending=True)

        # Dynamically scale figure size depending on number of items
        fig_height = max(5, len(s) * 0.3)   # 0.3 inch per bar, minimum 5
        fig_width = 12                      # wide enough for readability

        ax = s.plot(kind="barh", figsize=(fig_width, fig_height), color="steelblue")

        #plt.xlabel("Erabiltzaileak")
        plt.ylabel(f"{_type} {date}".capitalize())
        plt.title(f"{date}")

        # Define x-axis ticks every 200 up to the max value
        max_val = s.max()
        #plt.xticks(np.arange(0, max_val + 200, 200), rotation=-45)

        # Add labels: inside in white if > 200, else outside in black
        for i, (device, value) in enumerate(s.items()):
            if value > max_val - 20:
                ax.text((max_val - 10), i, str(value),
                        va='center', ha='right', color='white',
                        fontsize=10, fontweight='bold')
            else:
                ax.text(value + 5, i, str(value),
                        va='center', ha='left', color='black',
                        fontsize=10)

        plt.tight_layout()
        fig = ax.get_figure()
        plt.close(fig)
        return fig

    def save(self, _type, date, data):
        graphic = self.get(_type, date, data)
        graphic.savefig(self.output_file, dpi=600, bbox_inches='tight')
        print(f"Geos saved: {self.output_file}")
        return self.output_file