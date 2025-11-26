---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.18.1
kernelspec:
  name: python3
  display_name: Python 3
---

+++ {"id": "jHf3y_y3wLxa"}

# Lab: Linear Regression Modeling and Sklearn

In this lab, we will walk through the process of:
1. Use Linear Regression for numerical prediction tasks, such as estimating housing prices. Understand Linear Regression as a supervised learning approach and discuss why it is an appropriate choice for this task.
2. Define and understand the loss and risk functions associated with Linear Regression, focusing on Root Mean Squared Error (RMSE).
3. Begin with a constant model as a baseline, then introduce a simple linear model using `scikit-learn` package. Interpret the coefficients and compare the performance of these two models. Progress to multiple linear regression. Compare all three models, discussing training and test errors, and make observations on model performance. Introduce and explain concepts of underfitting and overfitting.
4. Experiment with feature selection and document your observations.

```{code-cell}
:id: Rx-CFAp6ZOaN

# Run this cell to import important packages for this lab
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
```

+++ {"id": "PJS5mj5IE3UQ"}

-------------------------------------------
## 1. Introduction
For this lab, we will use a toy dataset to predict housing prices in California with data provided by `sklearn.datasets` package. There are more interesting datasets in the package if you want to explore them during your free time!

+++ {"id": "tmr7DhISFkWz"}

Run the following cell to load data.

```{code-cell}
:id: WIDyXosteKnM

# Run this cell
from sklearn.datasets import fetch_california_housing
california_housing = fetch_california_housing(as_frame=True)
```

+++ {"id": "hkmnaHB8Gkel"}

Some methods we can use to explore this dataset:
- `data`: The independent variables/features (X)
- `target`: the response vector (Y)
- `feature_names`: The column names
- `DESCR`: A full description of the data, and
- `frame`: full DataFrame with `data` and `target`

