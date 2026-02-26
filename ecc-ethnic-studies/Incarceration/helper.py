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

#big data 
arrest= pd.read_csv('OnlineArrestData.csv') #data
arrest['Sum Total']= arrest['F_TOTAL']+arrest['M_TOTAL']+arrest['S_TOTAL'] 
arrest
#1 
year_slider= widgets.IntRangeSlider(min=1980, max=2023, step=1, description="Year Range:", continuous_update= True)

def plot_arrest(arrest, years):
    sum_arrest= arrest[(arrest['YEAR']<=years[1]) & (arrest['YEAR']>=years[0])] [['YEAR','F_TOTAL']].groupby('YEAR').sum().reset_index()
    sns.lineplot(data = sum_arrest, x= 'YEAR', y='F_TOTAL')
    plt.title("Arrest")
    plt.show()

#2
def plot_drug_arrest(arrest, years):
    plt.clf()
    drug_arrest= arrest[(arrest['YEAR']<=years[1]) & (arrest['YEAR']>=years[0])][['YEAR','F_DRUGOFF']].groupby('YEAR').sum().reset_index()
    sns.lineplot(data = drug_arrest, x= 'YEAR', y='F_DRUGOFF', label = 'Drugs')
    plt.title("Drug Arrest")
    plt.show()

#3
race_dropdown= widgets.Dropdown(options=['White', "Black", "Hispanic", "Other"])
year_slider= widgets.IntRangeSlider(min=1980, max=2023, step=1, description="Year Range:", continuous_update= True)

def drug_plot_race(arrest, years, race):
    race_drug_arrest= arrest[(arrest['RACE']== race) & (arrest['YEAR']<=years[1]) & (arrest['YEAR']>=years[0])][['YEAR','F_DRUGOFF']].groupby('YEAR').sum().reset_index()
    sns.lineplot(data= race_drug_arrest,  x= 'YEAR', y= 'F_DRUGOFF')
    plt.title(race + " Drug Arrest")
    plt.show()

#4
checkboxes = [
    widgets.Checkbox(description='White'),
    widgets.Checkbox(description='Black'),
    widgets.Checkbox(description='Hispanic'),
    widgets.Checkbox(description='Other')
]

def get_selected_races():
    """Extract selected race values from checkboxes."""
    return [cb.description for cb in checkboxes if cb.value]

def plot_races(arrest,years):
    """Plot drug arrests for selected races over the given year range."""
    selected_races = get_selected_races()  # Get selected checkboxes

    # Filter dataset
    race_drug_arrest = arrest[
        (arrest['YEAR'] <= years[1]) & 
        (arrest['YEAR'] >= years[0]) &
        (arrest['RACE'].isin(selected_races))
    ].groupby(['YEAR', 'RACE'])['F_DRUGOFF'].sum().reset_index()

    # Plot each selected race
    plt.figure(figsize=(10, 5))
    for race in selected_races:
        subset = race_drug_arrest[race_drug_arrest['RACE'] == race]
        sns.lineplot(data=subset, x='YEAR', y='F_DRUGOFF', label=race)
    
    plt.legend()
    plt.title('Drug Arrests by Race Over Time')
    plt.xlabel('Year')
    plt.ylabel('Number of Drug Arrests')
    plt.show()
    
#5 
def drug_percentage_increase(arrest, race):
    race_drug_arrest = arrest[['YEAR','F_DRUGOFF','RACE']].groupby(['YEAR','RACE']).sum().reset_index()
    drug_arrest = Table.from_df(race_drug_arrest)
    eighty = drug_arrest.where('YEAR',1980).where('RACE', race).column('F_DRUGOFF')[0]
    ninety=  drug_arrest.where('YEAR',1989).where('RACE', race).column('F_DRUGOFF')[0]
    return print( 'From 1980 to 1989 ' + race + " people had a "+ str(((ninety-eighty)/eighty)*100) + " percent growth rate, in drug arrest.") 
    
#6
arrest_dropdown= widgets.Dropdown(options=['F_DRUGOFF','F_TOTAL'])
def plot_type_arrest(arrest, arrest_type,years):
    sum_arrest= arrest[(arrest['YEAR']<=years[1]) & (arrest['YEAR']>=years[0])][['YEAR',arrest_type]].groupby('YEAR').sum().reset_index()
    sns.lineplot(data = sum_arrest, x= 'YEAR', y=arrest_type)
    plt.title(arrest_type)
    plt.show()

#7 
def plot_violence(arrest, years, overlay):

    if overlay: 
        drug_arrest= arrest[(arrest['YEAR']<=years[1]) & (arrest['YEAR']>=years[0])][['YEAR','F_DRUGOFF']].groupby('YEAR').sum().reset_index()
        violent_arrest= arrest[(arrest['YEAR']<=years[1]) & (arrest['YEAR']>=years[0])][['YEAR','VIOLENT']].groupby('YEAR').sum().reset_index()
        sns.lineplot(data = drug_arrest, x= 'YEAR', y='F_DRUGOFF', label = 'Drugs')
        sns.lineplot(data = violent_arrest, x= 'YEAR', y='VIOLENT', label= 'VIOLENT')
        plt.legend()
        plt.show()



    else:
        violent_arrest= arrest[(arrest['YEAR']<=years[1]) & (arrest['YEAR']>=years[0])][['YEAR','VIOLENT']].groupby('YEAR').sum().reset_index()
        sns.lineplot(data = violent_arrest, x= 'YEAR', y='VIOLENT', label= 'VIOLENT')
        plt.legend()
        plt.show()

