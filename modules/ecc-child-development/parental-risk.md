---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.18.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Exploring Prenatal Risk Factors Across Different States and Over Time Through PRAMS Data
<br>

**Estimated Time:** 30-45 minutes <br>
**Notebook Developed By:** Lan Dinh <br>

Welcome! In this notebook, we will use the Pregnancy Risk Assessment Monitoring System (PRAMS) to investigate various factors that influence pregnancy health across different states in America. You won't have to be answering any coding questions yourself in the notebooks for this class, but instead you'll be asked to answer some short-answer questions as we explore and visualize the data. Any questions you see in **yellow-shaded sections** below are questions you'll be answering! Additionally, there will be some optional questions in **blue-shade sections** that help you follow along the notebook and understand the context. We hope this notebook serves as an engaging and informative introduction to the critical role of data collection in understanding prenatal development.

+++

## Learning Outcomes

In this notebook, you will learn about:
- How to utilize PRAMS data to study various factors influencing prenatal health across different states in the U.S.
- How to visualize and interpret trends in maternal health indicators over time using geographic maps and bar charts.

## Table of Contents
1. Prenatal Development: Teratogen and Maternal Factors <br>
1. Data Background
1. Data Exploration <br>
1. Visualizations <br>
>4.1. Geographic Map <br>
>4.2. Trends Over Time: Visualizing Changes in Health Indicators using Tables <br>
>4.3. Trends Over Time: Visualizing Changes in Health Indicators using Bar Charts <br>

+++

As some quick reminders, you will not be expected or required to do any coding yourself in this notebook! The only questions you will be answering are some short-answer questions based on the data and visualizations. These questions that you will be answering are located in the yellow-shaded boxes throughout the notebook. Along with this, for any code cells that say "`## Run this cell`" at the top, be sure to run them so you can properly see the data tables and visualizations!

**Note: To run a cell, first move your cursor over it and click once. After that, press `Ctrl + Enter` on your keyboard.**

+++

------------------
## Run the cell below to import all our required materials for this notebook!

```{code-cell} ipython3
## Run this cell
!pip install openpyxl --upgrade
# Used for visualizations and interactions
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import ipywidgets as widgets
from ipywidgets import interact
from IPython.display import display
import plotly.express as px

# Numerical computation
import numpy as np
from numpy import NaN
from decimal import Decimal

# Manipulating data in form of series or dataframes
import pandas as pd

# Manipulating fields that are date or time
import datetime
from datetime import time
```

-------------
## 1. Prenatal Development: Teratogen and Maternal Factors<a id='0'></a>

+++