For more information, refer to this [document](https://scikit-learn.org/1.0/modules/generated/sklearn.datasets.fetch_california_housing.html#sklearn.datasets.fetch_california_housing)

+++ {"id": "1heT3rFMH6w9"}

Now, we use `DESCR` method to undertand what each columns represents. Run the cell below.

```{code-cell}
:id: RlMNKP8KGiSM

# Run this cell
print(california_housing.DESCR)
```

+++ {"id": "rqus_k8rz4d5"}

**Question**: What is the granularity of this dataset? Specifically, what does each row represent?

+++ {"id": "egUWk8PWPK6K"}

*Type your answer here, replacing this text.*

+++ {"id": "FCS1hGoZIcud"}

Let's store our full DataFrame as `california_housing`

```{code-cell}
:id: heqB5DOjeSDv

# Run this cell
california_housing = california_housing.frame
california_housing.head()
```

+++ {"id": "TeHvyw-gLeZc"}

**Question**:
What is the target variable we aim to predict? What are the input features? Identify at least two features that you believe would be useful for this prediction task, and explain why they would add value.

+++ {"id": "N693weYTPNlm"}

*Type your answer here, replacing this text.*

+++ {"id": "ECNm8I1aVnr4"}

------------------------------------------------------------
### 2. Data Overview
First, we have to understand what our data look like before picking a model.

+++ {"id": "8ydzl0XOXjXR"}

**Question 2**:
Fill in '...' below in the cell to plot the histogram of the response variable (Y), which is `MedHouseVal`. You can either use `seaborn` or `matplotlib.pyplot` package. Make sure to have a clear title and labels for each axis

```{code-cell}
:id: LqCkyFbhYGC7

# TO-DO: Plot the histogram of MedHouseVal
# Plot the distribution of response variable
...
```

+++ {"id": "o8-uS3m5YTma"}

**Question 3**: To add more information, fill in the code below to produce statistical summary for the response variable.

```{code-cell}
:id: Q9XZiwmKYinP

# TO-DO: Produce statistical summary for MedHouseVal
# Hint: using a pandas function on a column of `california_housing` DataFrame.
# Can you think of which column and which function to use?
statistical_summary = california_housing[...]...
statistical_summary
```

+++ {"id": "qfgqgvpYZOJI"}

**Question 4**: After reviewing the statistical summary and the histogram, what patterns or trends do you notice? Do you observe any unusual or unexpected values?"

+++ {"id": "kz6WjYFePQmi"}

*Type your answer here, replacing this text.*

+++ {"id": "mF56uwBVaz_L"}

**Question 5**: Create a visualization of the distribution for one of the features in the dataset. What do you observe about the distribution of this variable?

```{code-cell}
:id: aCgzez4cbS4G

# TO-DO: Visualize a distribution of another variable
...
```

+++ {"id": "D0ugxv7a2ze8"}

-------------------------------------------------------------------
### 3. Modeling Process
As a reminder, when we're building a model, there are a few key steps we follow to ensure it makes reliable predictions. Here is the process:
- Define a model
- Choose a loss function and calculate the average loss (risk) on our dataset
- Find the best value of $\theta$, known as $\hat{\theta}$, that minimizes the loss. There can be multiple such $\theta$ values (not covered in this lab).
- Evaluate the model performance

+++ {"id": "RqwITS5gV1a9"}

#### Define a Model
In this lab, we'll use Linear Regression to predict the median house value for California districts. Linear Regression is a suitable choice because it’s a powerful, interpretable method for modeling relationships between variables, especially when our goal is to predict a continuous numeric outcome, like housing prices. It allows us to see how each factor, such as median income or average number of rooms, contributes to the target prediction.

The general form of a Linear Regression model can be written as:

$$
y = \theta_0 + \theta_1 x_1 + \theta_2 x_2 + \dots + \theta_n x_n
$$

where:
- $ y $ is the target variable (in this case, median house value),
- $ \theta_0 $ is the intercept,
- $ \theta_1, \theta_2, \dots, \theta_n $ are the coefficients for each predictor variable $ x_1, x_2, \dots, x_n $,



+++ {"id": "mLpPhQgw15Y4"}

Before building our models, we’ll split our dataset into a training set and a test set. For the first half of the lab, we’ll focus on the training set to train our model and evaluate its risk (or error).

```{code-cell}
:id: HfPPivE0qQwn

# Run this cell; no TO-DO
# Spliting train and test
from sklearn.model_selection import train_test_split
train, test = train_test_split(california_housing, test_size=0.2, random_state=42)
```

+++ {"id": "mVT7jCNyWBFl"}

#### Choose Risk Function and Evaluate Model Performance
The next step is to define our risk function, which represents the average loss over all data points in our dataset. For Linear Regression, we typically use Root Mean Squared Error (RMSE) as the loss function, which provides a measure of the model's prediction error in the same units as the target variable.

In mathematical terms, the RMSE can be written as:

$$
\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2}
$$

where:
- $ N $ is the number of data points,
- $ y_i $ is the actual value of the target variable for the $ i $-th data point,
- $ \hat{y}_i $ is the predicted value for the $ i $-th data point.

This function helps us quantify the average difference between predicted and actual values, making it a useful metric to assess the accuracy of our Linear Regression model.





+++ {"id": "fh1-853cqUbt"}

**Question**: Write a Python function to calculate the Root Mean Squared Error (RMSE), which takes y_true (actual values) and y_pred (predicted values) as inputs and returns a single RMSE value.

*Hint: Use a numpy function on arrays for efficient computation instead of a for loop.*

```{code-cell}
:id: 7mTtN8VSqh_S

def rmse(y_true, y_pred):
  """
  Calculate the Root Mean Squared Error (RMSE) between actual and predicted values.

  Parameters:
  y_true (array-like): Actual values.
  y_pred (array-like): Predicted values.

  Returns:
  float: The RMSE value, representing the average deviation of predictions from actual values.
  """
  return ...
```

+++ {"id": "u2Q97Q0Nqocl"}

##### 1. Constant Model: $y = \theta_0$

+++ {"id": "jzi3cn7n38AU"}

