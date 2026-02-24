---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# ANOVA

+++

**Estimated Time**: 60 Minutes <br>
**Developers**: James Geronimo, Mark Barranda

+++

## Table of Contents

+++

1. Introduction <br>
    1.1. Learning Objectives <br>
    1.2. Understanding ANOVA <br>
    1.3. Setup <br>
2. Data Preparation <br>
    2.1. Loading the Data <br>
    2.2. Choosing the Right Columns <br>
    2.3. Filtering the Data  <br>
3. Visualizing the Data <br>
    3.1. Box Plots <br>
    3.2. Violin Plots <br>
    3.3. Histograms <br>
4. Performing ANOVA <br>
    4.1. Group Means and Overall Mean <br>
    4.2. Between-Group Sum of Squares (SSB) <br>
    4.3. Within-Group Sum of Squares (SSW) <br>
    4.4. Degrees of Freedom <br>
    4.5. Mean Squares (MSB, MSW) <br>
    4.6. F-Statistic <br>
    4.7. p-value <br>
5. Sanity Check using SciPy <br>
6. Penguins Sandbox <br>
    6.1. Loading the Data <br>
    6.2. Exploring Variable Distributions <br>
    6.3. Performing ANOVA <br>
7. Conclusion

+++

## Deliverables

+++

Throughout the notebook, there will be free-response questions! For each question, fill in your answer in the corresponding `Markdown` cell that says *Your Answer Here*. Please make sure to respond to each of the following questions, as they will be **graded**:

2. Data Preparation <br>
    **Question 2.3.1.** <br>
    **Question 2.3.2.** <br>
    **Question 2.3.3.** <br>
3. Visualizing the Data <br>
    **Question 3.1.** <br>
    **Question 3.2.** <br>
    **Question 3.3.1.** <br>
    **Question 3.3.2.** <br>
    **Question 3.3.3.** <br>
4. Performing ANOVA <br>
    **Question 4.6.** <br>
    **Question 4.7.** <br>
6. Penguins Sandbox <br>
    **Question 6.2.** <br>
    **Question 6.3.**

+++

---

+++

## 1. Introduction

+++

### 1.1. Learning Objectives

+++

Understanding how to compare multiple groups statistically is crucial in data analysis. We will learn to apply **ANOVA** to analyze housing prices and penguin attributes. In this notebook, you will:
- Understand when it is appropriate to use ANOVA
- Visualize housing price differences across different groups
- Learn how to manually compute ANOVA step-by-step
- Use SciPy’s `stats.f_oneway` as a sanity check
- Apply these techniques to the Palmer Penguins dataset

+++

### 1.2. Understanding ANOVA

+++

What is the motivation for using **An**alysis **O**f **Va**riance, a.k.a. **ANOVA**, over a traditional Two-Mean Test? ANOVA is used when comparing **more than two groups**. More specfically, when comparing multiple groups, a series of two-sample t-tests is inefficient and increases the risk of Type I errors (false positives). ANOVA allows us to compare **more than two groups** in a single test. ANOVA checks whether the means of different groups are significantly different by comparing within-group and between-group variability.

We will explore **comparing house prices across different neighborhoods** in our dataset. In order to run an ANOVA test in the first place, there are three assumptions that need to be made:

1. **Normality:** The populations follow a normal distribution.
2. **Homogeneity of Variance:** Variances across groups are equal.
3. **Independence:** Observations are independent of each other.

For the sake of this module, we will assume that these three assumptions are true.

+++

### 1.3. Setup

+++

Below, we have imported the Python libraries needed for this module. Run the code in this cell before running any other code cells, and be careful **not to change** any of the code.
You can run the cell in any of these ways:
 - Ctrl + Enter: Run the cell and keep the cursor in the same cell.
- Shift + Enter: Run the cell and move the cursor to the next cell.
- Click the Play button: Click the Run (play) button to the left of the cell to execute it.

```{code-cell} ipython3
import numpy as np
import pandas as pd
import scipy.stats as stats

import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import seaborn as sns

import ipywidgets as widgets
from IPython.display import display, clear_output
from utils import *
```

---

+++

## 2. Data Preparation

+++

### 2.1. Loading the Data

