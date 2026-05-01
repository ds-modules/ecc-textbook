"""
Interactive widgets for Excel_to_Pandas_Zillow.ipynb.
Used for: explore data, filter markets, pivot table builder, metro trends chart.
"""

from io import BytesIO

import pandas as pd
import numpy as np
from IPython.display import display, HTML
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed


def explore_data_widget(df):
    """
    Interactive dropdown to explore a DataFrame: head(), tail(), shape, info(), describe(), columns.
    Call with the DataFrame to inspect (e.g. home_values).
    """
    if df is None or not isinstance(df, pd.DataFrame):
        display(HTML("<p>Please pass a valid pandas DataFrame (e.g. <code>home_values</code>).</p>"))
        return

    def _explore(method):
        if method == "head() — first 5 rows":
            print("df.head()")
            display(df.head())
        elif method == "tail() — last 5 rows":
            print("df.tail()")
            display(df.tail())
        elif method == "shape — (rows, columns)":
            print("df.shape")
            print(f"→ {df.shape[0]:,} rows × {df.shape[1]} columns")
        elif method == "info() — column types and non-null counts":
            print("df.info()")
            df.info()
        elif method == "describe() — summary statistics":
            print("df.describe()")
            display(df.describe())
        elif method == "columns — column names":
            print("df.columns")
            print(list(df.columns))

    interact(
        _explore,
        method=[
            "head() — first 5 rows",
            "tail() — last 5 rows",
            "shape — (rows, columns)",
            "info() — column types and non-null counts",
            "describe() — summary statistics",
            "columns — column names",
        ],
    )