We start with the simplest model, called the constant model, which predicts the same value for every data point. In this case, we use the average `MedHouseVal` as our prediction. Why? Because using the average as a baseline provides a simple reference point, giving us a measure of overall central tendency. This helps us understand how much our more complex models improve over simply guessing the average value for all predictions.

+++ {"id": "Qn2znjG4q5M8"}

**Question**: store this constant model to variable `constant_model`. Make sure to use `train` data to take average on column `MedHouseVal`

```{code-cell}
:id: fuWBus6wrF7R

# TO-DO: calculate average `MedHouseVal`
constant_model = train[...]...
constant_model
```

+++ {"id": "B6AVh-dFtAKV"}

Next, we’ll visualize the constant model alongside our training data. This will help us see how well the average value represents the data and serves as a baseline for comparison with more complex models.



```{code-cell}
:id: rPH63rjItUTQ

# Run this cell; no TO-DO
# Run this cell; no TO-DO
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=train["MedInc"],
    y=train["MedHouseVal"],
    mode="markers",
    name="data"
))
fig.add_trace(go.Scatter(
    x=train["MedInc"],
    y=constant_model*np.ones(len(train)),
    mode="lines",
    name="constant model"
))
```

+++ {"id": "lkTyFvmztWUb"}

**Question**: Use your `rmse` function to calculate the risk (RMSE) of our constant model on the training data.

*Hint: Pass the actual values of `MedHouseVal` in the `train` data and the constant model value to your `rmse` function.*

```{code-cell}
:id: wR6OmlwZrM8S

# TODO: Calculate RSME of our constant model on the training data
rmse_dict = {}
rmse_dict["constant"] = rmse(train[...], ...)
rmse_dict
```

+++ {"id": "VfNarvJBrain"}

##### 2. Simple Model Using Median Income

In this step, we’ll build a simple linear model that predicts `MedHouseVal` (median house value) based on `MedInc` (median income) in the dataset. This model has the form:

$$
y = \theta_0 + \theta_1 \cdot \text{MedInc}
$$

where:
- $y$ is the predicted median house value,
- $\theta_0$ is the intercept (a constant term),
- $\theta_1$ is the coefficient for `MedInc`, representing the effect of median income on the predicted house value.

This approach allows us to examine how well a single feature (median income) explains variations in house value. By fitting this model, we can see if there’s a strong linear relationship between income and house prices in the data.

```{code-cell}
:id: IIFLQtaV9DAo

# Run this celll; no TO-DO
# Scatter plot between `MeHouseVal` and `MedInc`
sns.scatterplot(data=train, x="MedInc", y="MedHouseVal")
plt.title("Median Income vs. Median House Value")
plt.xlabel("Median Income")
plt.ylabel("Median House Value")
plt.show()
```

+++ {"id": "aQ1MX-zy9gZx"}

Next, we will use `sklearn` to build our Linear Regression.

+++ {"id": "dWC2L43Jd6rb"}

###### Introduction to sklearn

To fit a linear regression model, we will use `sklearn`, an industry-standard package for machine learning applications. Because it is application-specific, `sklearn` is often faster and more robust than the analytical methods. Note that `scikit-learn` and `sklearn` refers to the same package, but it can only be imported under the name `sklearn`.

To use `sklearn`:

- Create an `sklearn` object.
- Fit the object to data.
- Analyze fit or call `predict`.

+++ {"id": "My2wyGqOeBaP"}

**1. Create object.**

We first create a LinearRegression object. Here's the sklearn [documentation.](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) Note that by default, the object will include an intercept term when fitting.

Here, model is like a "blank slate" for a linear model.

```{code-cell}
:id: veX5oRo0svSV

# Run this cell, no TO DO
# Create LinearRegression object
from sklearn.linear_model import LinearRegression
simple_model = LinearRegression()
```

+++ {"id": "Wy-mllFgeXQQ"}

**2. Fit the object to data.**

Now, we need to tell model to "fit" itself to the data. Essentially, it creates a risk function and finds the parameter(s) that minimize that risk.

Note: X needs to be a matrix (or DataFrame), as opposed to a single array (or Series) when running `model.fit`. This is because `sklearn.linear_model` is robust enough to be used for multiple regression, which we will look at later in this lab. This is why we use the double square brackets around `MedInc` when passing in the argument for X.

