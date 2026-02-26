# File: code_folder/visualization.py

import pandas as pd
import ipywidgets as widgets
from ipywidgets import interact
import matplotlib.pyplot as plt


def run_workforce_plot(df):
    """
    Creates an interactive plot to display the distribution of Race and Ethnicity,
    with filters for Region and LicenseName (Occupation).

    Parameters:
    df (pd.DataFrame): DataFrame containing at least the following columns:
                       'Region', 'LicenseName', and 'RaceEthnicity'.
    """
    
    # Create filter options based on the dataframe content
    region_options = ['All'] + sorted(df['Region'].dropna().unique())
    workforce_options = ['All'] + sorted(df['LicenseName'].dropna().unique())

    def visualize_data(region='All', workforce='All'):
        # Filter the DataFrame based on widget selections
        df_filtered = df.copy()
        if region != 'All':
            df_filtered = df_filtered[df_filtered['Region'] == region]
        if workforce != 'All':
            df_filtered = df_filtered[df_filtered['LicenseName'] == workforce]

        # Plot the Race and Ethnicity distribution
        plt.figure(figsize=(8, 5))
        df_filtered['RaceEthnicity'].value_counts().plot(kind='bar', color='skyblue')
        plt.title(f'Race and Ethnicity Distribution\n(Region: {region}, Occupation: {workforce})')
        plt.xlabel('Race and Ethnicity')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.show()

    # Create interactive widgets for Region and Workforce selections
    interact(
        visualize_data,
        region=widgets.Dropdown(options=region_options, value='All', description='Region:'),
        workforce=widgets.Dropdown(options=workforce_options, value='All', description='Occupation:')
    )


def run_highedu_plot(df):
    """
    Creates an interactive plot to display the distribution of Race and Ethnicity,
    with filters for Region and Highest Education.

    Parameters:
    df (pd.DataFrame): DataFrame containing at least the following columns:
                       'Region', 'HighestEduLevel', and 'RaceEthnicity'.
    """
    
    # Create filter options based on the dataframe content
    region_options = ['All'] + sorted(df['Region'].dropna().unique())
    workforce_options = ['All'] + sorted(df['HighestEduLevel'].dropna().unique())

    def visualize_data(region='All', workforce='All'):
        # Filter the DataFrame based on widget selections
        df_filtered = df.copy()
        if region != 'All':
            df_filtered = df_filtered[df_filtered['Region'] == region]
        if workforce != 'All':
            df_filtered = df_filtered[df_filtered['HighestEduLevel'] == workforce]

        # Plot the Race and Ethnicity distribution
        plt.figure(figsize=(8, 5))
        df_filtered['RaceEthnicity'].value_counts().plot(kind='bar', color='lightgreen')
        plt.title(f'Race and Ethnicity Distribution\n(Region: {region}, HighestEduLvl: {workforce})')
        plt.xlabel('Race and Ethnicity')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.show()

    # Create interactive widgets for Region and Workforce selections
    interact(
        visualize_data,
        region=widgets.Dropdown(options=region_options, value='All', description='Region:'),
        workforce=widgets.Dropdown(options=workforce_options, value='All', description='Highest Education:')
    )

