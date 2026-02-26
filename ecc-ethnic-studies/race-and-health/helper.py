from datascience import * # Loads functions from the datascience library into our current environment
import numpy as np # Loads numerical functions
import math, random # Loads math and random functions
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Latex, Markdown
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display
from ipywidgets import interact
import warnings
warnings.filterwarnings('ignore')

maternal= pd.read_csv('maternal_mortality_by_race_2018_2023.csv')

races= ['Non-Hispanic Black',	'Non-Hispanic White',	'Hispanic']

Uninsured_Rate= pd.read_csv('data-YAypV.csv')
Uninsured_Rate = Uninsured_Rate.rename(columns={'X.1': 'Year'}).drop(['AIAN', 'NHPI'], axis=1)
Uninsured_Rate

insurance= pd.read_csv('data-R8TpY.csv')
insurance= insurance.drop(['NHPI','AIAN'], axis=1).rename(columns={'Race': 'Insurance Type'})
insurance

def Uninsured():
    Merge = Uninsured_Rate.melt(id_vars="Year", 
                           var_name="Race", 
                           value_name="Insurance Rates")
    
    Merge["Insurance Rates"] = (
        Merge["Insurance Rates"]
        .replace('[%,]', '', regex=True)   # remove % and commas/semicolons
        .replace('', pd.NA)                # replace blanks with NaN
        .astype(float)                     # convert to numeric
    )
    
    
    # Plot using Plotly Express
    fig = px.line(Merge,
                  x="Year",
                  y="Insurance Rates",
                  color="Race",
                  markers=True,
                  title="Uninsured Rate by Race Over Time")
    
    fig.update_layout(template="plotly_white",
                      yaxis_title="Uninsured Rate (%)",
                      xaxis_title="Year")
    
    fig.show()
    
def Mortality_Rate_line():
    melted = maternal.melt(id_vars="Year", 
                       var_name="Race", 
                       value_name="Mortality Rate")
    fig = px.line(melted, 
              x="Year", 
              y="Mortality Rate", 
              color="Race", 
              markers=True,
              title="Maternal Mortality Rate by Race (2018–2023)")
    fig.update_layout(xaxis_title="Year",
                  yaxis_title="Rate (per 100,000 live births)",
                  template="plotly_white")
    fig.show()

def Mortality_Rate_bar():
    melted = maternal.melt(id_vars="Year", 
                       var_name="Race", 
                       value_name="Mortality Rate")
    fig = px.bar(melted,
                 x="Year",
                 y="Mortality Rate",
                 color="Race",
                 barmode="group",  # side-by-side bars
                 title="Maternal Mortality Rates by Race (2018–2023)")
    
    fig.update_layout(template="plotly_white",
                      xaxis_title="Year",
                      yaxis_title="Rate (per 100,000 live births)")
    
    fig.show()

def insurance_type():

    df = insurance

        
    for col in df.columns[1:]:
        df[col] = df[col].str.replace('%', '', regex=False).astype(float)
    
    # Melt into long format
    df_melted = df.melt(id_vars="Insurance Type", 
                        var_name="Race", 
                        value_name="Percent")
    
    # Plot stacked bar chart: one bar per race, stacked by insurance type
    fig = px.bar(df_melted,
                 x="Race",
                 y="Percent",
                 color="Insurance Type",
                 title="Health Insurance Coverage by Race",
                 barmode="stack")
    
    fig.update_layout(template="plotly_white",
                      yaxis_title="Percent",
                      xaxis_title="Race")
    
    fig.show()


# Load and stack data
cancer1 = pd.read_csv('USCSOverviewMap-1.csv')
cancer2 = pd.read_csv('USCSOverviewMap-2.csv')
cancer3 = pd.read_csv('USCSOverviewMap-3.csv')
cancer4 = pd.read_csv('USCSOverviewMap-4.csv')

cancer_death = pd.concat([cancer1, cancer2, cancer3, cancer4], ignore_index=True)

# Clean up
cancer_death = cancer_death[cancer_death['Age-Adjusted Rate'] != 'Data not presented']
cancer_death['Death Count'] = pd.to_numeric(cancer_death['Death Count'], errors='coerce')
cancer_death['Population'] = pd.to_numeric(cancer_death['Population'], errors='coerce')

# Calculate proper rate
cancer_death['Rate'] = (cancer_death['Death Count'] / cancer_death['Population']) * 100000

# Drop unused columns
cancer_death = cancer_death.drop(['Cancer Type', 'Year', 'Sex', 'Type', 'Age-Adjusted Rate'], axis=1)

# Only get areas (states) that have valid data
valid_states = cancer_death['Area'].unique()

# Dropdown widget for one state
state_selector = widgets.Dropdown(
    options=valid_states,
    description='State:',
)

# Function to update plot
def update_plot(selected_state):
    filtered_data = cancer_death[cancer_death['Area'] == selected_state]
    
    fig = px.bar(filtered_data,
                 x="Race",
                 y='Rate',
                 color="Race",
                 title=f"Cancer Death Rate in {selected_state} (2018–2021)")
    
    fig.update_layout(template="plotly_white",
                      xaxis_title="Race",
                      yaxis_title="Cancer Death Rate (per 100,000 people)")
    fig.show()

# Connect widget to plot

