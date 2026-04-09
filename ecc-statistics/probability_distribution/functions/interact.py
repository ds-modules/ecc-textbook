import ipywidgets as widgets
from ipywidgets import interact

from functions.utils import *

def bernoulli():
    interact(plot_bernoulli, 
         p=widgets.FloatSlider(min=0, max=1, step=0.05, value=0.5, description="p"),
         highlight=widgets.IntSlider(min=0, max=1, step=1, value=1, description="X=x"));

def binomial():
    interact(plot_binomial, 
         n=widgets.IntSlider(min=1, max=20, step=1, value=8, description="n"),
         p=widgets.FloatSlider(min=0.01, max=1, step=0.01, value=1/6, description="p"),
         highlight=widgets.IntSlider(min=0, max=20, step=1, value=2, description="X=x"));

def poisson():
    interact(plot_poisson, 
         lam=widgets.IntSlider(min=1, max=40, step=1, value=3, description="λ"),
                               highlight=widgets.IntSlider(min=0, max=50, step=1, value=2, description="k"));

def geometric():
    interact(plot_geometric, 
         p=widgets.FloatSlider(min=0.01, max=1, step=0.02, value=0.5, description="p"),
         highlight=widgets.IntSlider(min=1, max=15, step=1, value=3, description="X=x"));

def uniform():
    interact(plot_uniform_bars, 
         a=widgets.IntSlider(min=0, max=20, step=1, value=0, description="a"),
         b=widgets.IntSlider(min=1, max=30, step=1, value=10, description="b"),
         highlight=widgets.IntSlider(min=0, max=30, step=1, value=5, description="X=x"));


def geometric_walkthrough():
    """Launch the interactive geometric walkthrough visualizer."""
    interact(
        geometric_walkthrough_visualizer,
        p_example=widgets.FloatSlider(value=0.44, min=0.1, max=0.9, step=0.02, description="p (example)"),
        k_example=widgets.IntSlider(value=3, min=1, max=10, description="k (call #)"),
        target_prob=widgets.FloatSlider(value=0.30, min=0.05, max=0.9, step=0.05, description="Target prob (Q2)"),
    )