def filter_markets_widget(df):
    """
    Interactive filter by state(s) and home value range.
    Expects DataFrame with StateName (or 'State') and HomeValue (or first numeric column used as value).
    """
    if df is None or not isinstance(df, pd.DataFrame):
        display(HTML("<p>Please pass a valid pandas DataFrame (e.g. <code>latest_home_values</code>).</p>"))
        return

    state_col = "StateName" if "StateName" in df.columns else "State" if "State" in df.columns else None
    value_col = "HomeValue" if "HomeValue" in df.columns else None
    if value_col is None:
        num_cols = df.select_dtypes(include=[np.number]).columns
        value_col = num_cols[0] if len(num_cols) else None

    if state_col is None or value_col is None:
        display(HTML("<p>DataFrame must have a state column (StateName or State) and a value column (e.g. HomeValue).</p>"))
        return

    states = ["All"] + sorted(df[state_col].dropna().unique().astype(str).tolist())
    v_min = int(df[value_col].min()) if df[value_col].notna().any() else 0
    v_max = int(df[value_col].max()) if df[value_col].notna().any() else 1_000_000
    step = max(10000, (v_max - v_min) // 50)

    def _filter(state_choice, min_val, max_val):
        f = df.copy()
        if state_choice != "All":
            f = f[f[state_col].astype(str) == state_choice]
        f = f[(f[value_col] >= min_val) & (f[value_col] <= max_val)]
        display(HTML(f"<p><b>Showing {len(f)} of {len(df)} rows</b></p>"))
        display(f.head(20))

    interact(
        _filter,
        state_choice=states,
        min_val=widgets.IntSlider(min=v_min, max=v_max, step=step, value=v_min, description="Min value:"),
        max_val=widgets.IntSlider(min=v_min, max=v_max, step=step, value=v_max, description="Max value:"),
    )


def pivot_table_widget(df):
    """
    Interactive pivot table builder: choose index, columns, values, and aggfunc.
    Expects DataFrame with at least one numeric column (e.g. HomeValue) and categorical columns (e.g. MarketTier, StateName).
    """
    if df is None or not isinstance(df, pd.DataFrame):
        display(HTML("<p>Please pass a valid pandas DataFrame (e.g. <code>home_values_pivot</code>).</p>"))
        return

    object_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not object_cols or not numeric_cols:
        display(HTML("<p>DataFrame needs both categorical and numeric columns for a pivot.</p>"))
        return

    index_options = ["(none)"] + object_cols
    col_options = ["(none)"] + object_cols
    value_options = numeric_cols
    agg_options = ["mean", "median", "sum", "count", "min", "max"]

    def _pivot(index_col, columns_col, values_col, agg_func):
        if index_col == "(none)" or values_col is None:
            display(HTML("<p>Choose at least <b>index</b> and <b>values</b>.</p>"))
            return
        try:
            kwargs = dict(values=values_col, index=index_col, aggfunc=agg_func)
            if columns_col != "(none)":
                kwargs["columns"] = columns_col
                kwargs["fill_value"] = 0
            pt = df.pivot_table(**kwargs)
            if hasattr(pt, "round"):
                pt = pt.round(0)
            display(HTML("<p><b>pivot_table result:</b></p>"))
            display(pt)
        except Exception as e:
            display(HTML(f"<p style='color:red;'>Error: {e}</p>"))

    interact(
        _pivot,
        index_col=index_options,
        columns_col=col_options,
        values_col=value_options,
        agg_func=agg_options,
    )


def metro_trends_widget(df):
    """
    Interactive line chart: pick metros and plot HomeValue (or first numeric column) over Date.
    Expects long-format DataFrame with Date, RegionName (or similar), and a value column (e.g. HomeValue).
    """
    if df is None or not isinstance(df, pd.DataFrame):
        display(HTML("<p>Please pass a valid pandas DataFrame (e.g. <code>home_values</code>).</p>"))
        return

    date_col = "Date" if "Date" in df.columns else None
    if date_col is None:
        for c in df.columns:
            if "date" in c.lower() or c == "Month":
                date_col = c
                break
    name_col = "RegionName" if "RegionName" in df.columns else "Region" if "Region" in df.columns else None
    if name_col is None:
        for c in ["Metro_Name", "Metro", "Name"]:
            if c in df.columns:
                name_col = c
                break
    value_col = "HomeValue" if "HomeValue" in df.columns else None
    if value_col is None:
        num_cols = df.select_dtypes(include=[np.number]).columns
        value_col = num_cols[0] if len(num_cols) else None

    if not all([date_col, name_col, value_col]):
        display(HTML("<p>DataFrame needs Date, RegionName (or similar), and a value column (e.g. HomeValue).</p>"))
        return

    try:
        from matplotlib.figure import Figure
    except ImportError:
        display(HTML("<p>matplotlib is required for metro_trends_widget. Install with: pip install matplotlib</p>"))
        return

    metros = sorted(df[name_col].dropna().unique().astype(str).tolist())

    # Selection persists across search/filter; widget shows only the subset visible in the current filter.
    state = {
        "accumulated": {metros[0]} if metros else set(),
        "last_rendered": None,
    }
    _suppress_observer = False

    def _chart_png_bytes(metro_choices):
        """Return PNG bytes for a single chart image (no display(); avoids duplicate rich-output renders)."""
        fig = Figure(figsize=(12, 6))
        ax = fig.subplots()
        if not metro_choices:
            ax.text(0.5, 0.5, "Select at least one metro.", ha="center", va="center", fontsize=12)
            ax.axis("off")
        else:
            sub = df[df[name_col].astype(str).isin(metro_choices)].copy()
            if sub.empty:
                ax.text(0.5, 0.5, "No data for selected metros.", ha="center", va="center", fontsize=12)
                ax.axis("off")
            else:
                sub[date_col] = pd.to_datetime(sub[date_col])
                pivot = sub.pivot_table(index=date_col, columns=name_col, values=value_col)
                pivot.plot(ax=ax, linewidth=2)
                ax.set_title("Home Value Over Time by Metro", fontsize=14, fontweight="bold")
                ax.set_xlabel(date_col)
                ax.set_ylabel(value_col)
                ax.legend(title=name_col, fontsize=8)
                ax.grid(True, alpha=0.3)
                for label in ax.get_xticklabels():
                    label.set_rotation(45)
                fig.tight_layout()
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", dpi=110)
        return buf.getvalue()

    # Keep all metros available; use search to narrow the list (selection still accumulates).
    metro_selector = widgets.SelectMultiple(
        options=metros,
        value=(metros[0],) if metros else (),
        description="Metros:",
        rows=min(12, len(metros)),
    )
    search_box = widgets.Text(
        value="",
        placeholder="Type to filter metros (e.g., Dallas or TX)",
        description="Search:",
    )
    comparison_status = widgets.HTML()
    # One static image widget — update `.value` with PNG bytes only (no stacked figures in VS Code / Jupyter).
    chart_image = widgets.Image(
        format="png",
        layout=widgets.Layout(max_width="100%", border="0"),
    )

    def _render(force=False):
        acc = sorted(state["accumulated"])
        acc_key = tuple(acc)
        # Guard against duplicate callback chains that request the same draw.
        if not force and state["last_rendered"] == acc_key:
            return
        state["last_rendered"] = acc_key
        preview = ", ".join(acc[:12])
        if len(acc) > 12:
            preview += " …"
        comparison_status.value = (
            f"<p><b>Comparing {len(acc)} metro(s):</b> {preview}</p>"
            if acc
            else "<p><b>No metros selected.</b></p>"
        )
        chart_image.value = _chart_png_bytes(acc)

    def _on_selector_change(change):
        nonlocal _suppress_observer
        if _suppress_observer:
            return
        opts = set(metro_selector.options)
        new = set(metro_selector.value)
        # Replace selection for metros currently listed; keep metros not in this filter.
        state["accumulated"] = (state["accumulated"] - opts) | new
        _render()

    def _on_search(change=None):
        nonlocal _suppress_observer
        query = search_box.value.strip().lower()
        filtered = [m for m in metros if query in m.lower()] if query else metros
        visible = tuple(sorted(m for m in state["accumulated"] if m in filtered))
        _suppress_observer = True
        try:
            metro_selector.options = filtered or []
            metro_selector.value = visible
        finally:
            _suppress_observer = False
        _render()

    metro_selector.observe(_on_selector_change, names="value")
    search_box.observe(_on_search, names="value")
    help_text = widgets.HTML(
        "<p>Search narrows the list below. Selections <b>stay</b> when you change the search "
        "(use the status line to see every metro in the chart).<br>"
        "In the list: Cmd-click (Mac) or Ctrl-click (Windows/Linux) to select multiple.</p>"
    )
    display(widgets.VBox([help_text, search_box, metro_selector, comparison_status, chart_image]))
    _render(force=True)
