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

# Project 2: Cal EnviroScreen

+++

**Estimated Time**: 60-90 Minutes <br>
**Developers**: Bing Concepcion, James Geronimo

+++

## Table of Contents

+++

1. Introduction <br>
    1.1. Learning Objectives <br>
    1.2. Setup <br>
2. Data Preprocessing <br>
    2.1. Loading the Data <br>
    2.2. Checking for Missing Values <br>
    2.3. Filling the Missing Values <br>
    2.4. Defining our Objective <br>
3. Feature Engineering <br>
    3.1. Selecting Features <br>
    3.2. Setting Up X and y <br>
    3.3. Scaling Features <br>
4. Train-Test Split, Cross-Validation, Fit, and Predict <br>
    4.1 Splitting the Dataset <br>
    4.2 Training a Random Forest Classifier <br>
    4.3 Applying Cross-Vlidation <br>
    4.4 Fitting the Model <br>
    4.5 Predicting Labels <br>
5. Model Evaluation <br>
    5.1 Accuracy <br>
    5.2 Confusion Matrix <br>
    5.3 Classification Report <br>
    5.4 Feature Importances <br>
6. Final Thoughts

+++

---

+++

## 1. Introduction

+++

### 1.1. Learning Objectives

In Project 1, we explored the CalEnviroScreen dataset to perform exploratory data analysis (EDA) and understand environmental and demographic factors affecting communities. We examined key variables, visualized distributions, and identified patterns that highlight disparities in environmental risk.

In Project 2, we will use the insights we have gained to better our modeling task. In this notebook, we will build a machine learning model to predict whether a census tract falls into a **high risk** or **low risk** category based on environmental and demographic data. We will:

1. Perform data preprocessing and **feature engineering**
2. **Train** a classification model
3. Use **cross-validation** to assess our model's performance
4. **Evaluate** model **results** and discuss implications

+++

### 1.2. Setup

Below, we have imported some Python libraries that are necessary for this module. Make sure to run this cell before running any other code cells!

```{code-cell} ipython3
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

import ipywidgets as widgets
from IPython.display import display
```

---

+++

## 2. Data Preprocessing

+++

### 2.1 Loading the Data

**Question 2.1**: Let's first load our dataset `cal_enviro_screen.csv` into a variable called `ces`, and print out the shape of our `DataFrame`. Recall that we did this in Project 1, so feel free to refer back to it for guidance.

```{code-cell} ipython3
ces = pd.read_csv(...)
print(f"Shape of `ces`: {...}")

display(ces.head(5))
```

### 2.2 Checking for Missing Values

We are working with a lot of data, so it's important that we ensure it is clean enough to work with. 

**Question 2.2**: In the cell below, output a `Series` where the index is each column and the value is the number of missing values in that column. The `.isnull()` ([documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isnull.html)) function may be particularly helpful here.

```{code-cell} ipython3
...
```

### 2.3. Filling the Missing Values

Now that we have identified missing values in our dataset, we need to address them before proceeding with modeling. Handling missing data is crucial to ensure our analysis remains accurate and reliable. Depending on the nature of the missing values, we can either **drop rows or columns** with excessive missing data or impute values based on statistical measures such as the mean, median, or mode.

A simple fix to this problem is filling missing numerical values with the median of the quantitative column, as this best handles more skewed distributions. For categorical columns, we can fill them with the mode since it is the most common value. 

**Question 2.3**: Below, finish the code such that missing numerical values are filled with the column's median, and missing categorical values are filled with the column's mode. The output of the cell should be similar to the one above, but with all zeroes.

```{code-cell} ipython3
num_cols = ces.select_dtypes(include=['number']).columns
ces[num_cols] = ces[num_cols].fillna(ces[num_cols]...

cat_cols = ces.select_dtypes(include=['object']).columns
ces[cat_cols] = ces[cat_cols].fillna(ces[cat_cols]...)

...
```

### 2.4. Defining our Objective

With our data's missing values now tended to, we first must define what it means for a census tract to fall into either a high-risk or low-risk category. We will use the `"CES 4.0 Percentile"` feature as our target variable. However, recall that this variable is numerical (and you can prove this to yourself by checking the data yourself). In order to use it in a classification task, we must convert the variable into a binary classification problem. 

In these contexts, *high risk* often refers to values at or above the 75th percentile. Thus, we will define high risk as having a percentile greater than or equal to 75, and low risk as having a percentile less than 75. 

**Question 2.4**: Create a new column called `"high_risk"`, where the values are `True` if the percentile is greater than or equal to 75, and `False` otherwise.