+++

Let's first load our data in a `DataFrame` object named `ames`. We do this by using the `read_csv` function from the `pandas` library. We then use `head(10)` to see the first 10 rows of the data. In other words, we view the "head" of the data. Additionally, we print the `columns` variable to see all the features present in our dataset.

```{code-cell} ipython3
# Load the dataset and print the columns
ames = pd.read_csv("ames.csv")
display(ames.head(10))
print(ames.columns)
```

### 2.2. Choosing the Right Columns

+++

Wow, that's a lot of columns to work with! While there are cool features like `"Garage Finish"` and `"Wood Deck SF"`, our analysis is primarily focused on understanding how house prices vary by neighborhood. Thus, we are only interested in two columns, namely, `"Neighborhood"` and `"SalePrice"`, so let's go ahead and index into these two columns and update our `ames` `DataFrame`. We will also print the shape of this filtered `DataFrame` to get a better idea of the data we are working with.

```{code-cell} ipython3
# Select relevant columns
ames = ames[["Neighborhood", "SalePrice"]]
display(ames.head(10))
print(ames.shape)
```

### 2.3. Filtering the Data

+++

We now need to ensure that our analysis focuses on neighborhoods with a sufficient number of observations. If a neighborhood has too few sales recorded, it may introduce statistical noise or lead to unreliable conclusions.

We start by calculating how many times each neighborhood appears in our dataset using the `value_counts` function. This provides a count of sales transactions per neighborhood. Next, we define a threshold to filter out neighborhoods with very few observations. In this case, we keep only neighborhoods with more than 50 recorded sales. This step helps ensure that our statistical tests have adequate sample sizes for meaningful comparisons. Finally, we update our `ames` DataFrame to retain only the neighborhoods that meet our threshold using `isin(selected_neighborhoods)` to filter rows where the `"Neighborhood"` column matches one of the selected values.

```{code-cell} ipython3
# Filter neighborhoods with enough data
neighborhood_counts = ames["Neighborhood"].value_counts()
selected_neighborhoods = neighborhood_counts[neighborhood_counts > 50].index
ames = ames[ames["Neighborhood"].isin(selected_neighborhoods)]
ames
```

**Question 2.3.1.** We set a threshold of 50 sales when filtering neighborhoods. What could happen if we included all neighborhoods, even those with very few observations?

+++

*Your Answer Here*

+++

**Question 2.3.2.** If we increased the threshold from 50 to 100, how might that affect our analysis? Would we be gaining accuracy or losing valuable data?

+++

*Your Answer Here*

+++

**Question 2.3.3.** What are some potential risks of excluding data from neighborhoods with few sales? What bias might this introduce in our results?

+++

*Your Answer Here*

+++

---

+++

## 3. Visualizing the Data

+++

### 3.1. Box Plots 

+++

Before conducting statistical tests, it’s important to explore the data visually. This helps us understand the distribution of house prices across neighborhoods and check for variability between groups. Generating box plots are a great way to summarize key aspects of the data, such as median prices, interquartile ranges (IQR), and potential outliers in each neighborhood.

We've abstracted away the code used to generate the plots you will see in this section, but if you're curious they can all be found in `utils.py`! We've also split the box plots in two, so the first half is the top 8 neighborhoods by average sale price, and the second half is the other 9.

```{code-cell} ipython3
ames_box_plots(ames)
```

**Question 3.1.** What do the circles in each of the box plots indicate? What do they tell us about the different neighborhoods?

+++

*Your Answer Here*

+++

### 3.2. Violin Plots

+++

As previously noted, visual exploration is key to understanding whatever data is being analyzed. A violin plot is a great alternative to a box plot, as it provides additional insights into the shape of the data distribution. Unlike box plots, violin plots reveal more about the distribution shape and density of sale prices, making them useful for spotting multimodal distributions.

We use similar code to 3.1. to generate our plot defined by `ames_violin_plots`, and split the violin plots by a similar criteria but in thirds.

```{code-cell} ipython3
ames_violin_plots(ames)
```

**Question 3.2.** Both box plots and violin plots show distribution, but what additional information does a violin plot provide that a box plot does not?

+++