#8 
county_dropdown= widgets.Dropdown(options= arrest['COUNTY'].unique())

def map_f_arrest(arrest, x): 
    sum_arrest= arrest[(arrest['COUNTY']== x)][['YEAR','F_TOTAL']].groupby('YEAR').sum().reset_index()
    sns.lineplot(data = sum_arrest, x= 'YEAR', y='F_TOTAL')
    plt.show()
    race_arrest = arrest[arrest['COUNTY']== x][['YEAR','F_TOTAL','RACE']].groupby(['YEAR','RACE']).sum().reset_index()
    for race in arrest['RACE'].unique():
        sns.lineplot(data = race_arrest[race_arrest['RACE']== race ],  x= 'YEAR', y= 'F_TOTAL',label= race)
        plt.legend()
    
    plt.show()


# 9 
#edit table 
pop_percent= pd.read_csv('pop.csv')
pop_percent['Other']= pop_percent['Asian or Pacific Islander'].str.split('%').str[0].astype('float')+pop_percent['Other'].str.split('%').str[0].astype('float')
pop_percent = pop_percent.drop('Asian or Pacific Islander', axis =1 )
pop_percent

#joining tables 
races = ["White", "Hispanic", "Black", "Other"]
for race in races:
    pop_race= pop_percent[[race]].rename({race: 'pop_percent'}, axis = 1)
    pop_race['Race']= race
    pop_race['Year']= pop_percent['Race or ethnicity']
    if not race== "Other":
        pop_race['pop_percent']= pop_race['pop_percent'].str.split('%').str[0].astype('float')
    globals()[race]= pop_race

df_combined = pd.concat([White, Black], ignore_index=True)
df_combined = pd.concat([df_combined, Hispanic], ignore_index=True)
pop_race = pd.concat([df_combined, Other], ignore_index=True)
pop_race
# function baced on type of arrest
pop_cal = pd.read_csv('california_population.csv')
def type_arrest(x):
    incar = arrest.groupby(['RACE','YEAR'])[x].agg('sum').reset_index()
    per_arrest = pd.merge(left = incar, right = pop_cal, left_on = 'YEAR', right_on= 'Year').drop('YEAR', axis =1).rename({'RACE':'Race'}, axis =1)
    per_arrest = pd.merge(left = per_arrest, right = pop_race, on= ['Race', 'Year'])
    per_arrest['race_pop']= np.round(per_arrest['Population']*(per_arrest['pop_percent']/100))
    per_arrest['Percent Arrest per Race']= per_arrest[x]/per_arrest['race_pop']*100
    return per_arrest[['Race', 'Year','Sum Total', 'race_pop', 'Percent Arrest per Race']]

extended_arrest= type_arrest("Sum Total")
year_dropdown= widgets.Dropdown(options= range(1990, 2023))

#10
def bar_arrest(extended_arrest, year): 
    group = extended_arrest.groupby(['Year','Race']).agg({'Percent Arrest per Race': np.mean}).reset_index()
    group_year = group[group['Year']== year]
    sns.barplot(data= group_year, x= 'Race', y='Percent Arrest per Race')
    plt.title("Percent Arrest per Race "+ str(year))
    plt.show()

#11
def bar_years(extended_arrest,year_range):
    # Ensure that the 'Year' column is numeric
    extended_arrest['Year'] = pd.to_numeric(extended_arrest['Year'], errors='coerce')

    # Aggregate data
    group = extended_arrest.groupby(['Year', 'Race'], as_index=False).agg({'Percent Arrest per Race': 'mean'})

    # Filter for the selected range of years
    group_year = group[(group['Year'] >= year_range[0]) & (group['Year'] <= year_range[1])]

    # Create grouped bar plot (bars side by side)
    fig = px.bar(group_year, 
                 x='Race', 
                 y='Percent Arrest per Race', 
                 color=group_year['Year'].astype(str),  # Convert Year to string for better grouping
                 barmode='group',  # This ensures side-by-side bars
                 title="Percent Arrests by Race (Selectable Year Range)",
                 labels={'Percent Arrest per Race': 'Percent Arrests', 'Year': 'Year'},
                 hover_data=['Year'])

    fig.update_layout(xaxis_title="Race", yaxis_title="Percent Arrests", legend_title="Year")

    # Show figure
    fig.show()

# Year range selection widget
year_selector = widgets.IntRangeSlider(
    value=[2000, 2010],  # Default range
    min=1980,
    max=2025,
    step=1,
    description="Years:",
    continuous_update=False
)

#12
def box_arrest(extended_arrest): 
    group = extended_arrest.groupby(['Year','Race']).agg({'Percent Arrest per Race': np.mean}).reset_index()
    group_year = group
    sns.boxplot(data = extended_arrest, x ='Percent Arrest per Race' , y = 'Race')



    