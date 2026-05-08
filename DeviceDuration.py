import pandas            as pd
import matplotlib.pyplot as plt

class DeviceDuration:

    def __init__(self):
        pass

    def get(self, date, data):
        self.output_file = f"./build/devices-dur-{date}.svg"

        # Convert seconds to minutes
        data_min = {k: round(v / 60, 1) for k, v in data.items()}

        s = pd.Series(data_min)
        s = s.sort_values(ascending=True)

        fig_height = max(5, len(s) * 0.3)
        fig_width  = 12

        ax = s.plot(kind="barh", figsize=(fig_width, fig_height), color="darkorange")

        plt.ylabel(f"{date}".capitalize())
        plt.title(f"{date}")
        plt.xlabel("minutuak")

        max_val = s.max()

        for i, (device, value) in enumerate(s.items()):
            if value > max_val - (max_val * 0.1):
                ax.text(max_val * 0.98, i, str(value),
                        va='center', ha='right', color='white',
                        fontsize=10, fontweight='bold')
            else:
                ax.text(value + max_val * 0.01, i, str(value),
                        va='center', ha='left', color='black',
                        fontsize=10)

        plt.tight_layout()
        fig = ax.get_figure()
        plt.close(fig)
        return fig

    def save(self, date, data):
        graphic = self.get(date, data)
        graphic.savefig(self.output_file, dpi=600, bbox_inches='tight')
        print(f"DeviceDuration saved: {self.output_file}")
        return self.output_file
