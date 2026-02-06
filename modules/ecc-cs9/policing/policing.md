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

```{code-cell} ipython3
:deletable: false
:editable: false

# Initialize Otter
import otter
grader = otter.Notebook("policing.ipynb")
```

# The **Stanford Open Policing** Project

+++

**Estimated Time**: 30 Minutes <br>
**Developers**: Bing Concepcion and James Geronimo

+++

**Note**: This notebook is adapted from the open-source work of the [**Stanford Open Policing Project**](https://openpolicing.stanford.edu/).

+++

---

+++

## Table of Contents

+++

1. Background <br>
2. Setup, Sampling, and Subsetting <br>
3. Exploring Trends (Counts and Proportions)
4. Benchmark Analysis
5. Veil of Darkness Test

+++

---

+++

## 1. Background

+++

On a typical day in the United States, police officers make more than 50,000 traffic stops. The Stanford Open Policing Project is gathering, analyzing, and releasing records from millions of traffic stops by law enforcement agencies across the country. Their goal is to help researchers, journalists, and policymakers investigate and improve interactions between police and the public.

+++

Below, we've linked a YouTube video from Stanford's Computational Policy Lab, which provides a brief overview of the Stanford Open Policing Project. We highly encourage you to give it a watch, as content throughout this notebook will relate back to this video.

```{code-cell} ipython3
from IPython.display import YouTubeVideo
YouTubeVideo("iwOWcuFjNfw", width=640, height=360)
```

+++ {"deletable": false, "editable": false}

**Question 1.1**: Fill in the blank: Black and Hispanic drivers are ticketed, searched and arrested at __________ rates than white drivers.*

+++ {"deletable": false, "editable": false}

**Question 1.2**: Fill in the blank. 

Black and Hispanic drivers are searched on the basis of _______ evidence than white drivers.*

+++ {"deletable": false, "editable": false}

**Question 1.3**: What effect did 8 states legalizing recreational marijuana have on the number of searches? Why?

+++

---

+++

## 2. Setup, Sampling, and Subsetting

+++

Just importing some libraries we'll need for the analysis we will partake in this notebook.

```{code-cell} ipython3
import pandas as pd
import numpy as np

from suntime import Sun
from datetime import datetime, timedelta

import seaborn as sns
import matplotlib.pyplot as plt

import statsmodels.formula.api as smf
```

+++ {"deletable": false, "editable": false}

You may have noticed that a dataset was not given for the assignment. That's because you will be retrieving it yourself! 

**Question 2.1**: From the project's [Data page](https://openpolicing.stanford.edu/data/), download the *CSV* file corresponding to *Los Angeles, California*, and drag it into the current working directory of this notebook. Once you've successfully done this, the cell below should generate a `DataFrame`.

```{code-cell} ipython3
stops = ...
stops.head()
```

```{code-cell} ipython3
:deletable: false
:editable: false

grader.check("q4")
```

+++ {"deletable": false, "editable": false}

Before diving into any heavy-duty analysis, it's important to understand the size of the dataset we're working with.

**Question 2.2**: Calculate the number of rows in `stops`.

```{code-cell} ipython3
num_rows = ...
num_rows
```

```{code-cell} ipython3
:deletable: false
:editable: false

grader.check("q5")
```

+++ {"deletable": false, "editable": false}

Our dataset contains over 5 million traffic stops. Working with a dataset of this size can quickly become computationally expensive. It can slow down operations like filtering, joining, and plotting, especially on machines with limited memory.

To make our workflow more efficient without sacrificing the integrity of our analysis, we'll take a random 10% sample of the data. This allows us to get a reliable sense of overall patterns and relationships, without requiring full-scale processing of the entire dataset.

> Of course, for final results or publication-level accuracy, we’d want to use the full dataset—but for exploratory analysis, a random sample often gets us most of the way there.

**Question 2.3**: Generate a 10% random sample of using `stops`. The `sample` function ([documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html)) will be particuarly useful here. Please set `random_state` to 42 for reproducibility.

```{code-cell} ipython3
stops_sample = ...
len(stops_sample)
```

```{code-cell} ipython3
:deletable: false
:editable: false

grader.check("q6")
```

+++ {"deletable": false, "editable": false}

**Question 2.4**: What is the granularity of the data? Does this change at all by the random sample we just did?

+++ {"deletable": false, "editable": false}

**Question 2.5**: Take a look at the provided feature set that came with the data. What additional feature would be interesting to add in this dataset? How might it add to an analysis?

+++ {"deletable": false, "editable": false}

Our dataset spans multiple years. But after some digging, you'll notice that we only have partial data for 2018, which may bias our analysis. To ensure consistency, we’ll focus only on the years we have complete data for, 2010–2017.

**Question 2.6**: Extract the year from the date column and filter accordingly. You'll first want to convert the data in the `"date"` column to a `datatime` type. `to_datetime` ([documentation](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html)). Then, create a new column `"year"`, which is simply the year at that given row. The `dt` [documentation](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.html) will be helpful here, and note that a `year` attribute does exist. 

```{code-cell} ipython3
stops_sample['date'] = ...
stops_sample['year'] = ...
stops_sample = ...
stops_sample.head()
```

```{code-cell} ipython3
:deletable: false
:editable: false

grader.check("q9")
```

+++ {"deletable": false, "editable": false}

The dataset includes both pedestrian and vehicular stops. For this notebook, we'll be focusing our analysis on traffic enforcement, so we’ll zoom in on just the vehicular stops for now.

> Do note that we can perform the same analysis on vehicular stops as we do to pedestrian stops. We are simply going to remove pedestrian stops for consistency of our analysis and since vehicular stops were the primary motivation of the Stanford Open Policing Project.

**Question 2.7**: Filter the data so `stops_sample` only contains rows corresponding to vehicular stops.

```{code-cell} ipython3
stops_sample = stops_sample[stops_sample['type'] == 'vehicular']
len(stops_sample)
```

```{code-cell} ipython3
:deletable: false
:editable: false

grader.check("q10")
```

---

+++

## 3. Exploring Trends (Counts and Proportions)

+++ {"deletable": false, "editable": false}

Now that we’ve filtered to just vehicular stops from 2010–2017, let’s take a look at how the number of stops changed over time and whether those patterns differ by race.

**Question 3.1**: Using the `"year"` column we defined in Question 2.6, get the count for the number of stops per year. Make sure to sort your result by year, starting at 2010 and ending at 2017.

```{code-cell} ipython3
stops_per_year = ...
stops_per_year
```

```{code-cell} ipython3
:deletable: false
:editable: false

grader.check("q11")
```

+++ {"deletable": false, "editable": false}

**Question 3.2**: Using similar logic as Question 3.1, calculate the stop counts by race.

```{code-cell} ipython3
stops_by_race = ...
stops_by_race
```

```{code-cell} ipython3
:deletable: false
:editable: false

grader.check("q12")
```

+++ {"deletable": false, "editable": false}

So far, we've narrowed our dataset to a manageable sample of vehicular stops, and carried out the calculations to understand the volume of traffic stops over time and by race.

It's time to build some data visualizations that will provide a strong indicator for trends and disparities. 

**Question 3.3**: Build a line plot that visualizes the number of stops of each race per year. You'll first want to group by the `"year"` and `"subject_race"` columns and aggregate the data somehow to generate a new `DataFrame` called `stops_by_year_race`.

```{code-cell} ipython3
stops_by_year_race = ...

plt.figure(figsize=(10, 6))
sns.lineplot(
    data= ...
    x= ...
    y= ...
    hue= ...
    marker='o'
)
plt.title('Counts of Traffic Stops by Year and Race')
plt.xlabel('Year')
plt.ylabel('Number of Stops')
plt.legend(title='Race')
plt.grid(True)
plt.show()
```

+++ {"deletable": false, "editable": false}

**Question 3.4**: Are there any significant disparities in the plot above?

+++ {"deletable": false, "editable": false}

**Question 3.5**: Name at least one limitation of our data/plot, and explain how you could circumvent this.

+++ {"deletable": false, "editable": false}

So far, we’ve looked at the raw number of stops each year, broken down by race. While this helps us understand absolute trends, it doesn’t tell us everything.

> Imagine one year had a spike in overall stops — it would likely inflate all racial group counts, even if their relative share of stops didn’t change.

That’s why we now turn to proportional analysis. Instead of asking:

> "How many Black drivers were stopped in 2016?" <br> We now ask: "What percentage of all drivers stopped in 2016 were Black?"

This helps us determine whether certain groups were being stopped more or less often relative to others, regardless of how much total enforcement was happening.

**Question 3.6**: Below, we've defined a `"total_stops_in_year"` column, which is the total number of stops conduct in each year. Use this to calculate a new column called `"prop_stop"` — the proportion of stops each race accounted for within each year. Then, visualize these proportions across years in a line plot.

```{code-cell} ipython3
stops_by_year_race['total_stops_in_year'] = ...
stops_by_year_race.head()
```

```{code-cell} ipython3
stops_by_year_race['prop_stops'] = ...

plt.figure(figsize=(10, 6))
sns.lineplot(
    data=stops_by_year_race,
    x='year',
    y='prop_stops',
    hue='subject_race',
    marker='o'
)

plt.title('Proportion of Traffic Stops by Race Over Time (Sample)')
plt.xlabel('Year')
plt.ylabel('Proportion of Stops')
plt.legend(title='Race')
plt.grid(True)
plt.show()
```

```{code-cell} ipython3
:deletable: false
:editable: false

grader.check("q16")
```

+++ {"deletable": false, "editable": false}

**Question 3.7**: What differences do you see between the "count" and "proportion" plots? 

+++ {"deletable": false, "editable": false}

**Question 3.8**: Name at least one aspect of either visualization that surprised you the most.

+++

---

+++

## 4. Benchmark Analysis

+++

Earlier, we examined how traffic stops were distributed by race. But to interpret those results meaningfully, we need a baseline. To do this, we will compare the racial makeup of stops to the racial demographics of Los Angeles.

Below, we've provided the Los Angeles population demographic from 2017 and stored it in the `DataFrame` `population_2017`. These numbers were taken from [Census Reporter](https://censusreporter.org/profiles/14000US06037201700-census-tract-2017-los-angeles-ca/). 

```{code-cell} ipython3
population_2017 = pd.DataFrame({
    'subject_race': [
        'white', 'black', 'asian/pacific islander', 'other', 'hispanic'
    ],
    'num_people': [
        1092687, 316317, 456460+4536, 24178+6005+135551, 1822163
    ]
})

population_2017['population_prop'] = population_2017['num_people'] / population_2017['num_people'].sum()
population_2017
```

+++ {"deletable": false, "editable": false}

Before we use `population_2017` we need to filter our data to the year 2017.

**Question 4.1**: Filter the `stops_by_year_race` to 2017 and assign it to `stops_2017`.

```{code-cell} ipython3
stops_2017 = ...
stops_2017
```

```{code-cell} ipython3
:deletable: false
:editable: false

grader.check("q19")
```

+++ {"deletable": false, "editable": false}

Now that we've filtered our dataset to only stops in 2017, we can now get ready to compare stops for each racial group relative to their population proportions.


**Question 4.2**: Let's merge these `stops_2017` and `population_2017` by the `subject_race` column and assign this merged DataFrame to `benchmark_df`. Then, create a `stop_rate_per_person` column which shows the number of stops per person for each racial group.

```{code-cell} ipython3
benchmark_df = ...
benchmark_df['stop_rate_per_person'] = ...
benchmark_df
```

```{code-cell} ipython3
:deletable: false
:editable: false

grader.check("q20")
```

+++ {"deletable": false, "editable": false}

Numerically, we see some signficant differences amongst the propoprtion of stops to the stop rate per person. Let's visualize the stop rate per person so we can more clearly see these differences.

**Question 4.3**: Create a bar plot with the x-axis representing the racial groups and the y-axis representing the corresponding stop rate per person. Be sure to provide appropriate axis labels and title!

```{code-cell} ipython3
plt.figure(figsize=(10, 6))

sns.barplot(
    data= ...
    x= ...
    y= ...
)

plt.title('Stop Rate per Person by Race (2017, Sampled Data)')
plt.xlabel('Race')
plt.ylabel('Stop Rate (Stops per Person)')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()
```

+++ {"deletable": false, "editable": false}

**Question 4.4**: Based on the stop rate per person bar plot, what insights can you draw about how race affects an individuals chance of being stopped in Los Angeles? Which racial groups are stopped at disproportionately high rates? 

+++ {"deletable": false, "editable": false}

**Question 4.5**: How does the stop rate per person plot differ from early graphs looking at number and proportions of stops by race? Why is it important to account for population size, rather than just looking at raw counts or proportions?

+++

---

+++

## 5. Veil of Darkness Test

+++

The **Veil of Darkness** hypothesis explores whether the proportion of Black drivers that are stopped changes at all when it becomes dark. This is proposed under the idea that officers can no longer perceive race before making the stop.

We essentially explore through this test whether or not racial bias exists, given we find a signficant difference in the proportion of Black drivers stopped at night. 

+++ {"deletable": false, "editable": false}

In order to perform this analysis, we need to know exactly when it was light and dark on each date in our dataset. Note that we can't simply assume all days get dark at a specific time because the hours of daylight change across seasons. Thus, we must calculate the sunrise and sunset times for each unique date.

**Question 5.1**: We have already defined the geographic coordinates of Los Angeles and the solar calculator you will need to use. Your task is to compute the sunrise and sunset times for each date to build a DataFrame `sun_times`, which stores the local sunrise and sunset time for each stop date.

```{code-cell} ipython3
# Coordinates for Los Angeles
center_lat = 34.0549
center_lng = -118.2426

# Solar calculator
sun = ...

# Get sun times for each unique date
sun_times = []
dates = stops_sample['date'].unique()
for date in dates:
    sunrise_utc = ...
    sunset_utc = ...
    sunrise_la = ...
    sunset_la = ...
    sun_times.append({'date': date, 'sunrise': sunrise_la, 'sunset': sunset_la}) 
sun_times = ...

sun_times.head()
```

```{code-cell} ipython3
:deletable: false
:editable: false

grader.check("q24")
```

+++ {"deletable": false, "editable": false}

Now that we have sunrise and sunset times for each unique date, we can determine whether a specific stop in our `stops_sample` DataFrame happened during daylight or darkness.

**Question 5.2**: Join the sunrise and sunset times to our `stops_sample` DataFrame.

```{code-cell} ipython3
# Merge sun times with stops
vod_stops = stops_sample.merge(sun_times, on='date', how='left')
vod_stops.head()
```

+++ {"deletable": false, "editable": false}

`vod_stops` is a DataFrame that has information on each of the stops from `stops_sample` in addition to each day's sunrise and sunset times. We should define what stops were made in the dark to help us conduct the analysis. We have pre-defined the minute values for each of the stop, sunrise, and sunset times. 

**Question 5.3**: In `vod_stops`, create a `"is_dark"` column that is set to `True` when `stop_minute` is strictly greater than `sunset_minute` and strictly less than `sunrise_minute`, but is `False` otherwise.

```{code-cell} ipython3
# Convert stop, sunrise, and sunset time to minutes
vod_stops['stop_minute'] = pd.to_datetime(vod_stops['time'], format='%H:%M:%S').dt.hour * 60 + pd.to_datetime(vod_stops['time'], format= ...
vod_stops['sunrise_minute'] = pd.to_datetime(vod_stops['sunrise'], format='%H:%M:%S').dt.hour * 60 + pd.to_datetime(vod_stops['sunrise'], format= ...
vod_stops['sunset_minute'] = pd.to_datetime(vod_stops['sunset'], format='%H:%M:%S').dt.hour * 60 + pd.to_datetime(vod_stops['sunset'], format= ...

# Define "is_dark" column
vod_stops['is_dark'] = (vod_stops['stop_minute'] > (vod_stops['sunset_minute'] + 60)) | \
                        ...
vod_stops.head()
```

```{code-cell} ipython3
:deletable: false
:editable: false

grader.check("q26")
```

+++ {"deletable": false, "editable": false}

Now that we've determined whether each stop occurred during darkness or daylight, we're ready to set up our Veil of Darkness analysis.

**Question 5.4**: Filter `vod_stops` to only include stops involving Black and White drivers to simplify our analysis to two groups. Then, create a new indicator column `is_black` that is `1` if the stopped driver was Blakc, and `0` if the stopped driver was White. After correctly implementing these instructions and running the cell, a "Logit Regression Results" table should appear.

```{code-cell} ipython3
vod_stops = ...
vod_stops['is_black'] = (vod_stops['subject_race'] = ...

# Logistic regression model
vod_stops['is_dark'] = ...
model = ...
model.summary()
```

```{code-cell} ipython3
:deletable: false
:editable: false

grader.check("q27")
```

+++ {"deletable": false, "editable": false}

**Question 5.5**: What does the statistically significant coefficient on `is_dark` suggest about how race may influence traffic stops after dark?

+++ {"deletable": false, "editable": false}

**Question 5.6**: How does this finding compare to the original Veil of Darkness hypothesis?

+++

---

+++

Hurray! You're done with this notebook!

+++ {"deletable": false, "editable": false}

## Submission

Make sure you have run all cells in your notebook in order before running the cell below, so that all images/graphs appear in the output. The cell below will generate a zip file for you to submit. **Please save before exporting!**

These are some submission instructions.

```{code-cell} ipython3
:deletable: false
:editable: false

# Save your notebook first, then run this cell to export your submission.
grader.export(run_tests=True)
```
