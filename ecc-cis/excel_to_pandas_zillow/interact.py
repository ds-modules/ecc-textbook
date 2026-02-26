"""
Interactive widgets for Excel_to_Pandas_Zillow.ipynb.
Used for: explore data, filter markets, pivot table builder, metro trends chart.
"""

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
        import matplotlib.pyplot as plt
    except ImportError:
        display(HTML("<p>matplotlib is required for metro_trends_widget. Install with: pip install matplotlib</p>"))
        return

    metros = sorted(df[name_col].dropna().unique().astype(str).tolist())
    if len(metros) > 100:
        metros = metros[:100]  # limit dropdown size

    def _plot(metro_choices):
        if not metro_choices:
            display(HTML("<p>Select at least one metro.</p>"))
            return
        sub = df[df[name_col].astype(str).isin(metro_choices)].copy()
        if sub.empty:
            display(HTML("<p>No data for selected metros.</p>"))
            return
        sub[date_col] = pd.to_datetime(sub[date_col])
        pivot = sub.pivot_table(index=date_col, columns=name_col, values=value_col)
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot.plot(ax=ax, linewidth=2)
        ax.set_title("Home Value Over Time by Metro", fontsize=14, fontweight="bold")
        ax.set_xlabel(date_col)
        ax.set_ylabel(value_col)
        ax.legend(title=name_col, fontsize=8)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # Multi-select for metros; interact doesn't support SelectMultiple easily, so use dropdown with a few metros
    # or we use a single dropdown that allows multiple via a tuple. ipywidgets SelectMultiple in a Box.
    metro_selector = widgets.SelectMultiple(
        options=metros,
        value=[metros[0]] if metros else [],
        description="Metros:",
        rows=min(12, len(metros)),
    )

    def _on_change(change=None):
        out.clear_output()
        with out:
            _plot(list(metro_selector.value))

    out = widgets.Output()
    metro_selector.observe(_on_change, names="value")
    display(widgets.VBox([widgets.HTML("<p>Select one or more metros to compare over time:</p>"), metro_selector, out]))
    _on_change()