[First few chapters in Intro to child development class](https://bookdown.org/nathalieyuen/understanding-the-whole-child/)

+++

-------------
## 2. Data Background<a id='0'></a>

+++

The PRAMS (Pregnancy Risk Assessment Monitoring System) data on maternal and child health indicators for 2016-2021 provides detailed information on various health measures aggregated by site. This includes statistics on prenatal care, breastfeeding, maternal smoking, and infant sleep practices, among other topics. These indicators help public health officials, researchers, and policymakers improve maternal and infant health programs. The data is available in standard and accessible formats for each year from 2016 to 2021.

For more detailed information, you can visit the [PRAMS MCH Indicators page](https://www.cdc.gov/prams/php/data-research/mch-indicators-by-site.html).

+++

-------------
## 3. Data Exploration<a id='0'></a>

+++

In this section, we will load and preprocess the PRAMS data for the years 2016 to 2021. Run the two cells below by clicking on the code cell and press `Ctrl + Enter`

```{code-cell} ipython3
## Run this cell
def preprocess(df):
    indices = [0,3]
    for i in range(1,42):
        idx = indices[-1]
        indices.append(idx+5)
    col_indices = np.array(indices[1:])-2
    columns = np.append(np.array(['Site Name']),df.iloc[0,col_indices].values)
    df = df.iloc[:,indices]
    df.columns = columns
    return df.drop([0,1]).drop(df.tail(8).index).set_index(['Site Name']).iloc[:,[0,1,2,3,4,5,6,7,8,9,10,13,14,15,17,19]]

filepath = "./PRAMS-MCH-Indicators-2016-2021.xlsx"
data_2016 = preprocess(pd.read_excel(filepath, sheet_name=0))
data_2017 = preprocess(pd.read_excel(filepath, sheet_name=1))
data_2018 = preprocess(pd.read_excel(filepath, sheet_name=2))
data_2019 = preprocess(pd.read_excel(filepath, sheet_name=3))
data_2020 = preprocess(pd.read_excel(filepath, sheet_name=4))
data_2021 = preprocess(pd.read_excel(filepath, sheet_name=5))    
common_idx = data_2016.index.intersection(data_2017.index).intersection(data_2018.index)\
                        .intersection(data_2019.index).intersection(data_2020.index)\
                        .intersection(data_2021.index)
sites_list = list(common_idx)  
```

```{code-cell} ipython3
## Run this cell
data_2019.head()
```

The table above shows various health indicators for pregnant women across different states in 2019. Each row represents a state, and each column represents a different health indicator. The units in each cell are percentages (%), indicating the proportion of women reporting each behavior or condition. In addition, the top row labeled `Sites aggregated*` provides average percentages across all sites. The table shows only the first few rows to give a general idea, omitting unnecessary parts to save space.

+++

Next, run the two cells below. They will provide a list of all indicators and sites we will focus on for the rest of the notebook.

```{code-cell} ipython3
## List of variables 
data_2016.columns
```

```{code-cell} ipython3
## List of avaiable sites
sites_list
```

<!-- BEGIN QUESTION -->
<div class="alert alert-warning">
    <h2>Question 1:</h2>
    <p>
        Based on the table above and the chapter <code>2.2. Prenatal Development</code>, discuss how this data aligns with the concepts of prenatal development and teratogens covered in the chapter. Consider how you use this data to improve prenatal care.
    </p>
 
</div>

+++

*Type your answer here. Double-click to edit this cell and replace this text with your answer. Run this cell to proceed when finished.*

+++

-------------
## 4. Visualizations <a id='0'></a>

+++

In this section, we will create visualizations to better understand the PRAMS data across different states and over time. These visualizations will help us identify trends and patterns in maternal health indicators, and how they vary geographically and temporally.

+++

## 4.1. Geographic Map

+++

In this subsection, we will create a geographic map to visualize the distribution of various health indicators across different states. This map allows us to see how specific prenatal and postpartum behaviors and conditions vary geographically. By selecting different years and variables, we can observe trends and identify regions with higher or lower percentages for certain health indicators. Run the code cell below to genarate an interactive geographic map. 

```{code-cell} ipython3
## Run this cell
def plot_map(year, variable):
    state_to_code = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}
    data = globals()[f"data_{year}"]
    df = data.drop(index=['Sites aggregated*'])
    df['State'] = df.index.map(state_to_code)

    fig = px.choropleth(
        df,
        locations='State',  # Column in DataFrame containing state names or abbreviations
        locationmode="USA-states",  # Ensures state names are recognized correctly
        color= variable,  # Data column to use for coloring
        scope="usa",  # Focus map on the USA
        title='State Data Visualization')
    fig.show()
year_dropdown = widgets.Dropdown(
    options= range(2016,2022),
    description = 'Year: ',
    disable= False
)
var_dropdown = widgets.Dropdown(
    options= data_2016.columns,
    description = 'Variable: ',
    disabled = False
)

interact(plot_map, year= year_dropdown, variable=var_dropdown);
```

When you run the code, you will see a map of the United States with states colored according to the percentage values of the selected health indicator. Darker colors typically represent higher percentages, while lighter colors represent lower percentages. By hovering over a state, you can see the exact percentage for that indicator in that state for the selected year. A legend box next to the map explains the values represented by the different colors.

**Interacting with the Map:**

Use the `Year` dropdown menu to select the year you want to analyze.
Use the `Variable` dropdown menu to select the health indicator you are interested in.
For example, if you select `2019` and `Any cigarette smoking during the last 3 months of pregnancy` you might observe that some states have higher percentages of smoking during pregnancy than others. This can highlight areas where targeted public health interventions might be needed to reduce smoking rates during pregnancy.

**Note:**
There are missing data in several states due to limited available sites from PRAMS data. If a state does not have data for the selected year or variable, it will not be colored on the map.

+++

<!-- BEGIN QUESTION -->
<div class="alert alert-warning">
    <h2>Question 2:</h2>
    <p>
        <b>
            Using the interactive map, select the year <code>2020</code> and the variable <code>Began prenatal care in 1st trimester.</code> Observe and describe any patterns or trends in early prenatal care initiation across the states. Which regions have higher percentages of women beginning prenatal care in the first trimester, and how might this information help target public health resources and interventions to improve prenatal care access and outcomes?
        </b>
    </p>
</div>

+++

*Type your answer here. Double-click to edit this cell and replace this text with your answer. Run this cell to proceed when finished.*

+++

## 4.2.  Trends Over Time: Visualizing Changes in Health Indicators using Tables

+++

In this subsection, we will analyze how a single health indicator changes over time across different states. This allows us to identify trends and patterns in a selected maternal health indicator over multiple years. By selecting different variables, we can compare the changes and gain insights into the effectiveness of health interventions and policies over time.

Run the cell below.

```{code-cell} ipython3
## Run this cell
def variable_over_time(var):
    data_frames = [globals()[f"data_{year}"].loc[sites_list, var].rename(year) for year in range(2016, 2022)]
    data = pd.concat(data_frames, axis=1)
    # Transpose to get years as rows for plotting
    data = data.transpose()
    return data
var_dropdown = widgets.Dropdown(
    options= data_2016.columns,
    description = 'Variable: ',
    disabled = False
)

interact(variable_over_time, var=var_dropdown, selected_sites=sites_list);
```

The generated table displays the percentage values of the selected health indicator for the chosen states over the years 2016 to 2021. Each row represents a year, and each column represents the percentage value for a state. Use the `Variable` dropdown menu to select the health indicator you want to analyze. This format allows for easy comparison of trends over time.

+++

<!-- BEGIN QUESTION -->

<div class="alert alert-warning">
    <h2>Question 3:</h2>
    <p>
        <b>
            Using the generated table, compare the trends in "Self-reported depression during pregnancy" from 2016 to 2021 for Massachusetts and Louisiana. What differences do you observe between these two states over time, and how might these trends reflect the effectiveness of mental health interventions for pregnant women in each state?
        </b>
    </p>
</div>

+++

*Type your answer here. Double-click to edit this cell and replace this text with your answer. Run this cell to proceed when finished.*

+++

## 4.3. Trends Over Time: Visualizing Changes in Health Indicators using Bar Charts

+++

The table in section 4.2 is helpful but has some limitations. In this subsection, we will conduct the same analysis of a single variable over time across different sites by using bar charts. This visual representation will allow us to better identify trends and differences in maternal health indicators across various states over multiple years.

Run the code cell below.

```{code-cell} ipython3
## Run the cell 
# Create a dictionary of Checkbox widgets for each site
checkboxes = {site: widgets.Checkbox(value=(site == sites_list[0]), description=site) for site in sites_list}

# Function to bundle the checkboxes into a UI component
def create_checkbox_group(checkbox_dict):
    return widgets.VBox([checkbox for checkbox in checkbox_dict.values()])

checkbox_group = create_checkbox_group(checkboxes)

# Widget setup for variable selection
var_dropdown = widgets.Dropdown(
    options= data_2016.columns,
    description = 'Variable: ',
    disabled = False
)

# Button to trigger the plot
plot_button = widgets.Button(description='Plot Data')

# Output widget for the plots
output = widgets.Output()

def on_plot_button_clicked(b):
    with output:
        output.clear_output()
        # Filter selected sites based on the checkbox states
        selected_sites = [site for site, checkbox in checkboxes.items() if checkbox.value]
        
        if not selected_sites:
            print("Please select at least one site.")
            return
     
        data_frames = [globals()[f"data_{year}"].loc[selected_sites, var_dropdown.value].rename(year) for year in range(2016, 2022)]
        data = pd.concat(data_frames, axis=1)
        
        # Transpose to get years as rows for plotting
        data = data.transpose()
        
        # Plotting
        data.plot.bar(rot=0)
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
        plt.title(f"How \"{var_dropdown.value}\" Changes Over Time")
        plt.show()

plot_button.on_click(on_plot_button_clicked)

# Displaying the UI components
print("Please select site(s) and a variable, then click \'Plot Data\'")
display(widgets.VBox([checkbox_group, var_dropdown, plot_button, output]))
```

**Instructions:**

Use the checkboxes to select the `states` you want to compare.

Use the `Variable` dropdown menu to select the health indicator you want to analyze.

Click the `Plot Data` button to generate the bar chart showing the changes in the selected variable over time for the chosen states.

The bar charts generated will display the percentage values of the selected health indicator for the chosen states over the years 2016 to 2021. Each bar represents the percentage for a specific year, and each group of bars represents a different state. The x-axis shows the years, while the y-axis shows the percentage values. This visual format allows for easy comparison of trends and differences in the selected health indicator over time between the states. By analyzing these charts, you can observe how maternal health behaviors and conditions have changed and identify any significant trends or patterns.

+++

<!-- BEGIN QUESTION -->

<div class="alert alert-warning">
    <h2>Question 4:</h2>
    <p>
        <b>
            Using the interactive tool, select the variable <code>Obese (BMI ≥30 kg/m2)</code> and compare the trends from 2016 to 2021 for Colorado and Pennsylvania. What differences do you observe between these two states over time, and what might these trends suggest about the prevalence and management of obesity among pregnant women in each state?
        </b>
    </p>
</div>

+++

*Type your answer here. Double-click to edit this cell and replace this text with your answer. Run this cell to proceed when finished.*

+++

-------------
## Congratulations! You Have Completed the Notebook!<a id='0'></a>
