import matplotlib.pyplot as plt
import numpy as np
from src.analytics import Analytics


class Visualizer:
    def __init__(self, analytics, risk_free_rate = 0.04):
        self.risk_free_rate = risk_free_rate
        self.analytics = analytics
    def plot_simulation(self):
        matrix = self.analytics.price_matrix
        figure, axes = plt.subplots(nrows=1, ncols=1)
        figure.patch.set_facecolor('#131722')
        axes.set_xlabel("Date", fontsize=12, fontweight="bold", labelpad=10, color="#787B86")
        axes.set_ylabel("Price", rotation=90, labelpad=10, fontsize=12, color="#787B86")
        axes.set_axisbelow(True)
        axes.grid(True, color="#787B86", alpha=0.3, linestyle="--", linewidth=0.5)
        axes.set_facecolor("#131722")
        axes.tick_params(axis="both", which="major", labelsize=12, labelcolor="#787B86")


        axes.spines["top"].set_visible(False)
        axes.spines["right"].set_visible(False)
        axes.spines["left"].set_visible(False)
        axes.spines["bottom"].set_visible(False)

        size = min(175, matrix.shape[0])
        sample = np.random.choice(matrix.shape[0], size, replace=False)
        sample_matrix = matrix[sample]
        profit_paths = sample_matrix[sample_matrix[:,-1] >
                                     self.analytics.start_price]
        loss_paths = sample_matrix[sample_matrix[:,-1] <
                                   self.analytics.start_price]

        axes.plot(loss_paths.T, linewidth=1, alpha=0.5, color="#ef5350")
        axes.plot(profit_paths.T, linewidth=1, alpha=0.5, color="#26a69a")

        mean = np.mean(matrix,axis=0)
        axes.plot(mean.T, linewidth=2, alpha=1, color="blue", label="Average Return")

        axes.axhline(self.analytics.start_price, linewidth=1.5, color="black",
                   linestyle="--",)
        axes.set_xlim(0, matrix.shape[1] - 1)

        p5 = np.percentile(matrix, 5, axis=0)
        p95 = np.percentile(matrix, 95, axis=0)
        axes.fill_between(np.arange(matrix.shape[1]), p5, p95, facecolor="gray",
                        alpha=0.5, label="90% confidence zone", zorder=2)
        # axes.legend(loc="upper left", fontsize=12, frameon=False,
        #           facecolor="#787B86", edgecolor="#787B86")
        axes.legend(loc="upper left", fontsize=12, frameon=False,
                    facecolor="#787B86", edgecolor="#787B86",
                    labelcolor='#b3b3b3')
        plt.savefig("simulation_results.png", dpi=300, bbox_inches="tight")

