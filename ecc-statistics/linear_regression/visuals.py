"""
Interactive visuals for the linear regression notebook.
These helpers keep widget/plot logic out of student exercise cells.
"""

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output


def show_interactive_correlation():
    """Interactive visual for correlation direction and strength."""
    r_slider = widgets.FloatSlider(
        value=0.6,
        min=-0.95,
        max=0.95,
        step=0.05,
        description="Target r:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="420px"),
    )
    n_slider = widgets.IntSlider(
        value=120,
        min=30,
        max=300,
        step=10,
        description="Sample size:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="420px"),
    )
    regen_btn = widgets.Button(description="Generate New Sample", button_style="info")
    out = widgets.Output()

    def draw(*_):
        with out:
            clear_output(wait=True)
            target_r = r_slider.value
            n = n_slider.value

            xv = np.random.randn(n)
            yv = target_r * xv + np.sqrt(1 - target_r**2) * np.random.randn(n)
            r_sample, _ = stats.pearsonr(xv, yv)

            fig, ax = plt.subplots(figsize=(7, 5))
            ax.scatter(xv, yv, alpha=0.45, s=32, color="steelblue", edgecolors="white")
            ax.set_title(f"Target r = {target_r:.2f} | Sample r = {r_sample:.2f}", fontsize=13)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.axhline(0, color="gray", linewidth=0.8, alpha=0.5)
            ax.axvline(0, color="gray", linewidth=0.8, alpha=0.5)
            plt.tight_layout()
            plt.show()

    r_slider.observe(draw, names="value")
    n_slider.observe(draw, names="value")
    regen_btn.on_click(draw)

    display(widgets.VBox([r_slider, n_slider, regen_btn, out]))
    draw()


def show_interactive_line_tuner(
    x,
    y,
    a,
    b,
    x_range,
    y_hat,
    *,
    x_label="Points Per Game",
    y_label="Salary",
    money_yaxis=True,
):
    """Interactive visual to compare a user-selected line with least-squares."""
    y_spread = float(np.std(y))
    b_try = widgets.FloatSlider(
        value=float(b),
        min=float(b * 0.2),
        max=float(b * 1.8),
        step=max(float(abs(b) * 0.02), 1e-6),
        description="Your slope b:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="500px"),
    )
    if money_yaxis:
        a_try = widgets.FloatSlider(
            value=float(a),
            min=float(a - 8_000_000),
            max=float(a + 8_000_000),
            step=100_000,
            description="Your intercept a:",
            style={"description_width": "initial"},
            layout=widgets.Layout(width="500px"),
        )
    else:
        a_try = widgets.FloatSlider(
            value=float(a),
            min=float(a - 4 * y_spread),
            max=float(a + 4 * y_spread),
            step=max(y_spread / 80, 0.05),
            description="Your intercept a:",
            style={"description_width": "initial"},
            layout=widgets.Layout(width="500px"),
        )
    out = widgets.Output()

    def draw(*_):
        with out:
            clear_output(wait=True)
            b_user = b_try.value
            a_user = a_try.value

            y_user = a_user + b_user * x
            y_best = a + b * x
            sse_user = float(np.sum((y - y_user) ** 2))
            sse_best = float(np.sum((y - y_best) ** 2))

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(x, y, alpha=0.3, color="steelblue", edgecolors="white", s=55)
            ax.plot(x_range, y_hat, color="crimson", linewidth=2.5, label="Best-fit line")
            ax.plot(
                x_range,
                a_user + b_user * x_range,
                color="darkorange",
                linewidth=2,
                linestyle="--",
                label="Your line",
            )
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_title("Compare Your Line vs Least-Squares Line")
            if money_yaxis:
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v/1e6:.1f}M"))
            ax.legend()
            plt.tight_layout()
            plt.show()

            print(f"Your SSE     : {sse_user:,.2e}")
            print(f"Best-fit SSE : {sse_best:,.2e}")
            print("Tip: move sliders to try to make Your SSE as small as possible.")

    b_try.observe(draw, names="value")
    a_try.observe(draw, names="value")

    display(widgets.VBox([b_try, a_try, out]))
    draw()


