"""
Interact module for the Confidence Interval notebook.
Provides the interactive widget for exploring how sample size and confidence level
affect the width of a confidence interval for the mean.
"""

import numpy as np
from scipy import stats
import ipywidgets as widgets
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from IPython.display import display


def _update_ci_plot(population, n, confidence_level, out, show_true_mean=False):
    """Draw a sample, compute CI, and plot histogram with CI and width."""
    with out:
        out.clear_output(wait=True)
        sample = np.random.choice(population, size=n, replace=False)
        sample_mean = np.mean(sample)
        sample_std = np.std(sample, ddof=1)
        true_mean = float(np.mean(population))

        alpha = 1 - confidence_level
        z = stats.norm.ppf(1 - alpha / 2)
        se = sample_std / np.sqrt(n)
        ci_low = sample_mean - z * se
        ci_high = sample_mean + z * se
        width = ci_high - ci_low

        fig, ax = plt.subplots(figsize=(10, 5.5), facecolor="white")
        ax.set_facecolor("#fafafa")

        bins = min(28, max(6, n // 4))
        n_hist, _, patches = ax.hist(
            sample, bins=bins, color="#4a90d9", edgecolor="white", linewidth=1.2,
            density=True, alpha=0.85, label="Sample distribution"
        )
        ax.axvspan(ci_low, ci_high, alpha=0.18, color="#c44e52", zorder=0)
        ax.axvline(ci_low, color="#c44e52", linestyle="-", linewidth=2.5, label=f"{int(confidence_level * 100)}% CI")
        ax.axvline(ci_high, color="#c44e52", linestyle="-", linewidth=2.5)
        ax.axvline(sample_mean, color="#2d2d2d", linestyle="--", linewidth=2, label=f"Sample mean = {sample_mean:.2f}")
        if show_true_mean:
            ax.axvline(
                true_mean,
                color="#1b7f3a",
                linestyle="-",
                linewidth=2.5,
                zorder=4,
                label=f"True population mean = {true_mean:.2f}",
            )

        ax.set_xlabel("Study hours", fontsize=12, color="#333")
        ax.set_ylabel("Density", fontsize=12, color="#333")
        ax.tick_params(colors="#555", labelsize=10)
        ax.set_ylim(bottom=0)
        ymax = ax.get_ylim()[1]
        xmin, xmax = ax.get_xlim()
        # Stack Lower/Upper CI in upper-left so they never overlap
        ci_text = f"Lower CI = {ci_low:.2f}\nUpper CI = {ci_high:.2f}"
        ax.text(xmin + (xmax - xmin) * 0.02, ymax * 0.94, ci_text, fontsize=10, color="#c44e52",
                ha="left", va="top", fontweight="bold", linespacing=1.4,
                bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#c44e52", alpha=0.95))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.2f}"))
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(True, axis="y", alpha=0.35, linestyle="--")
        ax.legend(loc="upper right", frameon=True, fancybox=True, shadow=True, fontsize=10)

        title = f"Sample size n = {n}   →   {int(confidence_level * 100)}% CI = ({ci_low:.2f}, {ci_high:.2f})   →   Width = {width:.2f} hours"
        ax.set_title(title, fontsize=12, color="#333", pad=12)
        plt.tight_layout()
        plt.show()


def interact_ci(population):
    """Run the interactive widget: histogram, CI lines, and width update with n and confidence level.

    The Resample button draws a new random sample without changing the sliders.
    Toggle Show true mean to overlay the population mean the CI is estimating.
    """
    n_slider = widgets.IntSlider(
        min=10, max=200, step=10, value=40,
        description="Sample size (n):",
        style={"description_width": "140px"},
        layout=widgets.Layout(width="320px"),
    )
    level_slider = widgets.FloatSlider(
        min=0.80, max=0.99, step=0.01, value=0.95,
        description="Confidence level:",
        style={"description_width": "140px"},
        layout=widgets.Layout(width="320px"),
    )
    resample_btn = widgets.Button(
        description="Resample",
        tooltip="Draw a new random sample with the same n and confidence level",
        layout=widgets.Layout(width="120px"),
    )
    true_mean_toggle = widgets.Checkbox(
        value=False,
        description="Show true mean",
        indent=False,
        style={"description_width": "initial"},
        layout=widgets.Layout(margin="0 0 0 16px"),
    )
    out = widgets.Output()

    def on_change(change=None):
        _update_ci_plot(
            population,
            n_slider.value,
            level_slider.value,
            out,
            show_true_mean=true_mean_toggle.value,
        )

    def on_resample(_):
        on_change()

    n_slider.observe(on_change, names="value")
    level_slider.observe(on_change, names="value")
    true_mean_toggle.observe(on_change, names="value")
    resample_btn.on_click(on_resample)

    controls_row2 = widgets.HBox([resample_btn, true_mean_toggle])
    box = widgets.VBox([
        widgets.HBox([n_slider, level_slider]),
        controls_row2,
        out,
    ])
    display(box)
    on_change()


def plot_many_confidence_intervals(population, n, confidence_level=0.85, n_intervals=40):
    """
    Plot many confidence intervals for the population mean and highlight which
    intervals contain the true mean.

    This is used in the student notebook to illustrate that the true value is
    not always in the center of the interval, but is likely to be somewhere
    inside most of them.

    Parameters
    ----------
    population : array-like
        The population values to sample from.
    n : int
        Sample size for each interval.
    confidence_level : float, optional
        Confidence level for each interval (e.g. 0.85 for 85%).
    n_intervals : int, optional
        Number of intervals to generate and plot.
    """
    true_mean = np.mean(population)
    alpha = 1 - confidence_level
    z = stats.norm.ppf(1 - alpha / 2)

    ci_lowers, ci_uppers = [], []
    for _ in range(n_intervals):
        sample = np.random.choice(population, size=n, replace=False)
        sample_mean = np.mean(sample)
        se = np.std(sample, ddof=1) / np.sqrt(n)
        ci_lowers.append(sample_mean - z * se)
        ci_uppers.append(sample_mean + z * se)

    contains = sum(a <= true_mean <= b for a, b in zip(ci_lowers, ci_uppers))

    plt.figure(figsize=(8, 6))
    for i, (a, b) in enumerate(zip(ci_lowers, ci_uppers)):
        color = "steelblue" if a <= true_mean <= b else "coral"
        plt.plot([a, b], [i, i], color=color, linewidth=1.5)

    plt.axvline(true_mean, color="green", linestyle="--", linewidth=2)
    plt.xlabel("Study hours per week")
    plt.ylabel("Sample (each line is a different sample)")
    plt.title(
        f"{n_intervals} different {int(confidence_level * 100)}% CIs: "
        f"{contains} contain the true mean (~{100 * contains / n_intervals:.0f}% coverage)"
    )
    # Legend: steelblue = interval covers true mean; coral = interval misses (true mean is outside)
    pct = int(confidence_level * 100)
    legend_handles = [
        Line2D(
            [0], [0], color="steelblue", linewidth=2.5,
            label=f"Blue: {pct}% CI contains true mean",
        ),
        Line2D(
            [0], [0], color="coral", linewidth=2.5,
            label=f"Orange: {pct}% CI does not contain true mean",
        ),
        Line2D(
            [0], [0], color="green", linestyle="--", linewidth=2,
            label="Green dashed: true population mean",
        ),
    ]
    plt.legend(handles=legend_handles, loc="lower right", frameon=True)
    plt.tight_layout()
    plt.show()


def plot_bootstrap_mean_distribution(boot_means, boot_ci_lower, boot_ci_upper, sample_mean):
    """
    Plot the bootstrap distribution of the sample mean with CI endpoints and the sample mean.

    Parameters
    ----------
    boot_means : array-like
        Bootstrap sample means.
    boot_ci_lower : float
        Lower endpoint of the bootstrap confidence interval.
    boot_ci_upper : float
        Upper endpoint of the bootstrap confidence interval.
    sample_mean : float
        The original sample mean.
    """
    plt.figure(figsize=(8, 5))
    plt.hist(boot_means, bins=30, density=False, color="skyblue", edgecolor="white")
    plt.axvline(boot_ci_lower, color="red", linestyle="--", label="2.5% percentile")
    plt.axvline(boot_ci_upper, color="red", linestyle="--", label="97.5% percentile")
    plt.axvline(sample_mean, color="black", linestyle=":", label="Sample mean")
    plt.xlabel("Bootstrap sample mean (hours)")
    plt.ylabel("Frequency")
    plt.title("Bootstrap Distribution of the Sample Mean")
    plt.legend()
    plt.tight_layout()
    plt.show()