```{code-cell}
:id: 7fDaO-0MegFg

# Run this cell; no TO DO
# Fit the object to data
simple_model.fit(train[["MedInc"]], train["MedHouseVal"])
```

+++ {"id": "osVhle2Yegfd"}

**3. Analyze fit.**

Now that the model exists, we can look at the intercept and coeffients of the model.

```{code-cell}
:id: c2cY28AIfHk-

# Intepret the model by looking at intercept and coefficient
simple_model.intercept_, simple_model.coef_
```

+++ {"id": "LhqyKel9_AWT"}

**Question**: What does coefficient mean? Fill in the blank

"As the value of MedInc _________ *(increases/decreases)* by one unit, the predicted MedHouseVal ___________ *(increases/decreases)* by approximately ________ units. This coefficient suggests a ________*(positive/negative)* relationship between median income and median house value."

+++ {"id": "r_wtC0MZPW5l"}

*Type your answer here, replacing this text.*

+++ {"id": "5WLbBsrUfH-X"}

To use the sklearn linear regression model to make predictions, you can use the model.predict method.

```{code-cell}
:id: uw7Lx_VIscju

# Run this cell, no TO-DO
# Store our predctions for `MedHouseVal` on train data using `simple_model`
simple_predicted_train = simple_model.predict(train[["MedInc"]])
```

+++ {"id": "shzHtAc4Bojx"}

Let's visualize our predictions using simple model on training data

```{code-cell}
:id: FLbe7fzeBmy7

# Run this cell; no TO-DO
fig.add_trace(go.Scatter(
    x=train["MedInc"],
    y=simple_predicted_train,
    mode="lines",
    name="simple model"
))
fig.update_layout(
    xaxis_title="MedInc",
    yaxis_title="MedHouseVal"

)
```

+++ {"id": "7H-G9sCRB8Mn"}

**Question**: Caldulate RMSE for our simple model on `train` data

```{code-cell}
:id: 6oOk7U4Eu3Rp

# TO-DO: Caldulate RMSE for our simple model on `train` data
rmse_dict["simple"] = rmse(train[...],...)
```

```{code-cell}
:id: 0KIkYMOCvBgc

# Run this cell; no TO-DO
# Compare two models
rmse_dict
```

+++ {"id": "zaeghgoRvF-c"}

**Question**: Compare the errors between the constant model and the simple model. Note that these are the errors calculated on our training data, commonly referred to as training errors. What differences do you observe between the two models’ training errors, and what might these differences indicate about each model's performance?

+++ {"id": "pSGxDysCPY5e"}

*Type your answer here, replacing this text.*

+++ {"id": "fsgrJdjEteiY"}

#### 3. Multiple Linear Regression with Median Income and Average Rooms

In this step, we’ll expand our model to include two features: `MedInc` (Median Income) and `AveRooms` (Average Rooms). This model, known as multiple linear regression, helps us understand the combined effect of both income and average number of rooms on median house values.

The model’s equation can be written as:

$$
y = \theta_0 + \theta_1 \cdot \text{MedInc} + \theta_2 \cdot \text{AveRooms}
$$

where:
- $y$ is the predicted median house value (`MedHouseVal`),
- $\theta_0$ is the intercept, representing the baseline prediction when both `MedInc` and `AveRooms` are zero,
- $\theta_1$ is the coefficient for `MedInc`, indicating how changes in median income affect the house value, holding `AveRooms` constant,
- $\theta_2$ is the coefficient for `AveRooms`, representing how changes in the average number of rooms impact the house value, holding `MedInc` constant.

Including both `MedInc` and `AveRooms` allows us to capture a more complex relationship between features and target, potentially improving prediction accuracy. We’ll fit this model and then evaluate how well it performs compared to the previous models.

```{code-cell}
:id: 0W_6_PEktz3u

# Create LinearRegression object
multiple_model = ...

# Fit the object to data
....fit(train[[...]], train[...])
```