```{code-cell} ipython3
ces['high_risk'] = ...

ces['high_risk']
```

---

+++

## 3. Feature Engineering

+++

### 3.1. Selecting Features

Now it is time to choose the features we would like in our model. Note that we will be using a Random Forest Classifier to carry out this classification task. It is important that we select features that have a significant relationship with the `"CES 4.0 Percentile"` column. 

Below, we've imported a function called `feature_selector` from `utils.py` that makes use of an interactive widget using `ipywidgets` so you can easily choose features with a click of a button (or multiple)! 

**Question 3.1**: For this part, select features that you think are appropriate for predicting whether or not a census tract is high risk or not. We highly encourage you to look back at the results you found from Project 1 to find meaningful features! Additionally, looking through the data dictionary of the dataset found in `ces_dictionary.pdf` will also be very useful.

```{code-cell} ipython3
from utils import feature_selector

features = ['Approximate Location', 'Asthma', 'Asthma Pctl', 'California County',
     'Cardiovascular Disease', 'Cardiovascular Disease Pctl', 'Census Tract', 'Cleanup Sites',
     'Cleanup Sites Pctl', 'Diesel PM', 'Diesel PM Pctl', 'Drinking Water', 'Drinking Water Pctl',
     'Education', 'Education Pctl', 'Groundwater Threats', 'Groundwater Threats Pctl',
     'Haz. Waste', 'Haz. Waste Pctl', 'Housing Burden', 'Housing Burden Pctl',
     'Imp. Water Bodies', 'Imp. Water Bodies Pctl', 'Latitude', 'Lead', 'Lead Pctl',
     'Linguistic Isolation', 'Linguistic Isolation Pctl', 'Longitude', 'Low Birth Weight',
     'Low Birth Weight Pctl', 'Ozone', 'Ozone Pctl', 'PM2.5', 'PM2.5 Pctl', 'Pesticides',
     'Pesticides Pctl', 'Pollution Burden', 'Pollution Burden Pctl', 'Pollution Burden Score',
     'Pop. Char.', 'Pop. Char. Pctl', 'Pop. Char. Score', 'Poverty', 'Poverty Pctl',
     'Solid Waste', 'Solid Waste Pctl', 'Total Population', 'Tox. Release', 'Tox. Release Pctl',
     'Traffic', 'Traffic Pctl', 'Unemployment', 'Unemployment Pctl', 'ZIP']

selected_features = []

feature_selector(features, selected_features)
```

### 3.2. Setting Up X and y

Now, we need to define our `X` and `y` variables. 

**Question 3.2**: Set `X` to be a `DataFrame` derived from `ces` with our `selected_features` from 3.1. Set `y` to be the `Series` of the variable we are trying to predict (`"high_risk"`)! 

```{code-cell} ipython3
X = ...
y = ...

print(f"Selected features: {selected_features}\n")
print(y.value_counts(normalize=True))
```

### 3.3 Scaling Features

With `X` and `y` now set up, the next step is to standardize our numeric features to ensure a consistent scale across all variables. Many machine learning models, particularly those relying on distance-based calculations (e.g., logistic regression, KNN), are sensitive to differences in feature magnitudes. Features like pollution scores and socioeconomic indicators may have vastly different ranges, which could bias the model if left unscaled.

**Question 3.3**: To address this, use `StandardScaler` ([documentation](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)) to transform each numeric feature to have a **mean of 0** and a **standard deviation of 1**. This process improves model convergence and prevents features with larger values from dominating those with smaller ones.

```{code-cell} ipython3
scaler = ...
X_scaled = ...
```

---

+++

## 4. Train-Test Split, Cross-Validation, Fit, and Predict

+++

### 4.1 Splitting the Dataset

To evaluate our model effectively, we first need to split the dataset into training and testing subsets. This will allow us to train the model on a majority of the data while preserving a portion to evaluate the model against unseen data.

**Question 4.1**: Using `train_test_split` ([documentation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)), use an **80-20 split**, reserving 80% of the data for training and 20% for testing. To ensure that the distribution of our target variable remains consistent across both subsets, set the `stratify` parameter set to `y`. This prevents us from having imbalanced splits, which could lead to misleading performance.

```{code-cell} ipython3
X_train, X_test, y_train, y_test = ...

print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
```

### 4.2 Defining a Random Forest Classifier

We'll start by defining a Random Forest Classifier, an ensemble learning method that leverages the predictions of multiple decision trees. This particular model will help reduce overfitting and improve generalization. Additionally, the model provides built-in feature importance scores, offering strong model interpretability. 

**Question 4.2**: Below, define a `RandomForestClassifier` ([documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)) under the variable `rf`. For reproducibility, set the `random_state` to 42. 

