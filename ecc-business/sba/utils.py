import pandas as pd
import numpy as np
import plotly.express as px

import ipywidgets as widgets
from IPython.display import display, clear_output

# Load the SBA dataset via partitioned CSV files
sba = [pd.read_csv(f"sba_{i}.csv", low_memory=False) for i in range(5)]
sba = pd.concat(sba, ignore_index=True)


def initial_inspection():
    output = widgets.Output()
    
    btn1 = widgets.Button(description='Columns 1-9')
    btn2 = widgets.Button(description='Columns 10-18')
    btn3 = widgets.Button(description='Columns 19-27')
    
    def show_chunk(start, end):
        with output:
            clear_output(wait=True)
            display(sba.shape)
            display(sba.iloc[:, start:end].head())
    
    btn1.on_click(lambda b: show_chunk(0, 9))
    btn2.on_click(lambda b: show_chunk(9, 18))
    btn3.on_click(lambda b: show_chunk(18, sba.shape[1]))
    
    button_box = widgets.HBox([btn1, btn2, btn3])
    display(button_box, output)
    show_chunk(0, 9)


def top_states_by_amount():
    for col in ['DisbursementGross', 'GrAppv', 'SBA_Appv']:
        sba[col] = sba[col].replace('[\\$,]', '', regex=True).astype(float)
    
    state_funding = (
        sba.groupby('State')['SBA_Appv']
           .sum()
           .sort_values(ascending=False)
           .reset_index()
    )
    
    total_states = len(state_funding)
    
    pages = 5
    chunk_size = 11
    min_sba = state_funding['SBA_Appv'].min()
    max_sba = state_funding['SBA_Appv'].max()
    
    page_slider = widgets.IntSlider(
        value=1,
        min=1,
        max=pages,
        description='Page',
        continuous_update=False
    )
    
    out = widgets.Output()
    
    def show_page(page):
        start = (page - 1) * chunk_size
        end = start + chunk_size
        chunk = state_funding.iloc[start:end]
    
        with out:
            clear_output(wait=True)
            fig = px.bar(
                chunk.sort_values('SBA_Appv'),
                x='SBA_Appv',
                y='State',
                orientation='h',
                color='SBA_Appv',
                color_continuous_scale='Greens',
                range_color=[min_sba, max_sba],
                labels={'SBA_Appv': 'SBA-Approved ($)', 'State': 'US State'},
                title=f'States {start+1}–{min(end, total_states)} by SBA-Approved Loan Amount'
            )
            fig.update_xaxes(range=[0, max_sba], tickformat="$.2s")
            fig.update_layout(width=1200, height=600, coloraxis_colorbar=dict(title='Loan Volume'))
            fig.show()
    
    display(widgets.HBox([page_slider]), out)
    widgets.interactive(show_page, page=page_slider)
    show_page(1)


def top_cities_by_amount():
    top_cities = sba.groupby(['City', 'State'])['SBA_Appv'].sum().reset_index()
    top_cities = top_cities.sort_values('SBA_Appv', ascending=False).head(20)
    
    fig = px.bar(top_cities, x='City', y='SBA_Appv',
                 title='Top 20 Cities by SBA-Approved Loan Amount',
                 color='State',
                 labels={'City': 'US City', 'SBA_Appv': 'SBA-Approved ($)'})
    
    fig.update_layout(width=1200, height=600)
    fig.show()


