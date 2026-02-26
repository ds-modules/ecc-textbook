from datascience import * # Loads functions from the datascience library into our current environment
import numpy as np # Loads numerical functions
import math, random # Loads math and random functions
import otter # Loads functions that we'll use later to export this notebook to PDF for submission
from datascience import * # Loads functions from the datascience library into our current environment
import numpy as np # Loads numerical functions
import math, random # Loads math and random functions
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Latex, Markdown
import plotly.express as px
generator = otter.Notebook()

diabetes = Table.read_table("Diabetes_LA_2021.csv") # Here we see an assignment statement
income =  Table.read_table("Median_Household_Income.csv")
diabetes.relabel('name', 'Neighborhoods').relabel('denom_pop_18_over', 'Population') #relabeling 
diabetes = diabetes.with_column("Diabetes", diabetes.apply(lambda x: int(float(x.strip('%'))), "Diabetes"))
diabetes = diabetes.join('Neighborhoods', income, 'name')
diabetes = diabetes.with_column("Median Household Income", diabetes.apply(lambda x: int(np.nan_to_num(float(x))), "Median Household Income"))
diabetes = diabetes.drop('year_2', 'denom_total_hh')
diabetes = diabetes.with_column("Percent Diabetes", (diabetes.column("Diabetes") / diabetes.column("Population"))*100)



def level(x):
    if x>= 140363:
        return 'High'
    if  x>=83696 :
        return 'High-Medium' 
    if  x>=50092 :
        return 'Medium' 
    if x>= 25807:
        return 'Medium-Low' 
    if x< 25807:
        return 'Low' 

diabetes = diabetes.with_column("Income Level", diabetes.apply(lambda x: level(x), "Median Household Income"))
    