*Your Answer Here*

+++

### 3.3. Histograms

+++

Now that we have a good grasp of the distributions per neighborhood, let's take a step back and look at all of the sale prices in Ames. We can do this by plotting a histogram, which helps us understand the overall distribution of house prices across the entire dataset. We will be capable of identifying some key trends, such as whether house prices are skewed, where the most common price ranges are, and whether there are outliers in the dataset.

Our custom `ames_histogram` function allows you to adjust the `bins` parameter dynamically using a slider! Try adjusting the slider below to change the number of bins and observe how it impacts the histogram.

```{code-cell} ipython3
ames_histogram(ames)
```

**Question 3.3.1.** What insights can we gain from looking at a histogram of house prices rather than just a single summary statistic like the mean or median?

+++

*Your Answer Here*

+++

**Question 3.3.2.** Looking at the histogram, do house prices appear to be normally distributed? If not, what type of skewness do you observe?

+++

*Your Answer Here*

+++

**Question 3.3.3.** When adjusting the slider, did increasing the bins reveal more details or make the visualization too noisy? What happens when you decrease the bins?

+++

*Your Answer Here*

+++

---

+++

## 4. Performing ANOVA

+++

Having cleaned and visualized the data, it is time to perform ANOVA! For this exercise, we will manually compute ANOVA in order to gain a deeper understanding of its components, in contrast to using a built-in function. There are 7 steps we want to follow:

+++

### 4.1. Group Means and Overall Mean

Computing the mean sale prices for each neighborhood and the overall mean of sale prices.

```{code-cell} ipython3
group_means = ames.groupby("Neighborhood", observed=True)["SalePrice"].mean()
overall_mean = ames["SalePrice"].mean()

group_means[:3], overall_mean
```

### 4.2. Between-Group Sum of Squares (SSB)

Computing the sum of squares between, or SSB.

```{code-cell} ipython3
ssb = sum(ames.groupby("Neighborhood", observed=True).size() * (group_means - overall_mean) ** 2)
ssb
```

### 4.3. Within-Group Sum of Squares (SSW)

Computing the sum of squares within, or SSW.

```{code-cell} ipython3
ssw = sum(sum((ames[ames["Neighborhood"] == group]["SalePrice"] - group_mean) ** 2)
          for group, group_mean in group_means.items())
ssw
```

### 4.4. Degrees of Freedom

Computing the degrees of freedom.

```{code-cell} ipython3
ames_between = len(group_means) - 1
ames_within = len(ames) - len(group_means)

print(f"{ames_between} {ames_within}")
```

### 4.5. Mean Squares (MSB, MSW)

Computing the mean squares between (MSB) and mean squares within (MSW).

```{code-cell} ipython3
msb = ssb / ames_between
msw = ssw / ames_within

print(f"MSB: {msb}, MSW: {msw}")
```

### 4.6. F-Statistic

Computing the F-Statistic.

```{code-cell} ipython3
f_statistic = msb / msw
f_statistic
```

**Question 4.6.** What does a very large F-statistic indicate about the differences in sale prices between neighborhoods? What would a small F-statistic suggest?

+++

*Your Answer Here*

+++

### 4.7. p-value

Computing the p-value.

```{code-cell} ipython3
p_value = 1 - stats.f.cdf(f_statistic, ames_between, ames_within)
float(p_value)
```

**Question 4.7.** The computed p-value is extremely small. What does this tell us about the likelihood that all neighborhoods have the same average sale price? How should we interpret this result?

+++

*Your Answer Here*

+++

---

+++

## 5. Sanity Check Using SciPy

+++

Now that we have computed the F-statistic and p-value for ANOVA manually, let us use a pre-packaged function from `SciPy` called `f_oneway` to sanity check our results. 

Before we can instantly plug our data into `f_oneway`, there are a few steps we need to take to set up our input correctly. First, we initialize an empty list called `price_groups` to store sale prices per neighborhood. Next, we loop through `selected_neighborhoods`, filter the data to each neighborhood, and extract the sale prices for each one. Then, these extracted values are appended to `price_groups`, ultimately creating a list of `pd.Series`. Finally, we pass this list into `f_oneway`, using the unpacking operator `*` to so it inputs each `pd.Series` as a separate argument.

