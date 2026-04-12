"""
visuals.py  —  Hypothesis Testing Notebook Helper Visuals
All interactive plots used in hypothesis_testing.ipynb.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.stats as stats
import ipywidgets as widgets
from IPython.display import display, clear_output


# ── shared style ────────────────────────────────────────────────────────────
COLORS = {
    "null":      "#4C72B0",   # blue  – H0 distribution
    "alt":       "#DD8452",   # orange – Ha / true distribution
    "reject":    "#C44E52",   # red   – rejection region
    "pval":      "#8172B2",   # purple – p-value area
    "crit":      "#2CA02C",   # green – critical value line
    "neutral":   "#808080",
}


def _float_text(**kwargs):
    """FloatText whose .value tracks the box while typing (ipywidgets ≥7)."""
    try:
        return widgets.FloatText(**kwargs, continuous_update=True)
    except TypeError:
        return widgets.FloatText(**kwargs)


# ── 1. Hypothesis Tails Visual ───────────────────────────────────────────────
def show_hypothesis_tails():
    """
    Interactive dropdown: left-tailed, right-tailed, two-tailed.
    Shows the rejection region shaded in red on a standard normal curve.
    """
    tail_dropdown = widgets.Dropdown(
        options=[
            ("Two-Tailed  (Ha: μ ≠ μ₀)", "two"),
            ("Left-Tailed  (Ha: μ < μ₀)", "left"),
            ("Right-Tailed  (Ha: μ > μ₀)", "right"),
        ],
        value="two",
        description="Test type:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="380px"),
    )
    alpha_slider = widgets.FloatSlider(
        value=0.05, min=0.01, max=0.20, step=0.01,
        description="α (alpha):",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="380px"),
        readout_format=".2f",
    )
    out = widgets.Output()

    def _normalize_tail(value):
        """
        Normalize dropdown value to one of: 'two', 'left', 'right'.
        Handles both explicit values and legacy label strings.
        """
        text = str(value).strip().lower()
        if "left" in text:
            return "left"
        if "right" in text:
            return "right"
        if "two" in text:
            return "two"
        return "right"

    def _draw(change=None):
        with out:
            clear_output(wait=True)
            tail_key = _normalize_tail(tail_dropdown.value)
            alpha    = alpha_slider.value

            x = np.linspace(-4, 4, 500)
            y = stats.norm.pdf(x)

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(x, y, color=COLORS["null"], linewidth=2.5)
            ax.set_xlabel("Standard Normal (z)", fontsize=12)
            ax.set_ylabel("Probability Density", fontsize=12)
            ax.set_yticks([])

            if tail_key == "two":
                z_crit = stats.norm.ppf(1 - alpha / 2)
                ax.fill_between(x, y, where=(x <= -z_crit), color=COLORS["reject"], alpha=0.55, label=f"Rejection region (α/2 each tail)")
                ax.fill_between(x, y, where=(x >=  z_crit), color=COLORS["reject"], alpha=0.55)
                ax.axvline(-z_crit, color=COLORS["crit"], linestyle="--", linewidth=1.8, label=f"Critical values ±{z_crit:.2f}")
                ax.axvline( z_crit, color=COLORS["crit"], linestyle="--", linewidth=1.8)
                ax.set_title(f"Two-Tailed Test  |  α = {alpha:.2f}  →  reject if |z| > {z_crit:.2f}", fontsize=12)

            elif tail_key == "left":
                z_crit = stats.norm.ppf(alpha)
                ax.fill_between(x, y, where=(x <= z_crit), color=COLORS["reject"], alpha=0.55, label=f"Rejection region (left)")
                ax.axvline(z_crit, color=COLORS["crit"], linestyle="--", linewidth=1.8, label=f"Critical value {z_crit:.2f}")
                ax.set_title(f"Left-Tailed Test  |  α = {alpha:.2f}  →  reject if z < {z_crit:.2f}", fontsize=12)

            else:  # right
                z_crit = stats.norm.ppf(1 - alpha)
                ax.fill_between(x, y, where=(x >= z_crit), color=COLORS["reject"], alpha=0.55, label=f"Rejection region (right)")
                ax.axvline(z_crit, color=COLORS["crit"], linestyle="--", linewidth=1.8, label=f"Critical value {z_crit:.2f}")
                ax.set_title(f"Right-Tailed Test  |  α = {alpha:.2f}  →  reject if z > {z_crit:.2f}", fontsize=12)

            ax.text(
                0,
                max(y) * 0.45,
                r"Fail to\nReject $H_0$",
                ha="center",
                fontsize=10,
                color=COLORS["null"],
                fontweight="bold",
            )
            ax.legend(fontsize=9)
            ax.set_xlim(-4, 4)
            plt.tight_layout()
            plt.show()

    tail_dropdown.observe(_draw, names="value")
    alpha_slider.observe(_draw, names="value")
    display(widgets.VBox([tail_dropdown, alpha_slider]), out)
    _draw()


# ── 2. Type I / Type II Error Visual ────────────────────────────────────────
def show_error_visual():
    """
    Shows two overlapping normal distributions (H0 and the true distribution).
    Shades Type I error (α) and Type II error (β) regions.
    Students can slide the 'true mean' to see how α and β trade off.
    """
    sep_slider = widgets.FloatSlider(
        value=1.8, min=0.5, max=3.5, step=0.1,
        description="True mean shift:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="420px"),
        readout_format=".1f",
    )
    alpha_slider = widgets.FloatSlider(
        value=0.05, min=0.01, max=0.20, step=0.01,
        description="α (alpha):",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="420px"),
        readout_format=".2f",
    )
    out = widgets.Output()

    def _draw(change=None):
        with out:
            clear_output(wait=True)
            sep   = sep_slider.value
            alpha = alpha_slider.value
            z_crit = stats.norm.ppf(1 - alpha)  # right-tailed critical value

            x = np.linspace(-4, sep + 4, 600)
            y_null = stats.norm.pdf(x, loc=0,   scale=1)
            y_true = stats.norm.pdf(x, loc=sep, scale=1)

            fig, ax = plt.subplots(figsize=(9, 4.5))

            # distributions
            ax.plot(
                x,
                y_null,
                color=COLORS["null"],
                linewidth=2.2,
                label=r"$H_0$ distribution (assumed)",
            )
            ax.plot(x, y_true, color=COLORS["alt"],   linewidth=2.2, label="True distribution (Ha)")

            # Type I error: area under H0 curve beyond critical value
            ax.fill_between(x, y_null, where=(x >= z_crit),
                            color=COLORS["reject"], alpha=0.45, label=f"Type I error (α = {alpha:.2f})")

            # Type II error: area under true curve below critical value
            beta = stats.norm.cdf(z_crit, loc=sep, scale=1)
            ax.fill_between(x, y_true, where=(x <= z_crit),
                            color=COLORS["alt"], alpha=0.35, label=f"Type II error (β ≈ {beta:.2f})")

            ax.axvline(z_crit, color=COLORS["crit"], linestyle="--", linewidth=1.8, label=f"Critical value z = {z_crit:.2f}")

            ax.set_xlabel("Test Statistic", fontsize=12)
            ax.set_ylabel("Density", fontsize=12)
            ax.set_yticks([])
            ax.set_title("Type I & Type II Errors  —  How α and β Trade Off", fontsize=12)
            ax.legend(fontsize=9, loc="upper right")
            ax.set_xlim(-4, sep + 4)
            plt.tight_layout()
            plt.show()
            print(f"  α  (Type I error)  = {alpha:.2f}   ← probability of rejecting a true H₀")
            print(f"  β  (Type II error) ≈ {beta:.2f}   ← probability of missing a false H₀")
            print(f"  Power (1 – β)      ≈ {1 - beta:.2f}   ← probability of correctly rejecting H₀")

    sep_slider.observe(_draw, names="value")
    alpha_slider.observe(_draw, names="value")
    display(widgets.VBox([sep_slider, alpha_slider]), out)
    _draw()


# ── 3. p-Value on the Curve ──────────────────────────────────────────────────
def show_pvalue_visual(test_stat, tail, df=None, distribution="t"):
    """
    Plots where the test statistic falls on a t (or z) distribution
    and shades the corresponding p-value area.

    Parameters
    ----------
    test_stat    : float   – computed t or z statistic
    tail         : str     – "left", "right", or "two"
    df           : int     – degrees of freedom (None → standard normal)
    distribution : str     – "t" or "z"
    """
    use_t = (distribution == "t") and (df is not None)
    x = np.linspace(-5, 5, 600)
    y = stats.t.pdf(x, df) if use_t else stats.norm.pdf(x)
    dist_label = f"t (df={df})" if use_t else "Standard Normal (z)"

    # One-sided p-values must use the signed statistic (sf/cdf), not P(Z > |z|).
    if use_t:
        if tail == "two":
            p_val = 2 * stats.t.sf(abs(test_stat), df)
        elif tail == "right":
            p_val = stats.t.sf(test_stat, df)
        else:
            p_val = stats.t.cdf(test_stat, df)
    else:
        if tail == "two":
            p_val = 2 * stats.norm.sf(abs(test_stat))
        elif tail == "right":
            p_val = stats.norm.sf(test_stat)
        else:
            p_val = stats.norm.cdf(test_stat)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, y, color=COLORS["null"], linewidth=2.5, label=dist_label)

    if tail == "two":
        ax.fill_between(x, y, where=(x >=  abs(test_stat)), color=COLORS["pval"], alpha=0.55,
                        label=f"p-value = {p_val:.4f} (both tails)")
        ax.fill_between(x, y, where=(x <= -abs(test_stat)), color=COLORS["pval"], alpha=0.55)
        ax.axvline( abs(test_stat), color=COLORS["reject"], linestyle="--", linewidth=2)
        ax.axvline(-abs(test_stat), color=COLORS["reject"], linestyle="--", linewidth=2,
                   label=f"Test stat = ±{abs(test_stat):.3f}")
    elif tail == "right":
        ax.fill_between(x, y, where=(x >= test_stat), color=COLORS["pval"], alpha=0.55,
                        label=f"p-value = {p_val:.4f}")
        ax.axvline(test_stat, color=COLORS["reject"], linestyle="--", linewidth=2,
                   label=f"Test stat = {test_stat:.3f}")
    else:
        ax.fill_between(x, y, where=(x <= test_stat), color=COLORS["pval"], alpha=0.55,
                        label=f"p-value = {p_val:.4f}")
        ax.axvline(test_stat, color=COLORS["reject"], linestyle="--", linewidth=2,
                   label=f"Test stat = {test_stat:.3f}")

    ax.set_xlabel("Test Statistic", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_yticks([])
    ax.set_title(f"p-Value on the {dist_label} Distribution  ({tail}-tailed)", fontsize=12)
    ax.legend(fontsize=9)
    ax.set_xlim(-5, 5)
    plt.tight_layout()
    plt.show()
    return p_val


# ── 4.5 CDF/Tail Areas Visual ───────────────────────────────────────────────
def show_cdf_tail_visuals():
    """
    Interactive visual to explain CDF and tail areas.
    Displays left-tail, right-tail, and two-tail probabilities for
    a chosen observed statistic.
    """
    dist_drop = widgets.Dropdown(
        options=[("t distribution", "t"), ("Standard normal", "z")],
        value="t",
        description="Distribution:",
        style={"description_width": "initial"},
    )
    x_slider = widgets.FloatSlider(
        value=1.2, min=-3.5, max=3.5, step=0.1,
        description="Observed stat:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="420px"),
    )
    df_slider = widgets.IntSlider(
        value=20, min=2, max=100, step=1,
        description="df (t only):",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="420px"),
    )
    out = widgets.Output()

    def _draw(change=None):
        with out:
            clear_output(wait=True)
            dist = dist_drop.value
            x0 = x_slider.value
            df = df_slider.value

            x = np.linspace(-4.5, 4.5, 700)
            if dist == "t":
                y = stats.t.pdf(x, df)
                cdf_x0 = stats.t.cdf(x0, df)
                cdf_abs = stats.t.cdf(abs(x0), df)
                label = f"t (df={df})"
            else:
                y = stats.norm.pdf(x)
                cdf_x0 = stats.norm.cdf(x0)
                cdf_abs = stats.norm.cdf(abs(x0))
                label = "z"

            left_area = cdf_x0
            right_area = 1 - cdf_x0
            two_area = 2 * (1 - cdf_abs)

            fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)
            titles = [
                fr"Left tail: CDF = $P(X \leq x_0) = {left_area:.4f}$",
                fr"Right tail: $P(X > x_0) = 1 - \mathrm{{CDF}} = {right_area:.4f}$",
                fr"Two-tailed: $2(1-\mathrm{{CDF}}(|x_0|)) = {two_area:.4f}$",
            ]

            # Left tail
            axes[0].plot(x, y, color=COLORS["null"], linewidth=2)
            axes[0].fill_between(x, y, where=(x <= x0), color=COLORS["pval"], alpha=0.55)
            axes[0].axvline(x0, color=COLORS["reject"], linestyle="--", linewidth=2)
            axes[0].set_title(titles[0], fontsize=10)

            # Right tail
            axes[1].plot(x, y, color=COLORS["null"], linewidth=2)
            axes[1].fill_between(x, y, where=(x >= x0), color=COLORS["pval"], alpha=0.55)
            axes[1].axvline(x0, color=COLORS["reject"], linestyle="--", linewidth=2)
            axes[1].set_title(titles[1], fontsize=10)

            # Two tails
            axes[2].plot(x, y, color=COLORS["null"], linewidth=2)
            axes[2].fill_between(x, y, where=(x <= -abs(x0)), color=COLORS["pval"], alpha=0.55)
            axes[2].fill_between(x, y, where=(x >= abs(x0)), color=COLORS["pval"], alpha=0.55)
            axes[2].axvline(-abs(x0), color=COLORS["reject"], linestyle="--", linewidth=2)
            axes[2].axvline(abs(x0), color=COLORS["reject"], linestyle="--", linewidth=2)
            axes[2].set_title(titles[2], fontsize=10)

            for ax in axes:
                ax.set_xlim(-4.5, 4.5)
                ax.set_yticks([])
                ax.set_xlabel(fr"Observed stat $x_0$ = {x0:.2f}")
            axes[0].set_ylabel("Density")
            fig.suptitle(f"CDF and Tail Areas on {label} distribution", fontsize=12, y=1.03)
            plt.tight_layout()
            plt.show()

    dist_drop.observe(_draw, names="value")
    x_slider.observe(_draw, names="value")
    df_slider.observe(_draw, names="value")
    display(widgets.VBox([dist_drop, x_slider, df_slider]), out)
    _draw()


# ── 4. Interactive One-Sample t-Test ────────────────────────────────────────
def show_ttest_sandbox(nba_clean):
    """
    Lets students pick a numeric column, a hypothesized mean, and a tail.
    Draws the t-distribution with p-value shaded.
    """
    numeric_cols = nba_clean.select_dtypes(include="number").columns.tolist()

    col_drop = widgets.Dropdown(
        options=numeric_cols,
        value="Salary" if "Salary" in numeric_cols else numeric_cols[0],
        description="Column:",
        style={"description_width": "initial"},
    )
    # Sync .value while typing so "Run" matches what's in the box (not last Enter/blur).
    mu0_box = _float_text(
        value=5_000_000 if "Salary" in numeric_cols else 10.0,
        description="H₀ mean (μ₀):",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="280px"),
    )
    tail_drop = widgets.Dropdown(
        options=["two", "left", "right"],
        value="two",
        description="Tail:",
        style={"description_width": "initial"},
    )
    alpha_box = _float_text(
        value=0.05,
        description="α:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="180px"),
    )
    run_btn = widgets.Button(description="Run t-Test", button_style="primary")
    out = widgets.Output()

    def _run(btn):
        with out:
            clear_output(wait=True)
            col   = col_drop.value
            mu0   = mu0_box.value
            tail  = tail_drop.value
            alpha = alpha_box.value
            data  = nba_clean[col].dropna()
            n     = len(data)
            x_bar = data.mean()
            s     = data.std(ddof=1)
            se    = s / np.sqrt(n)
            t_stat = (x_bar - mu0) / se
            df_val = n - 1

            if tail == "two":
                p_val = 2 * (1 - stats.t.cdf(abs(t_stat), df_val))
            elif tail == "right":
                p_val = 1 - stats.t.cdf(t_stat, df_val)
            else:
                p_val = stats.t.cdf(t_stat, df_val)

            # Draw
            x = np.linspace(-4.5, 4.5, 600)
            y = stats.t.pdf(x, df_val)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(x, y, color=COLORS["null"], linewidth=2.3,
                    label=f"t-distribution (df={df_val})")

            t_plot = min(max(t_stat, -4.5), 4.5)
            if tail == "two":
                ax.fill_between(x, y, where=(x >=  abs(t_plot)), color=COLORS["pval"], alpha=0.55)
                ax.fill_between(x, y, where=(x <= -abs(t_plot)), color=COLORS["pval"], alpha=0.55,
                                label=f"p-value = {p_val:.4f}")
                ax.axvline( abs(t_plot), color=COLORS["reject"], linestyle="--", linewidth=2)
                ax.axvline(-abs(t_plot), color=COLORS["reject"], linestyle="--", linewidth=2,
                           label=f"t = ±{t_stat:.3f}")
            elif tail == "right":
                ax.fill_between(x, y, where=(x >= t_plot), color=COLORS["pval"], alpha=0.55,
                                label=f"p-value = {p_val:.4f}")
                ax.axvline(t_plot, color=COLORS["reject"], linestyle="--", linewidth=2,
                           label=f"t = {t_stat:.3f}")
            else:
                ax.fill_between(x, y, where=(x <= t_plot), color=COLORS["pval"], alpha=0.55,
                                label=f"p-value = {p_val:.4f}")
                ax.axvline(t_plot, color=COLORS["reject"], linestyle="--", linewidth=2,
                           label=f"t = {t_stat:.3f}")

            reject = p_val < alpha
            decision_plain = "Reject H0" if reject else "Fail to reject H0"
            decision_title = r"Reject $H_0$" if reject else r"Fail to reject $H_0$"
            ax.set_title(
                rf"{col}: $H_0$: $\mu = {mu0:,.1f}$  $\rightarrow$  {decision_title}",
                fontsize=12,
            )
            ax.set_xlabel("t statistic", fontsize=12)
            ax.set_yticks([])
            ax.legend(fontsize=9)
            plt.tight_layout()
            plt.show()

            print(f"  Sample mean   x̄  = {x_bar:,.4f}")
            print(f"  Sample std    s  = {s:,.4f}")
            print(f"  Sample size   n  = {n}")
            print(f"  t statistic      = {t_stat:.4f}")
            print(f"  p-value          = {p_val:.4f}")
            print(f"  α                = {alpha}")
            print(f"  Decision         : {decision_plain}")

    run_btn.on_click(_run)
    display(
        widgets.HBox([col_drop, tail_drop]),
        widgets.HBox([mu0_box, alpha_box]),
        run_btn, out,
    )


# ── 5. Interactive Proportion z-Test ────────────────────────────────────────
def show_proportion_sandbox(nba_clean):
    """
    Students pick a numeric column and a threshold to define 'success',
    then test whether the true proportion equals a claimed value p0.
    """
    numeric_cols = nba_clean.select_dtypes(include="number").columns.tolist()

    col_drop = widgets.Dropdown(
        options=numeric_cols,
        value="Points" if "Points" in numeric_cols else numeric_cols[0],
        description="Column:",
        style={"description_width": "initial"},
    )
    threshold_box = _float_text(
        value=15.0,
        description="'Success' if ≥:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="240px"),
    )
    p0_box = _float_text(
        value=0.30,
        description="H₀ proportion (p₀):",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="260px"),
    )
    tail_drop = widgets.Dropdown(
        options=["two", "left", "right"],
        value="two",
        description="Tail:",
        style={"description_width": "initial"},
    )
    alpha_box = _float_text(
        value=0.05,
        description="α:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="180px"),
    )
    run_btn = widgets.Button(description="Run Proportion z-Test", button_style="primary")
    out = widgets.Output()

    def _run(btn):
        with out:
            clear_output(wait=True)
            col       = col_drop.value
            threshold = threshold_box.value
            p0        = p0_box.value
            tail      = tail_drop.value
            alpha     = alpha_box.value
            data      = nba_clean[col].dropna()
            n         = len(data)
            x_succ    = (data >= threshold).sum()
            p_hat     = x_succ / n
            se        = np.sqrt(p0 * (1 - p0) / n)
            z_stat    = (p_hat - p0) / se

            if tail == "two":
                p_val = 2 * (1 - stats.norm.cdf(abs(z_stat)))
            elif tail == "right":
                p_val = 1 - stats.norm.cdf(z_stat)
            else:
                p_val = stats.norm.cdf(z_stat)

            x = np.linspace(-4.5, 4.5, 600)
            y = stats.norm.pdf(x)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(x, y, color=COLORS["null"], linewidth=2.3, label="Standard Normal (z)")

            z_plot = min(max(z_stat, -4.5), 4.5)
            if tail == "two":
                ax.fill_between(x, y, where=(x >=  abs(z_plot)), color=COLORS["pval"], alpha=0.55)
                ax.fill_between(x, y, where=(x <= -abs(z_plot)), color=COLORS["pval"], alpha=0.55,
                                label=f"p-value = {p_val:.4f}")
                ax.axvline( abs(z_plot), color=COLORS["reject"], linestyle="--", linewidth=2)
                ax.axvline(-abs(z_plot), color=COLORS["reject"], linestyle="--", linewidth=2,
                           label=f"z = ±{z_stat:.3f}")
            elif tail == "right":
                ax.fill_between(x, y, where=(x >= z_plot), color=COLORS["pval"], alpha=0.55,
                                label=f"p-value = {p_val:.4f}")
                ax.axvline(z_plot, color=COLORS["reject"], linestyle="--", linewidth=2,
                           label=f"z = {z_stat:.3f}")
            else:
                ax.fill_between(x, y, where=(x <= z_plot), color=COLORS["pval"], alpha=0.55,
                                label=f"p-value = {p_val:.4f}")
                ax.axvline(z_plot, color=COLORS["reject"], linestyle="--", linewidth=2,
                           label=f"z = {z_stat:.3f}")

            reject = p_val < alpha
            decision_plain = "Reject H0" if reject else "Fail to reject H0"
            decision_title = r"Reject $H_0$" if reject else r"Fail to reject $H_0$"
            ax.set_title(
                rf"Proportion of {col} $\geq$ {threshold}: $H_0$: $p = {p0}$  $\rightarrow$  {decision_title}",
                fontsize=11,
            )
            ax.set_xlabel("z statistic", fontsize=12)
            ax.set_yticks([])
            ax.legend(fontsize=9)
            plt.tight_layout()
            plt.show()

            print(f"  Successes ({col} ≥ {threshold}): {x_succ} out of {n}")
            print(f"  Sample proportion p̂ = {p_hat:.4f}")
            print(f"  H₀ proportion    p₀ = {p0}")
            print(f"  z statistic          = {z_stat:.4f}")
            print(f"  p-value              = {p_val:.4f}")
            print(f"  α                    = {alpha}")
            print(f"  Decision             : {decision_plain}")

    run_btn.on_click(_run)
    display(
        widgets.HBox([col_drop, tail_drop]),
        widgets.HBox([threshold_box, p0_box, alpha_box]),
        run_btn, out,
    )
