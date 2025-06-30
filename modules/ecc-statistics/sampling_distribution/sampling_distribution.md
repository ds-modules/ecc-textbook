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
# Necessary imports for this module
from utils import *
```

# Sampling Distributions & Central Limit Theorem

+++

**Estimated Time**: 30 Minutes <br>
**Developers**: James Geronimo, Mark Barranda

+++

**The sampling distribution of a statistic** is the distribution of all values of a statistic when all possible samples of the same size *n* are taken from the same population.

The basic idea is this: If you were to take multiple samples, what values from those samples will give you the best estimates of the population values?

+++

---

+++

## Example 1: Fair Die

```{code-cell} ipython3
n_samples = 10000
sample_size = 5
population = np.arange(1, 7)
```

### Means

+++

**Sampling Procedure:**  
Roll a fair six-sided die 5 times and record the sample mean, $\bar{x}$. <br>
Repeat this process 10,000 times to build a **distribution of sample means**.

- **Population Mean ($\mu$):** 3.5

🟩 The dashed green line represents the **mean of all sample means**.

```{code-cell} ipython3
fair_die_means(n_samples, sample_size, population)
```

In this cell block, we show a few indivudal sample means generate from five samples.

```{code-cell} ipython3
for i in range(5):
    rolls = np.random.choice(population, size=sample_size)
    print(f"Sample {i+1} rolls: {rolls}, Sample Mean: {np.mean(rolls):.2f}")
```

All outcomes are equally likely so the **__________** mean is 3.5;

The **__________** of the sample means in 10,000 trials is 3.51. If continued indefinitely, the sample mean will be 3.5.

+++

**Note:**
1) The mean of the sample means **__________** the value of the pouplation mean
2) The sample means have a **__________** distribution

+++

### Variances

+++

**Sampling Procedure:**  
Roll a fair six-sided die 5 times and record the sample variance, $s^2$. <br>
Repeat this process 10,000 times to build a **distribution of sample variances**.

- **Population Variance ($\sigma^2$):** 2.9

🟩 The dashed green line represents the **mean of all sample variances**.

```{code-cell} ipython3
fair_die_variances(n_samples, sample_size, population)
```

In this cell block, we show a few individual sample variances generate from five samples.

```{code-cell} ipython3
for i in range(5):
    rolls = np.random.choice(population, size=sample_size)
    print(f"Sample {i+1} rolls: {rolls}, Sample Mean: {np.var(rolls, ddof=1):.2f}")
```

All outcomes are equally likely so the **__________** variance is 2.9.

The **__________** of sample variance in the 10,000 trials is 2.92. If continued indefinitely, the sample variance will be 2.9.

+++

**Note:**
1) The mean of the sample variances **__________** the value of the pouplation variance
2) The sample variances have a **__________** distribution

+++

### Proportions

+++

**Sampling Procedure:**  
Roll a fair six-sided die 5 times and record the proportion of odd numbers. <br>
Repeat this process 10,000 times to build a **distribution of odd number proportions**.

- **Population Proportion of Odd Numbers ($p$):** 0.5
- $\hat{p}$ represents the sample proportion of odd numbers

🟩 The dashed green line represents the **mean of all odd number proportions**.

```{code-cell} ipython3
fair_die_proportions(n_samples, sample_size, population)
```

In this cell block, we show a few indivudal sample proportions generate from five samples.

```{code-cell} ipython3
for i in range(5):
    rolls = np.random.choice(population, size=sample_size)
    print(f"Sample {i+1} rolls: {rolls}, Sample Mean: {np.sum(rolls % 2 == 1) / sample_size:.2f}")
```

All outcomes are equally likely so the **__________** of odd numbers is 0.5.

The mean of the **__________** of the 10,000 trials is 0.503. If continued indefinitely, the mean of sample proportions will be 0.5.

+++

**Note:**
1) The mean of the sample proportions **__________** the value of the pouplation proportions
2) The sample proportions have a **__________** distribution

+++

### Estimators

+++

Using the above information, we discover **biased** and **unbiased estimators** of population parameters.

+++

#### Unbiased Estimators:

+++

The **__________** $\bar{x}$, **__________** $s^2$, and **__________** $\hat{p}$ of the samples are unbiased estimators of the corresponding pouplation parameters $mu$, $\sigma^2$, and $p$ because they target the value that the population would have.

+++

#### Biased Estimators:

+++

The **__________** , **__________** , and **__________** $s$ do NOT target their corresponding pouplation parameters, so they are generally NOT good estimators. However: often bias in the $s$ is small enough that it is used to estimate $\sigma$.

+++

---

+++

## Example 2: Assassinated Presidents

+++

There are four U.S. presidents who were assassinated in office. Their ages (in years) were Lincoln 56, Garfield 49, McKinley 59, and Kennedy 46.

+++

**a)** Assuming that 2 of the ages are randomly selected with replacement from [56, 49, 59, 46], list the 16 different possible samples by replacing the ellipses with appropriate values. We've filled out a few as a hint:

+++

[56, 56]   [49, 56]   [59, ...]   [46, ...] <br>
[56, 49]   [49, 49]   [..., ...]   [..., ...] <br>
[56, 59]   [49, ...]   [..., ...]   [..., ...] <br>
[56, 46]   [49, ...]   [..., ...]   [..., ...]

+++

**b)** Find the sample mean and range of possible samples by completing the functions `calculate_mean`, `calculate_range`, and `calculate_probability`. Then, run the cell to create tables that represent the probability distribution of each statistic.

```{code-cell} ipython3
def calculate_mean(number1, number2):
    """Fill in the ... to calculate the mean of two numbers."""
    return ...
    
def calculate_range(number1, number2):
    """Fill in the ... to calculate the range of two numbers."""
    return ...

def calculate_probability(frequency, total_samples):
    """Fill in the ... to calculate the probability given frequency and total_samples."""
    return ...

mean_range_tables(calculate_mean, calculate_range, calculate_probability)
```

**c)** Calculate the `population_mean` and `population_range`. Then, for each statistic, compare the mean of sample statistics to the population statistic. Which sampling distributions target the population parameter?

```{code-cell} ipython3
population_mean = ...
population_range = ...

print(f"Population Mean: {population_mean}")
print(f"Population Range: {population_range}")
```

Mean of sample means **__________** the population mean which makes this a **__________** estimator

+++

Mean of sample ranges **__________** the population range which makes this a **__________** estimator

+++

**d)** Complete each of the following expressions:

+++

Mean of sample medians **__________** the population median which makes this a **__________** estimator

+++

Mean of the sample proportions **__________**

+++

Mean of the **__________** variances **__________**

+++

**__________** of the **__________** standard deviations **__________**

+++

---

+++

**Hurray! You have completed this notebook! 🚀**