def top_industries_by_amount():
    sector_funding = (
        sba[sba['NAICS'] != 0]
          .assign(NAICS2=sba['NAICS'].astype(str).str[:2])
          .groupby('NAICS2')['SBA_Appv']
          .sum()
          .reset_index()
          .sort_values('SBA_Appv', ascending=False)
    )
    
    chunk_size = 8
    pages = 3
    max_sector = sector_funding['SBA_Appv'].max()
    
    page_slider = widgets.IntSlider(
        value=1, min=1, max=pages, description='Page', continuous_update=False
    )
    out = widgets.Output()
    
    def show_sector_page(page):
        start = (page - 1) * chunk_size
        end = start + chunk_size
        chunk = sector_funding.iloc[start:end]
    
        with out:
            clear_output(wait=True)
            fig = px.bar(
                chunk.sort_values('SBA_Appv'),
                x='SBA_Appv',
                y='NAICS2',
                orientation='h',
                color='SBA_Appv',
                color_continuous_scale='Oranges',
                range_color=[0, max_sector],
                labels={'SBA_Appv': 'SBA-Approved ($)', 'NAICS2': 'NAICS Sector Code'},
                title=f'NAICS Sectors {start+1}–{min(end, len(sector_funding))} by SBA-Approved ($)'
            )
            fig.update_xaxes(tickformat="$.2s", range=[0, max_sector])
            fig.update_layout(
                height=400,
                coloraxis_colorbar=dict(title='Loan Volume')
            )
            fig.show()
    
    display(widgets.VBox([page_slider]), out)
    widgets.interactive(show_sector_page, page=page_slider)
    show_sector_page(1)


def loan_count_per_state():
    state_counts = sba['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Loan Count']
    
    fig = px.choropleth(state_counts, locations='State',
                        locationmode='USA-states',
                        color='Loan Count',
                        scope="usa",
                        title="Loan Count per State")
    
    fig.update_layout(width=800, height=600)
    fig.show()


def avg_amount_per_loan_by_state():
    state_summary = (
        sba.groupby('State')
           .agg(total_sba=('SBA_Appv', 'sum'),
                loan_count=('SBA_Appv', 'count'))
           .reset_index()
    )
    state_summary['avg_sba_per_loan'] = state_summary['total_sba'] / state_summary['loan_count']
    
    fig = px.choropleth(
        state_summary,
        locations='State',
        locationmode='USA-states',
        color='avg_sba_per_loan',
        scope='usa',
        title='Average SBA-Approved Amount per Loan by State',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        width=800,
        height=600,
        coloraxis_colorbar=dict(title='Avg SBA $ / Loan')
    )
    fig.show()

def los_angeles_summary():
    la_df = sba[
        (sba['City'].str.upper() == 'LOS ANGELES') &
        (sba['State'] == 'CA')
    ].copy()
    
    la_summary = {
        'Total Loans': len(la_df),
        'Total SBA Approved ($)': la_df['SBA_Appv'].sum(),
        'Average SBA Approved ($)': la_df['SBA_Appv'].mean(),
        'Total Jobs Created': la_df['CreateJob'].sum(),
        'Total Jobs Retained': la_df['RetainedJob'].sum()
    }
    la_summary_df = pd.DataFrame.from_dict(la_summary, orient='index', columns=['Value'])
    la_summary_df.index.name = 'Metric'
    
    def format_value(metric, val):
        if 'SBA Approved' in metric:
            return f"${val:,.2f}"
        else:
            return f"{int(val):,}"
    
    la_summary_df['Value'] = [
        format_value(metric, value)
        for metric, value in la_summary_df['Value'].items()
    ]

    display(la_summary_df)

def annual_sba_approved_amount_la():
    la_df = sba[
        (sba['City'].str.upper() == 'LOS ANGELES') &
        (sba['State'] == 'CA')
    ].copy()
    
    la_df['ApprovalDate'] = pd.to_datetime(la_df['ApprovalDate'], format='%d-%b-%y')
    la_df['Year'] = la_df['ApprovalDate'].dt.year
    la_df = la_df[la_df['Year'] <= 2014]
    
    annual_la = la_df.groupby('Year')['SBA_Appv'].sum().reset_index()
    
    fig2 = px.line(
        annual_la,
        x='Year', y='SBA_Appv',
        title='Annual SBA Approved Amount in Los Angeles',
        labels={'SBA_Appv':'SBA Approved ($)'}
    )
    fig2.update_layout(width=1200, height=600)
    fig2.show()