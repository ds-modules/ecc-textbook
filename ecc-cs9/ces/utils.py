import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
from IPython.display import display, clear_output

ces = pd.read_csv('cal_enviro_screen.csv')
colleges = pd.read_excel("colleges.xlsx")
ces_cc = pd.merge(ces, colleges, how='inner', left_on='ZIP', right_on='Zip')

# Drop unneeded columns
ces_cc_filtered = ces_cc.drop(labels=["Census Tract", "ZIP", "Longitude", "Latitude", "Zip", "EVDCode", "OPEID", "yrs"], axis=1).sort_index(axis=1)

# Filter numeric columns
numeric_cols = [col for col in ces_cc_filtered.columns if pd.api.types.is_numeric_dtype(ces_cc_filtered[col])]

# Create wider, styled buttons
buttons = [
    widgets.Button(
        description=col,
        layout=widgets.Layout(width='200px', height='40px', margin='4px 4px 4px 0'),
        style={'button_color': '#f0f0f0'}
    )
    for col in numeric_cols
]

# Output for plot
output = widgets.Output(layout=widgets.Layout(border='1px solid lightgray', padding='10px'))

# Click event handler
def on_button_clicked(b):
    col = b.description
    data = ces_cc_filtered[col].dropna()

    output.clear_output()
    with output:
        plt.figure(figsize=(7, 4))
        sns.histplot(data, kde=True, bins=10, color='salmon')
        plt.title(f'Histogram of {col} (Seaborn)')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# Attach handler to all buttons
for btn in buttons:
    btn.on_click(on_button_clicked)

# Organize buttons in a grid layout with scrolling if needed
button_grid = widgets.GridBox(
    buttons,
    layout=widgets.Layout(
        grid_template_columns='repeat(auto-fill, minmax(200px, 1fr))',
        overflow='auto',
        max_height='300px',
        padding='8px',
        border='1px solid lightgray'
    )
)

# Final layout
ui = widgets.VBox([
    widgets.HTML("<h3 style='margin-bottom:0;'>📊 Column Histogram Viewer</h3>"),
    widgets.HTML("<b>Select a Column:</b>"),
    button_grid,
    widgets.HTML("<hr>"),
    output
])