```{code-cell} ipython3
rf = ...
```

### 4.3 Applying Cross-Validation

Before assessing fitting the model and applying it to the test set, apply **cross-validation** to gauge how well it generalizes to unseen data. This will give us a more stable estimate of model performance by averaging results across multiple folds, rather than relying on a single split.

**Question 4.3**: In the cell below, use `StratifiedKFold` ([documentation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html)) so that each fold maintains the same **class distribution** as the overall dataset, similar to what we did with setting the `stratify` parameter from 4.1. For reproducibility, set the `random_state` to 42. Then, use `cross_val_score` ([documentation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html)) to evaluate model accuracy across each split.

```{code-cell} ipython3
cv = ...
cv_scores = ...

print(f"Cross-validation scores: {cv_scores}")
print(f"Cross-validation accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
```

### 4.4 Fitting the Model

After obtaining strong cross-validation scores, we’re confident that our model can generalize well to unseen data! The next step is to train the model on the entire training set to take full advantage of the data before making final predictions on the test set.

**Question 4.4**: Below, `fit` ([documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier.fit)) the model on the entire training set.

```{code-cell} ipython3
...
```

### 4.5 Predicting Labels

Having trained the model, we can use it to make predictions on the test set. Specifically, we’ll predict whether each census tract in `X_test` falls into the *high risk* or *low risk* category based on the environmental and demographic features.

**Question 4.5**: Using `predict` ([documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier.predict)), generate the model’s predicted labels for `X_test`, and define the predictions under `y_pred`. We’ll later compare with the true labels in y_test to evaluate performance.

```{code-cell} ipython3
y_pred = ...
```

---

+++

## 5. Model Evaluation

+++

### 5.1 Accuracy

With predictions in hand, we now evaluate how well the model performs on the **test set**—data it has never seen before. This step is crucial for understanding the model’s true generalization ability.

**Question 5.1**: Begin by calculating accuracy, which gives a simple overall measure of performance by showing the proportion of correct predictions. While it doesn’t capture the full story, it provides a useful first look at how the model is doing.

```{code-cell} ipython3
test_accuracy = ...

print(f"Test Accuracy: {test_accuracy:.4f}")
```

### 5.2 Confusion Matrix

To better understand our model’s predictions, visualize the confusion matrix, which breaks down the number of correct and incorrect classifications by class. This will allow us to identify where the model is making mistakes—such as false positives (areas incorrectly classified as *high risk*) and false negatives (*high risk* areas the model failed to catch).

**Question 5.2**: In plotting the confusion matrix, make sure to include clear axis labels and a descriptive title so it’s easy to interpret which predictions were correct and where the model struggled. Note that `confusion_matrix` ([documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)) and `sns.heatmap` ([documentation](https://seaborn.pydata.org/generated/seaborn.heatmap.html)) will be particularly useful here.

```{code-cell} ipython3
...
```

### 5.3 Classification Report

To get a more detailed view of model performance, generate a classification report. This report produces the following metrics:

- **Precision**: Of the areas predicted as *high risk*, how many truly are?
- **Recall**: Of the actual *high risk* areas, how many did the model correctly identify?
- **F1-score**: The harmonic mean of precision and recall.

**Question 5.3**: In the cell below, make use of `classification_report` ([documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html)) to generate the classfication report.

```{code-cell} ipython3
...
```

### 5.4 Feature Importances

To understand what’s driving the model’s predictions, examine feature importances from the trained Random Forest. This will tell us which environmental and socioeconomic factors contributed most to the classification of *high risk* vs. *low risk* areas.

**Question 5.4**: First, retrieve the feature importances from the `feature_importances_` attribute of `rf` ([documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier.feature_importances_)). Next, sort the values from highest to lowest. Then, visualize these importances using a bar plot, making sure to include axis labels and a title.

```{code-cell} ipython3
...
```

---

+++

## 6. Final Thoughts

+++

**Question 6.1**: What features did you end up using in your final model?
Were there any features you initially thought would be useful but didn’t improve performance or caused issues? How did you decide what to include or leave out?

+++

*Your answer here.*

+++

**Question 6.2**: In this context, which type of error is more acceptable—false positives or false negatives? How does this choice reflect the real-world implications of misclassifying a census tract’s risk level?

+++

*Your answer here.*

+++

**Question 6.3**: Which features were most important in your model, and do you think they align with real-world intuition about environmental or health risks? Were there any surprises in the importance rankings?

+++

*Your answer here.*

+++

---

+++

## Congratulations, you are finished with Project 2!