```{code-cell} ipython3
# Prepare SalePrice data for each neighborhood
price_groups = []
for neighborhood in selected_neighborhoods:
    ames_neighborhood = ames[ames["Neighborhood"] == neighborhood]
    price_group = ames_neighborhood["SalePrice"]
    price_groups.append(price_group)

# Run the One-Way ANOVA test
anova_result = stats.f_oneway(*price_groups)

print(f"Sanity Check - SciPy F-statistic: {anova_result.statistic:.2f}, p-value: {anova_result.pvalue:.5f}")
```

---

+++

## 6. Penguins Sandbox

+++

After completing our ANOVA analysis on the Ames Housing dataset, we can pivot to a new dataset: the **Palmer Penguins** dataset. It contains physical measurements for penguins across three species — **Adelie, Chinstrap, and Gentoo** — and serves as a great dataset for exploring variance across groups.

+++

### 6.1. Loading the Data

We load the dataset directly from `Seaborn` and immediately drop rows with missing values using `dropna` to simplify the analysis. This gives us a clean dataset with complete records for each penguin.

```{code-cell} ipython3
# Load the dataset
penguins = sns.load_dataset("penguins")
penguins = penguins.dropna()
penguins.head(10)
```

### 6.2. Exploring Variable Distributions

Here, we use three custom interactive functions — `penguins_box_plots`, `penguins_violin_plots`, and `penguins_histogram` — to explore the distribution of quantitative features like `bill_length_mm` and `body_mass_g` across different species. Also, similar to the `ames_histogram` function from *Part 3.3.*, you can change the number of bins for `penguins_histogram` using the given slider. These features allow us to **visually assess variation** and determine whether differences might exist — a prerequisite for conducting **ANOVA**.

```{code-cell} ipython3
penguins_box_plots(penguins)
```

```{code-cell} ipython3
penguins_violin_plots(penguins)
```

```{code-cell} ipython3
penguins_histogram(penguins)
```

**Question 6.2.** Based on the visualizations you explored, which quantitative feature shows the most variation between penguin species? Which of the three visualization types was the most effective in revealing these differences, and why?

+++

*Your Answer Here*

+++

### 6.3. Performing ANOVA

We built a custom `penguins_run_anova` function that runs ANOVA similar to *Part 5.* Given the exploration you did in *Part 6.2.*, choose the feature you would like to run ANOVA on using the dropdown menu.

```{code-cell} ipython3
penguins_run_anova(penguins)
```

**Question 6.3.** Which feature did you choose to run your ANOVA test on? What does the F-statistic tell us in this context? How about the p-value — what does it indicate about differences between species? Do these results align with your expectations based on the visualizations in *Part 6.2.*?

+++

*Your Answer Here*

+++

---

+++

## 7. Conclusion

+++

In this notebook, we explored using ANOVA using the Ames Housing and Palmer Penguins datasets!

Note, however, that we should have more rigorously proved the ANOVA assumptions to be true at the start of the notebook, though this was abstracted away for the sake of this notebook. We highly encourage you to try proving these checks on your own, and you may find some interesting results!

We encourage you to explore further with the groundwork laid out with this notebook. You can try running ANOVA on different features and explore more tests to determine what neighborhoods had more signficant differences in sale price against other neighborhoods.

+++

## 📋 Post-Notebook Reflection Form

Thank you for completing the notebook! We’d love to hear your thoughts so we can continue improving and creating content that supports your learning.

Please take a few minutes to fill out this short reflection form:

👉 **[Click here to fill out the Reflection Form](https://docs.google.com/forms/d/e/1FAIpQLSezyVeNkjH-PDCo5BygyiVulUGkS7IRKnNKDFueAVyooXLcjw/viewform?usp=dialog)**

---

### 🧠 Why it matters:
Your feedback helps us understand:
- How clear and helpful the notebook was
- What you learned from the experience
- How your views on data science may have changed
- What topics you’d like to see in the future

This form is anonymous and should take less than 5 minutes to complete.

We appreciate your time and honest input! 💬

+++

---

+++

**Woohoo! You have completed this notebook! 🚀**