def show_prediction_slider(
    x,
    y,
    a,
    b,
    x_range,
    y_hat,
    *,
    x_label="Points Per Game",
    y_label="Salary",
    money_yaxis=True,
    slider_description="Points per game:",
):
    """Interactive visual for prediction from a chosen x value (salary or plain y)."""
    slider = widgets.FloatSlider(
        value=round(float(x.mean()), 1),
        min=round(float(x.min()), 1),
        max=round(float(x.max()), 1),
        step=0.1,
        description=slider_description,
        style={"description_width": "initial"},
        layout=widgets.Layout(width="480px"),
    )
    out = widgets.Output()

    def draw(*_):
        with out:
            clear_output(wait=True)
            x_in = slider.value
            y_pred = a + b * x_in

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(x, y, alpha=0.3, color="steelblue", edgecolors="white", s=55)
            ax.plot(x_range, y_hat, color="crimson", linewidth=2, label="Regression line")
            ax.axvline(x=x_in, color="orange", linestyle="--", alpha=0.6)
            pred_lbl = f"Predicted: ${y_pred/1e6:.2f}M" if money_yaxis else f"Predicted: {y_pred:.1f}"
            ax.scatter([x_in], [y_pred], color="orange", s=200, zorder=5, label=pred_lbl)
            ann = f"  ${y_pred/1e6:.2f}M" if money_yaxis else f"  {y_pred:.1f}"
            ax.annotate(
                ann,
                xy=(x_in, y_pred),
                fontsize=12,
                color="darkorange",
                xytext=(x_in + 0.3, y_pred),
            )
            ax.set_xlabel(x_label, fontsize=12)
            ax.set_ylabel(y_label, fontsize=12)
            if money_yaxis:
                ax.set_title(f"Predicted Salary for {x_in:.1f} points/game", fontsize=13)
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v/1e6:.1f}M"))
            else:
                ax.set_title(f"Predicted {y_label} for {x_label.lower()} = {x_in:.1f}", fontsize=13)
            ax.legend(fontsize=11)
            plt.tight_layout()
            plt.show()

    slider.observe(draw, names="value")
    display(slider, out)
    draw()


def show_sandbox_regression(nba_clean):
    """Interactive sandbox for any two numeric columns."""
    numeric_cols = nba_clean.select_dtypes(include="number").columns.tolist()
    x_drop = widgets.Dropdown(
        options=numeric_cols,
        value="AST" if "AST" in numeric_cols else numeric_cols[0],
        description="X variable:",
        style={"description_width": "initial"},
    )
    y_drop = widgets.Dropdown(
        options=numeric_cols,
        value="Salary" if "Salary" in numeric_cols else numeric_cols[1],
        description="Y variable:",
        style={"description_width": "initial"},
    )
    run_btn = widgets.Button(description="Run Regression", button_style="primary")
    out = widgets.Output()

    def run_sandbox(_):
        with out:
            clear_output(wait=True)
            col_x = x_drop.value
            col_y = y_drop.value

            if col_x == col_y:
                print("Please choose two different columns.")
                return

            data = nba_clean[[col_x, col_y]].dropna()
            sx, sy = data[col_x], data[col_y]

            r_sb, p_sb = stats.pearsonr(sx, sy)
            b_sb = r_sb * (sy.std() / sx.std())
            a_sb = sy.mean() - b_sb * sx.mean()

            x_rng = np.linspace(sx.min(), sx.max(), 200)
            y_rng = a_sb + b_sb * x_rng

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(sx, sy, alpha=0.4, color="mediumseagreen", edgecolors="white", s=60, label="Players")
            ax.plot(x_rng, y_rng, color="crimson", linewidth=2.5, label=f"r = {r_sb:.3f}  |  p = {p_sb:.2e}")
            ax.set_xlabel(col_x, fontsize=12)
            ax.set_ylabel(col_y, fontsize=12)
            ax.set_title(f"{col_x} vs. {col_y}", fontsize=14)
            ax.legend(fontsize=11)
            plt.tight_layout()
            plt.show()

            print(f"Slope     (b): {b_sb:.4f}")
            print(f"Intercept (a): {a_sb:.4f}")
            print(f"Equation     : y_hat = {a_sb:.2f} + {b_sb:.2f} * {col_x}")

    run_btn.on_click(run_sandbox)
    display(widgets.HBox([x_drop, y_drop]), run_btn, out)