```{code-cell}
:id: aUavygkAuh8q

# Look at the intercepts and cooefiences
multiple_model.intercept_, multiple_model.coef_
```

+++ {"id": "wHiezD_sumU1"}

**Question**: Interpret the coefficients of the multiple linear regression model. What relationships do each of the coefficients have with `MedHouseVal`? Additionally, how does the magnitude of each coefficient impact the interpretation?

+++ {"id": "by8wReawPHhy"}

*Type your answer here, replacing this text.*

+++ {"id": "BcnvTgaVD6O6"}

**Question**: Use the multiple linear regression model to predict `MedHouseVal` on the `train` data and calculate the RMSE for the predictions on this training data.

```{code-cell}
:id: NeGtF7iNuw-C

# TO-DO: Use multiple linear regression to predict MedHouseVal in training data
multiple_predicted_train = ....predict(train[[...]])
```

```{code-cell}
:id: JqAsy9FDu0VR

# TO-DO: Calculate RSME for this multiple_model on training data
rmse_dict["multiple"] = ...
```

```{code-cell}
:id: d8DreDJlvdon

# Run this cell, no TO-DO
# Compare three models
rmse_dict
```

+++ {"id": "5TLrcFqbvhlV"}

-----------------------------
### Your model, add one more on your choice
**Task**: Build a multiple linear regression model using `MedInc`, `AveRooms`, and one additional feature of your choice. Follow the modeling process using `sklearn`, train the model on the `train` data, and then use it to predict MedHouseVal for the `train` data. Finally, calculate the RMSE on the training data to evaluate your model’s performance.

*Hint: Choose a feature that you think may improve the model's accuracy.*

```{code-cell}
:id: GtY5-lBnvrpZ

# Create LinearRegression object
...
# Fit the object to data
...
# predict MedHouseVal in training data
...
# Calculate RSME on train data
rmse_dict['your_model'] = ...
```

```{code-cell}
:id: NDJj_89vKRxi

# Run this cell to compare training errors across models
rmse_dict
```

+++ {"id": "DPgA_7yWvusJ"}

#### Underfitting and Overfitting

Until now, we’ve been working solely with our training data, holding back our test data for the final evaluation. This approach helps us test our model's ability to generalize to new, unseen data.

Explanation of **Overfitting** and **Underfitting**:

- **Underfitting** occurs when a model is too simple to capture the patterns in the data. It may have high errors on both training and test data, indicating that it fails to represent the underlying trends.
- **Overfitting** happens when a model is too complex and learns not only the underlying patterns but also the noise in the training data. This results in very low training error but high test error, as the model doesn’t generalize well to new data.

**Task**: Calculate the test error (e.g., RMSE) on the test data and compare it to the training error. Use this comparison to assess whether the model may be underfitting, overfitting, or achieving a good fit.

```{code-cell}
:id: MVzD2z-Jv8Is

test_rsme = {}
# constant
test_rsme["constant"] = rmse(test[...], constant_model)
# simple
test_rsme["simple"] = rmse(test[...], simple_model.predict(test[["MedInc"]]))
# multiple
test_rsme["multiple"] = rmse(test[...], multiple_model.predict(test[[...,...]]))
# you model
test_rsme["your_model"] = rmse(test[...], ...)
```

```{code-cell}
:id: jWZrM4axv2ZG

# Transform rsmes to a dataframe
rmse_df = pd.DataFrame.from_dict(rmse_dict, orient="index", columns=["Training RMSE"])
rmse_df["Test RMSE"] = test_rsme.values()
rmse_df.index.name = "Model"
rmse_df
```

+++ {"id": "ORfVwjHTKAS3"}

**Question**: Examine the Test RMSE column. What patterns or differences do you notice? Compare the Test RMSE with the Training RMSE for each model. What insights can you draw from these comparisons regarding model performance and generalization?

+++ {"id": "LArtLZKQOGdj"}

*Type your answer here, replacing this text.*

+++ {"id": "rYR2SV1sP56K"}

---------------------------------------------------------
## Congratulations! You've finished the Modeling Lab

Developed by: Lan Dinh
