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

```{code-cell} ipython3
:deletable: false
:editable: false

# Initialize Otter
import otter
grader = otter.Notebook("Incarcerations.ipynb")
```

# Incarceration and Race

---

You will be learning about events in history that have impacted incarceration rates across different racial groups in the United States.

**Estimated Time:** ~30 minutes

---

## 1. Introduction to Data

- a. Overview of Data Table  
- b. Explanation of Table Columns  
- c. Question 1  
- d. First Look  

## 2. War on Drugs

- a. Introduction to the War on Drugs  
- b. Crack vs. Cocaine  
- c. Growth Rate of Drug Use  
- d. Question 2  
- e. 1990s Drug Drop  
- f. Percent of Arrests by Population  
- g. Questions 3 and 4  

## 3. Redlining

- a. County-Level Data  
- b. Historical Context of Redlining in Counties  
- c. Question 5  

## 4. Sources

+++

### Import Libraries

To start off, we need to load some libraries, such as NumPy, that we’ve learned about.  
Run the cell below to do so.

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
from IPython.display import Video
from ipywidgets import interact
import warnings
warnings.filterwarnings('ignore')
import helper as hp
```

# Helper Video

#### Use the following link for a follow-along video to help guide you through the notebook:

```{code-cell} ipython3
from IPython.display import YouTubeVideo

