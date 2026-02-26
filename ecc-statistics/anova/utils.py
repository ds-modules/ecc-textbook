import numpy as np
import pandas as pd
import scipy.stats as stats

import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import seaborn as sns

import ipywidgets as widgets
from IPython.display import display, clear_output


def ames_box_plots(ames):
    output = widgets.Output()
    neighborhood_medians = ames.groupby("Neighborhood", observed=True)["SalePrice"].median().sort_values(ascending=False)
    neighborhoods = neighborhood_medians.index.tolist()
    midpoint = len(neighborhoods) // 2

    def plot_half(half):
        with output:
            clear_output(wait=True)
            subset = neighborhoods[:midpoint] if half == "First Half" else neighborhoods[midpoint:]
            filtered_ames = ames[ames["Neighborhood"].isin(subset)]
            fig = px.box(filtered_ames, x="Neighborhood", y="SalePrice", color="Neighborhood",
                         category_orders={"Neighborhood": subset},
                         title=f"Box Plots of Sale Prices ({half})")
            fig.update_layout(xaxis_tickangle=-45)
            fig.show()

    half_selector = widgets.ToggleButtons(options=["First Half", "Second Half"], description="Show:")
    display(widgets.VBox([half_selector, output]))
    plot_half(half_selector.value)
    half_selector.observe(lambda change: plot_half(change['new']), names='value')


def ames_violin_plots(ames):
    output = widgets.Output()
    neighborhood_medians = ames.groupby("Neighborhood", observed=True)["SalePrice"].median().sort_values(ascending=False)
    neighborhoods = neighborhood_medians.index.tolist()
    third = len(neighborhoods) // 3

    def plot_third(segment):
        with output:
            clear_output(wait=True)
            if segment == "First Third":
                subset = neighborhoods[:third]
            elif segment == "Second Third":
                subset = neighborhoods[third:2*third]
            else:
                subset = neighborhoods[2*third:]
            filtered_ames = ames[ames["Neighborhood"].isin(subset)]
            fig = px.violin(filtered_ames, x="Neighborhood", y="SalePrice", color="Neighborhood", box=True,
                            category_orders={"Neighborhood": subset},
                            title=f"Violin Plots of Sale Prices ({segment})")
            fig.update_layout(xaxis_tickangle=-45)
            fig.show()

    third_selector = widgets.ToggleButtons(options=["First Third", "Second Third", "Last Third"], description="Show:")
    display(widgets.VBox([third_selector, output]))
    plot_third(third_selector.value)
    third_selector.observe(lambda change: plot_third(change['new']), names='value')


def ames_histogram(ames):
    output = widgets.Output()

    def plot_histogram(bins):
        with output:
            clear_output(wait=True)
            fig = px.histogram(ames, x="SalePrice", nbins=bins, marginal="rug", title=f"Histogram of Sale Prices (Bins={bins})")
            fig.update_layout(bargap=0.05)
            fig.show()

    bins_slider = widgets.IntSlider(min=5, max=50, step=5, value=25, description='Bins:')
    display(widgets.VBox([bins_slider, output]))
    plot_histogram(bins_slider.value)
    bins_slider.observe(lambda change: plot_histogram(change['new']), names='value')


def penguins_box_plots(penguins):
    output = widgets.Output()
    quantitative_columns = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

    def plot_boxplot(variable):
        with output:
            clear_output(wait=True)
            fig = px.box(penguins, x="species", y=variable, color="species",
                         title=f"Box Plot of {variable} by Species")
            fig.update_layout(xaxis_tickangle=-45)
            fig.show()

    variable_dropdown = widgets.Dropdown(options=quantitative_columns, description='Variable:')
    display(widgets.VBox([variable_dropdown, output]))
    plot_boxplot(variable_dropdown.value)
    variable_dropdown.observe(lambda change: plot_boxplot(change['new']), names='value')


def penguins_violin_plots(penguins):
    output = widgets.Output()
    quantitative_columns = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

    def plot_violinplot(variable):
        with output:
            clear_output(wait=True)
            fig = px.violin(penguins, x="species", y=variable, color="species", box=True,
                            title=f"Violin Plot of {variable} by Species")
            fig.update_layout(xaxis_tickangle=-45)
            fig.show()

    variable_dropdown = widgets.Dropdown(options=quantitative_columns, description='Variable:')
    display(widgets.VBox([variable_dropdown, output]))
    plot_violinplot(variable_dropdown.value)
    variable_dropdown.observe(lambda change: plot_violinplot(change['new']), names='value')


def penguins_histogram(penguins):
    output = widgets.Output()
    quantitative_columns = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

    def plot_histogram(variable, bins):
        with output:
            clear_output(wait=True)
            plt.figure(figsize=(12, 6))
            sns.histplot(data=penguins, x=variable, hue="species", bins=bins, kde=True, alpha=0.7)
            plt.ylabel("Count")
            plt.title(f"Overlaid Histogram of {variable} by Species (Bins={bins})")
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.show()

    variable_dropdown = widgets.Dropdown(options=quantitative_columns, description='Variable:')
    bins_slider = widgets.IntSlider(min=5, max=50, step=5, value=25, description='Bins:')
    display(widgets.VBox([variable_dropdown, bins_slider, output]))
    plot_histogram(variable_dropdown.value, bins_slider.value)
    variable_dropdown.observe(lambda change: plot_histogram(change['new'], bins_slider.value), names='value')
    bins_slider.observe(lambda change: plot_histogram(variable_dropdown.value, change['new']), names='value')


def penguins_run_anova(penguins):
    output = widgets.Output()
    quantitative_columns = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

    def run_anova(feature):
        with output:
            clear_output(wait=True)
            feature_groups = [penguins[penguins["species"] == sp][feature] for sp in penguins["species"].unique()]
            result = stats.f_oneway(*feature_groups)

            print(f"ANOVA on: {feature}")
            print(f"F-statistic: {result.statistic:.2f}")
            print(f"p-value: {result.pvalue:.5f}")

    feature_dropdown = widgets.Dropdown(options=quantitative_columns, description="Feature:")
    display(widgets.VBox([feature_dropdown, output]))
    run_anova(feature_dropdown.value)
    feature_dropdown.observe(lambda change: run_anova(change['new']), names='value')
