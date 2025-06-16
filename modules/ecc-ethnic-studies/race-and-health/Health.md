---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.2
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Race and Health

---

In this notebook, you will explore how race impacts health outcomes and access to healthcare in the United States.

**Estimated Time:** ~30 minutes

---

## Topics Covered

1. Maternal Mortality Rates  
2. Breast Cancer  
3. Insurance  

```{code-cell} ipython3
from datascience import * # Loads functions from the datascience library into our current environment
import numpy as np # Loads numerical functions
import math, random # Loads math and random functions
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Latex, Markdown
%matplotlib inline
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display
from ipywidgets import interact
import warnings
warnings.filterwarnings('ignore')
import helper as hp
```

## Notebook Walk through 
In addition to the instructions in the notebook, we also have a video walkthrough of the entire process. We encourage you to refer to the video if you need help or even follow along with the instructor as you complete the task.

```{code-cell} ipython3
from IPython.display import YouTubeVideo

YouTubeVideo("c_jACM5MUeo", width=560, height=315)
```

## Maternal Mortality Rates

In this section, we’re exploring maternal mortality rates by race to better understand the deeper racial inequalities embedded in the U.S. healthcare system.

### Question 1

To begin, what do you know about how maternal mortality rates vary across different racial or ethnic groups (or other racial issues in the healthcare system)?  
Have you heard or learned about this issue before? If so, where did you first come across it?

+++

The following dataset, collected by the CDC over several years, shows the maternal mortality rate (per 100,000 live births) broken down by race and year.  
Run the cell below to view the data.

```{code-cell} ipython3
hp.maternal
```

Now let’s take a closer look at two visualizations of this data.  
Run the cell below to display two interactive graphs, and use the tools provided to explore patterns and trends more deeply.

**Note:** The peak in the data occurs in 2021 due to the impacts of COVID-19, so keep that in mind when interpreting the results.

```{code-cell} ipython3
hp.Mortality_Rate_bar()
hp.Mortality_Rate_line()
```

### Question 2  
**Why is this happening?**

After reviewing the following article:  
[Black Women and Maternal Mortality – AP News (2023)](https://projects.apnews.com/features/2023/from-birth-to-death/black-women-maternal-mortality-rate.html),  
please respond to the prompts below in the next cell:

#### Explain the Data  
Interpret the maternal mortality statistics you’ve observed, incorporating the context and insights provided by the article.  
Consider factors such as racial disparities, systemic healthcare issues, and any historical or societal influences discussed.

#### Reflect on Impact  
How does this information influence your perception of the healthcare system?  
Does it affect you personally or change your understanding of racism in healthcare and how different patients are treated?  
Share your thoughts on how these revelations might shape your views or actions regarding healthcare equity.

+++

## Breast Cancer

First, read the following article to get more background on racial disparities in healthcare:  
[Breast Cancer Racial Disparities – BCRF](https://www.bcrf.org/about-breast-cancer/breast-cancer-racial-disparities/)

Then, run the cell below to display breast cancer death rates by state.  
Compare different states and make some initial observations.
 

```{code-cell} ipython3
display(widgets.interactive(lambda state : hp.update_plot(state), state= hp.state_selector))
```

### Question 3

Now, explore the different displays of data provided in the following report to better understand what our dataset is capturing — and what it might be missing:  
[Breast Cancer Facts & Figures 2024 – American Cancer Society (PDF)](https://www.cancer.org/content/dam/cancer-org/research/cancer-facts-and-statistics/breast-cancer-facts-and-figures/2024/breast-cancer-facts-and-figures-2024.pdf)

Afterward, choose one display from the article that you found most interesting.  
Connect it to the data shown above, and write a short summary of your findings.

+++

## Insurance

### Introduction  
Health insurance plays a major role in determining how easily someone can access healthcare services in the U.S.  
But not everyone has equal access to insurance. Across racial and ethnic groups, there are large gaps in both coverage rates and the types of insurance people rely on—such as employer-sponsored plans, private insurance, or government programs like Medicaid.  
These differences can significantly impact maternal health outcomes and the overall quality of care people receive.

### Question 4  
What types of health insurance are you familiar with, and who do you think has the hardest time accessing them?  
Why do you think some groups are more likely to be uninsured?

+++

In this next dataset, we’re looking at information from a report by KFF (Kaiser Family Foundation), based on their analysis of American Community Survey (ACS) data collected by the U.S. Census Bureau. The analysis focuses on individuals under age 65 and covers the years 2010 through 2023.

Run the next cells to display our two datasets:  
- The first shows uninsured rates by race from 2010 to 2023.  
- The second shows the average percentage of people in each racial group covered by various types of insurance.

```{code-cell} ipython3
hp.Uninsured_Rate
```

```{code-cell} ipython3
hp.insurance
```

play the next cell to see a visuliziations of the data 

```{code-cell} ipython3
hp.Uninsured()
```

```{code-cell} ipython3
hp.insurance_type()
```

### Question 5

What do the differences in uninsured rates and types of insurance coverage suggest about systemic barriers in the U.S. healthcare system?  
How might these barriers impact people's health outcomes across different communities?  
Did anything stand out to you?

+++

### Question 6

#### Final Reflection: Answer the following questions

- How do racial disparities in healthcare show up in both the numbers and the lived experiences described in the article?  
- What are some limits of using just data to understand these issues?  
- How do racial disparities in female health outcomes, like breast cancer death rates, reflect larger patterns of social inequality and systemic racism in the healthcare system?  
- In what ways do structural factors (like access to insurance, quality of care, and early diagnosis) help explain why women of different racial backgrounds experience different health outcomes — even when they have the same diseases?

+++

## 📋 Post-Notebook Reflection Form

Thank you for completing the notebook! We’d love to hear your thoughts so we can continue improving and creating content that supports your learning.

Please take a few minutes to fill out this short reflection form:

👉 **[Click here to fill out the Reflection Form](https://docs.google.com/forms/d/e/1FAIpQLScTa5vPzgOcrjpTiJAqjUv-le9_OsSE1iEdcr_MJbreEA7AOA/viewform?usp=header)**

---

### 🧠 Why it matters:
Your feedback helps us understand:
- How clear and helpful the notebook was
- What you learned from the experience
- How your views on data science may have changed
- What topics you’d like to see in the future

This form is anonymous and should take less than 8 minutes to complete.

We appreciate your time and honest input! 💬