YouTubeVideo("X2NvxzQ2CvI", width=560, height=315)
```

# Introduction 

+++

### Data

The Department of Justice (DOJ) Criminal Justice Statistics Center (CJSC) collects information on arrests  
and citations (from now on referred to as “arrest(s)”) as reported by law enforcement agencies (LEAs) throughout the state.  
The Monthly Arrest and Citation Register (MACR) data are reported monthly by law enforcement agencies (LEAs).  
Summary arrest counts are submitted to the Federal Bureau of Investigation’s (FBI) Uniform Crime Reporting Program (UCR).

Arrest data provides information on felony- and misdemeanor-level arrests for adults and juveniles,  
as well as status offenses (e.g., truancy, incorrigibility, running away, and curfew violations) for juveniles.  
The data includes aggregated arrest counts by reporting county, age, gender, and race/ethnic group of the arrestee.  
Arrest Disposition data also includes the law enforcement disposition.

---

Run the cell below to load the data, view the first few rows, and examine the column names.

```{code-cell} ipython3
arrest = hp.arrest
arrest
```

Run the next cell below to view the columns in our dataset.

```{code-cell} ipython3
print(arrest.columns)
```

### Review of Column Labels and Their Descriptions

- **Year** – The year the data was recorded, ranging from 1980 to 2023.

- **Gender** – The gender of the arrestee, categorized as either male or female.

- **Race** – Racial/ethnic group of the arrestee, categorized as White, Black, Hispanic, or Other.

- **Age Group** – Age categories grouped as:
  - Under 18  
  - 18–19  
  - 20–29  
  - 30–39  
  - 40–69  
  - 70+

- **County** – The California county where the arrest data was collected.

- **Violent** – Number of arrests for crimes classified as violent felonies.

- **Property** – Number of arrests for crimes classified as property felonies.

- **F_Drugoff** – Number of arrests for crimes classified as drug-related felonies.

- **F_Sexoff** – Number of arrests for crimes classified as sex-related felonies.

- **F_ALLOTHER** – Other felony arrests not categorized under a specific type.

- **F_Totalsum** – Total number of felony arrests.

- **M_Totalsum** – Total number of misdemeanor arrests.

- **S_Total** – Total number of status offenses (e.g., curfew violations, truancy).

- **Sum Total** – Total number of all arrests (felony, misdemeanor, and status offenses combined).

+++ {"deletable": false, "editable": false}

<!-- BEGIN QUESTION -->

### <span style="color: blue;">Question One</span>

In 2–3 sentences, summarize what this data represents using the information above, the column labels, and the snippet of the data table.  
Explain what each row represents, and highlight any personal interests or questions you have about the data.

+++ {"tags": ["otter_answer_cell"]}

_Type your answer here, replacing this text._

+++ {"deletable": false, "editable": false}

<!-- END QUESTION -->

## First Look at Data

In the cell below, you'll find a widget that displays the number of drug arrests by year.  
This widget allows you to interact with the data and select the range of years you'd like to explore.

In the following cell, adjust the slider to examine trends in **all felony arrests** over the years.

```{code-cell} ipython3
display(widgets.interactive(lambda years : hp.plot_arrest(arrest, years), years= hp.year_slider))
```

# War on Drugs

## Introduction

The War on Drugs, launched in the 1970s and intensified during the 1980s, led to a surge in drug arrests by 1990 due to harsh federal policies such as the Anti-Drug Abuse Acts of 1986 and 1988.  
As a result, 1990 saw a spike in drug possession arrests—particularly among minority communities—contributing to the long-term trend of mass incarceration in the U.S.

The widget below allows you to explore drug arrest trends.  
Adjust the slider to see how the War on Drugs influenced overall drug arrests based on the timing of key legislation.

```{code-cell} ipython3
display(widgets.interactive(lambda years : hp.plot_drug_arrest(arrest, years), years= hp.year_slider))
```

## Race Impacts

### Crack vs. Powder Cocaine

Refer to your reading to learn how the War on Drugs impacted different racial groups, especially in relation to crack versus powder cocaine sentencing disparities.

In the next cell, use the dropdown to select the race you'd like to display, and try to observe the differences.  
You can also adjust the year range — we recommend setting it from 1980 to 1990.

```{code-cell} ipython3
display(widgets.interactive(lambda years, race : hp.drug_plot_race(arrest, years, race), years= hp.year_slider, race= hp.race_dropdown))
```

It's challenging to compare different racial groups using separate graphs, but as data scientists, this is a skill we need to develop.  
To make comparisons easier, we use overlapping graphs.

Using the widget below, select the races you want to graph together (be sure to view all of them together at the end).  
You can also adjust the year range — we recommend setting it from 1980 to 1990.

**⚠️ Warning:** The graph will only update if you’ve selected a race (or multiple races) *and* adjusted the year slider.  
Each time you make a new selection, be sure to move the year widget to trigger the corresponding plot.

```{code-cell} ipython3
display(widgets.VBox(hp.checkboxes), widgets.interactive(lambda years: hp.plot_races(arrest, years), years= hp.year_slider))
```

## Rate of Growth

Getting numbers is important. It's nice to see trends visually, but let’s also look at the statistics:  
How much did arrests increase for each racial group from the 1980s to 1989?

Use the dropdown below to display the percentage growth rates for each group.

```{code-cell} ipython3
display(widgets.interactive(lambda race : hp.drug_percentage_increase(arrest, race), race= hp.race_dropdown))
```

+++ {"deletable": false, "editable": false}

<!-- BEGIN QUESTION -->

### <span style="color: blue;">Question Two</span>

How did the War on Drugs impact incarceration numbers?  
How did it affect different racial groups?

Black people made up around 7%, white people made up 60%, and Hispanic people made up 25% of California's population in the 1980s and 1990s — how does this influence your understanding of the data?  
Answer in the cell below.

**Racial Demographics in California (1980s):**

- **White (Non-Hispanic):** Approximately 60%  
- **Hispanic or Latino:** Around 25%  
- **Black or African American:** About 7%  
- **Asian:** Roughly 4–5%

+++ {"tags": ["otter_answer_cell"]}

_Type your answer here, replacing this text._

+++ {"deletable": false, "editable": false}

<!-- END QUESTION -->

## 1990s Drug Arrest Drop

In the early 1990s, law enforcement in California and across the U.S. shifted its focus from low-level drug offenses to violent crime and gang-related activity.  
Additionally, California’s **Three Strikes Law** was enacted in 1994. As a result, while drug-related arrests declined, overall incarceration rates remained high due to the crackdown on repeat offenders.

Use the widget below to explore how total felony arrests changed over the years compared to drug-related felony arrests around this period (especially starting in 1994).  
See if you can identify the trend: a decline in drug-related arrests, while overall incarceration remained high.

```{code-cell} ipython3
display(widgets.interactive(lambda arrest_type, years : hp.plot_type_arrest(arrest,arrest_type, years), arrest_type= hp.arrest_dropdown, years=hp.year_slider))
```

Now to see the relationship between drug arrest vs violence arrest observe the violence arrest graph below

```{code-cell} ipython3
display(widgets.interactive(lambda years : hp.plot_violence(arrest, years, overlay= True), years=hp.year_slider))
```

## Arrest Rates Compared to Population Distribution

As mentioned earlier, we don’t get a complete picture of arrest patterns without considering the population distribution of each racial group.  
In this next section, we’ll work with a dataset that displays arrest rates for different racial groups compared to their share of the total population in each year.

Run the next cell to display the data.

```{code-cell} ipython3
extended_arrest= hp.type_arrest("Sum Total")
extended_arrest
```

Run the next cell and use the dropdown menu to view the percentage of arrests by race for different years.

```{code-cell} ipython3
display(widgets.interactive(lambda year : hp.bar_arrest(extended_arrest, year),  year=hp.year_dropdown))
```

It’s hard to see the changes over time in the distribution above,  
so run the next cell to view arrest data across multiple years for each race.

Use the slider to adjust the year range.  
To zoom in on the bars for each race, hover over the graph, then click and drag.  
To zoom out, just double-click.

```{code-cell} ipython3
display(widgets.interactive(lambda year : hp.bar_years(extended_arrest, year),  year=hp.year_selector))
```

+++ {"deletable": false, "editable": false}

<!-- BEGIN QUESTION -->

### <span style="color: blue;">Question Three</span>

Interact with the data by hovering over the bars to see specific values for each year and race.  
Identify the year when the **percent of arrests** was highest and lowest for each racial group.  
If comparing the bars is difficult, use the zoom-in function described above to make it easier.

Then, reflect on the following:  
How does the arrest rate by race compare to that group’s percentage of the total population?  
Are certain groups overrepresented or underrepresented in arrest data?

+++ {"tags": ["otter_answer_cell"]}

_Type your answer here, replacing this text._

+++ {"deletable": false, "editable": false}

<!-- END QUESTION -->

Lastly, we can compare the distributions of percent arrests by race using a box plot.  
Run the next cell to display it.

```{code-cell} ipython3
hp.box_arrest(extended_arrest)
```

+++ {"deletable": false, "editable": false}

<!-- BEGIN QUESTION -->

### <span style="color: blue;">Question Four</span>

Using data science, there are many ways to analyze data and identify patterns, as we did in this section.  
With the four methods of displaying data above (table, single bar chart, grouped bar chart, and box plot), consider the following questions and answer below:

1. Which display of data was your favorite and why? In what ways was it the most helpful, and where did it fall short?  
2. How did looking at the **percent per race** compare to just viewing the raw numbers?  
3. Which visualization made it easiest to compare trends over multiple years? Why?  
4. How did the box plot help in understanding the spread and variation in the data compared to the bar charts?  
5. If you were to analyze a different dataset, which of these methods would you choose, and would you include any additional visualizations?

+++ {"tags": ["otter_answer_cell"]}

_Type your answer here, replacing this text._

+++ {"deletable": false, "editable": false}

<!-- END QUESTION -->

# Redlining and Gentrification

Use the widget below to display felony arrests across different counties.  
Explore the data and make some initial observations. Consider the following:

- Are some counties consistently higher in arrests than others?  
- Do any trends appear over time?  
- Are there noticeable shifts in certain counties during specific years?

```{code-cell} ipython3
display(widgets.interactive(lambda x : hp.map_f_arrest(arrest, x), x=hp.county_dropdown))
```

Data science is a powerful tool, but it doesn’t always capture the full picture.  
In the case of gentrification and its effects on crime, for example, we might rely on county-level data to track trends—but these broader datasets can miss important nuances that are essential for a complete understanding.

County-level data may show a decrease in crime rates, but that doesn’t account for the displacement of marginalized communities, increased surveillance, or social upheaval occurring at the neighborhood level.  
To draw more accurate and truthful conclusions, data scientists need to recognize the gaps in their data and acknowledge the context in which these numbers exist.

Without considering underlying social dynamics—such as increased policing, changes in community structure, and economic pressures—data analysis can paint an incomplete or misleading picture.  
Understanding these limitations and the broader context is essential for making informed and responsible decisions.

---

### 📝 To-Do:

Choose one or two counties from the list below and read about how gentrification has impacted them.  
Then, use the widget above to explore the arrest data for those counties and make observations.

**Reflection Prompt:**  
How does the historical information provided align with the trends shown in the data? In what ways?

---

### County Information

1. **San Francisco County**  
   *Gentrification Start: Early 1990s*  
   Neighborhoods like the Mission District, Tenderloin, and Bayview-Hunters Point have seen significant gentrification, driven by tech industry growth. Rising housing costs and the influx of wealthier residents displaced long-time working-class communities.

2. **Los Angeles County**  
   *Gentrification Start: Early 2000s (accelerated in 2010s)*  
   Areas such as Downtown LA, Echo Park, Silver Lake, and Highland Park have experienced gentrification due to real estate development and an influx of young professionals and artists, transforming historically lower-income, immigrant, and minority communities.

3. **Oakland (Alameda County)**  
   *Gentrification Start: Mid-2000s*  
   Neighborhoods like West Oakland, Fruitvale, and Uptown have seen displacement as higher-income residents moved in due to rising costs in San Francisco.

4. **Santa Clara County (San Jose)**  
   *Gentrification Start: Early 2000s*  
   Driven by the tech boom in Silicon Valley, downtown San Jose and surrounding cities have seen rising housing demand and displacement in lower-income, predominantly Latino communities.

5. **San Diego County**  
   *Gentrification Start: Mid-2000s*  
   Areas like North Park, Logan Heights, and Barrio Logan have experienced gentrification as coastal property values increased, accelerating in the 2010s.

6. **Sacramento County**  
   *Gentrification Start: 2010s*  
   Neighborhoods such as Oak Park, Midtown, and the River District have seen rising rents and new developments, leading to the displacement of long-time residents.

7. **Riverside County**  
   *Gentrification Start: Mid-2010s*  
   Though not as widely known for gentrification, cities like Riverside and Moreno Valley are seeing increased development and rising rents, pushing lower-income residents out.

8. **Ventura County**  
   *Gentrification Start: Early 2000s*  
   Cities such as Oxnard and Ventura have seen shifts as people priced out of Los Angeles move in, affecting historically affordable, working-class Latino neighborhoods.

+++ {"deletable": false, "editable": false}

<!-- BEGIN QUESTION -->

### <span style="color: blue;">Question Five</span>

How does the historical information provided align with the trends shown in the data?  
In what ways do the arrest patterns reflect—or fail to reflect—the impacts of gentrification, displacement, or increased policing in the counties you explored?

+++ {"tags": ["otter_answer_cell"]}

_Type your answer here, replacing this text._

+++ {"deletable": false, "editable": false}

<!-- END QUESTION -->

### Sources  
https://en.wikipedia.org/wiki/Gentrification_of_San_Francisco
https://www.urbandisplacement.org/maps/los-angeles-gentrification-and-displacement/
https://www.urbandisplacement.org/wp-content/uploads/2021/08/alameda_final.pdf
https://clsepa.org/media-great-silicon-valley-land-grab/
https://storymaps.arcgis.com/stories/96ab5b185efb415c94024a9371295543
https://sacramentoappraisalblog.com/2022/01/26/gentrification-neighborhood-boundaries-and-bias/
https://journals.sagepub.com/doi/10.1177/0308518X211053642?icid=int.sj-abstract.similar-articles.4
https://foothilldragonpress.org/286831/a-latest/gentrification-and-its-impacts-on-ventura/

+++

## 📋 Post-Notebook Reflection Form

Thank you for completing the notebook! We’d love to hear your thoughts so we can continue improving and creating content that supports your learning.

Please take a few minutes to fill out this short reflection form:

👉 **[Click here to fill out the Reflection Form](https://docs.google.com/forms/d/e/1FAIpQLSd38uJNsiY_xV0S2LTu4zAZnaYPkphOMAvz4mNbngWuJYB7dg/viewform?usp=header)**

---

### 🧠 Why it matters:
Your feedback helps us understand:
- How clear and helpful the notebook was
- What you learned from the experience
- How your views on data science may have changed
- What topics you’d like to see in the future

This form is anonymous and should take less than 5 minutes to complete.

We appreciate your time and honest input! 💬

+++ {"deletable": false, "editable": false}

## Submission

Make sure you have run all cells in your notebook in order before running the cell below, so that all images/graphs appear in the output. The cell below will generate a zip file for you to submit. **Please save before exporting!**

```{code-cell} ipython3
:deletable: false
:editable: false

# Save your notebook first, then run this cell to export your submission.
grader.export()
```
