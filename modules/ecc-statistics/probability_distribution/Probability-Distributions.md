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

Below, we have imported the Python libraries needed for this module. Run the code in this cell before running any other code cells, and be careful **not to change** any of the code.
You can run the cell in any of these ways:
 - Ctrl + Enter: Run the cell and keep the cursor in the same cell.
- Shift + Enter: Run the cell and move the cursor to the next cell.
- Click the Play button: Click the Run (play) button to the left of the cell to execute it.

```{code-cell} ipython3
import otter

from scipy import stats
from functions.interact import *
from functions.utils import*
from scipy.stats import binom, geom
```

___
*Estimated Time: ~30 minutes*
___

+++

Contents:

- Discrete Probability Distribution
- Interacting with Parameters
    - Bernoulli
    - Binomial
    - Poisson
    - Geometric
- Conclusion

+++

# Discrete Probability Distribution

+++

In statistics, discrete probability distribution refers to a distribution where a random variable can take on distinct values (eg. the number of heads in 20 coin flips). At their core, probability distributions are just functions similar to the ones you've seen in calculus:

$$ f(x) = x^2 $$

These functions, however, are defined by their parameters: the mean and variance

+++

When describing a random variable in terms of its distribution, we usually specify what kind of distribution it follows, its mean and standard deviation. Take for a example the normal distribution below:

$$ f(\mu, \sigma) = \mathcal{N}(\mu, \sigma) $$

Using the information above, we would specify that our variable follows a Normal Distribution with mean µ and standard deviation (SD) σ.

+++

## Understanding Probability Mass Function (PMF) 

+++

Before we dive deep into distributions below, it is important to fully understand the underlying mechanics behind them. When dealing with discrete probability, we will be using probability mass function (pmf). Probability Mass Function is defined as a function that gives the probability that a discrete random variable is exactly equal to some distrinct value. 

You may be wondering how this differs from Probability Density Function (PDF). One might say that unlike PMF which deals with discrete random variable, Probability Density Function deals with continuous random variable. To quote a response from [Stack Exchange](https://math.stackexchange.com/questions/23293/probability-density-function-vs-probability-mass-function#comment50446_23294):

*Think of the discrete distribution as having a mass at each point, where the probability of that point is how much of the total mass is there. Then the continuous case is linear density, where the mass is spread over an interval.*

+++

## Interacting with Parameters

+++

## Bernoulli

+++

A Bernoulli function represents a Bernoulli distribution, which is a discrete probability distribution for a single trial experiment (eg. one flip of a coin and the probability of getting a head) with only two possible outcomes:
- Success (1) with probability  p 
- Failure (0) with probability  1 - p                                                                                        

+++

The probability mass function for bernoulli is:
                             
\begin{cases} 
    1 - p, & \text{if } k = 0 \\
    p, & \text{if } k = 1
\end{cases}
    
$\text{for } k \in \{0,1\}, \quad 0 \leq p \leq 1.$

+++

Note: The Bernoulli function only takes a single parameter p which represents the probability of success. Below, think of Bernoulli(p) as P(Success).

```{code-cell} ipython3
bernoulli() # bernoulli(p)
q_1()
```

---

+++

## Binomial

+++

Now say your friend decides to flip a coin 20 times because they want to know have many heads they'll get, this sequence of outcomes is known as the Bernoulli process. To obtain the number of successes (# of heads in 20 flips), we will be looking at the Binomial Distribution. The Binomial function takes two parameters: 
- n - number of trials
- p - probability of success in each trial

The probability mass function for binomial is:

+++

$$ 
f(k, n, p) = P(X = k) = \binom{n}{k} p^k (1 - p)^{n - k}
$$

where 
$$
\binom{n}{k} = \frac{n!}{k!(n-k)!}
$$

is a binomial coefficent which counts the number of ways to choose the positions of the k successes among the n trials. Note: k is not a parameter but rather it represents a random variable for the number of success observed in n trials (below, it is X=x).

+++

Note: Alternatively for Q2 and Q3 you can use **stats.binom(k, n, p)** where k is the number of successes (see above formula), n is total number of trials, and p is probability of success. Keep in mind the assumptions for both scenarios when choosing p.

```{code-cell} ipython3
# Use this cell for help with questions 2 and 3 (uncomment and fill in the parameters below)
# print(binom.pmf(..., ..., ...))
```

```{code-cell} ipython3
# add in specific values for x

binomial()
q_2_3()
```

---

+++

## Poisson

+++

### Step-by-step: Using the Poisson distribution for the ambulance example

You work at a busy hospital emergency room where ambulances arrive at an average rate of 5 per hour. Two things you notice are that each ambulance's arrival does not have an effect on when the next one will arive (independent) and that their intervals are not evenly spaced or predictable (random). A Poisson distribution can model the probability of the hospital receiving exactly 7 ambulances in an hour. It can also predict the likelihood of having 2 or fewer arrivals in a given timeframe in order to help staff prepare and come up with effective strategies for delagating shifts.

1. **Define the random variable.**  
   Let $X$ be the number of ambulances that arrive at the ER in a 1-hour period.

2. **Check that a Poisson model is appropriate.**  
   - Arrivals are **independent** (one ambulance arriving does not affect the next).  
   - Arrivals happen at a **constant average rate** of 5 per hour ($\lambda = 5$).  
   - We are counting the **number of events in a fixed interval of time** (1 hour).  
   These are exactly the conditions under which the Poisson distribution is a good model.

3. **Identify the parameter.**  
   From the problem, the average rate is $\lambda = 5$ ambulances per hour.  
   We write $X \sim \text{Poisson}(\lambda = 5)$.

4. **Probability of exactly 7 ambulances in one hour.**  
   We want $P(X = 7)$. Using the Poisson pmf:
   $$
   P(X = 7) = \frac{5^{7} e^{-5}}{7!}.
   $$
   If you plug this into a calculator (or use Python), you get approximately:
   $$
   P(X = 7) \approx 0.104 \quad \text{(about a 10.4\% chance)}.
   $$

5. **Probability of 2 or fewer ambulances in one hour.**  
   Now we want $P(X \le 2)$, which is the sum of the probabilities for 0, 1, and 2 arrivals:
   $$
   P(X \le 2) = P(X = 0) + P(X = 1) + P(X = 2).
   $$
   Using the pmf for each value of $k$:
   $$
   P(X = k) = \frac{5^{k} e^{-5}}{k!}, \quad k = 0, 1, 2.
   $$
   So
   $$
   \begin{aligned}
   P(X \le 2) &= e^{-5}\left(\frac{5^{0}}{0!} + \frac{5^{1}}{1!} + \frac{5^{2}}{2!}\right) \\
               &= e^{-5}(1 + 5 + 12.5) \\
               &\approx 0.125 \quad \text{(about a 12.5\% chance)}.
   \end{aligned}
   $$

6. **(Optional) Check your work in Python.**  
   In code, you could compute these as:
   - $P(X = 7)$: `stats.poisson.pmf(7, 5)`  
   - $P(X \le 2)$: `stats.poisson.cdf(2, 5)`  
   These should give values close to the probabilities we computed by hand above.

+++

As suggested in the example above, under the Poisson distribution, we can find out the probability of a given number of events occuring in a fixed interval of time. 

It takes only one parameter, lambda (λ), which is the average number of events occuring in an interval of time or space. In our hospital scenario, λ = 5. The probability mass function is given by:

$$
f(k; \lambda) = \Pr(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}
$$

where k is the number of occurence, e is [Euler's Number](https://en.wikipedia.org/wiki/E_(mathematical_constant)), and k! is the factorial.

+++

Alternatively for Q4a and Q4b you can use **stats.poisson.pmf(k, λ)** to check your answer.

```{code-cell} ipython3
# Use this cell for help with questions 4a and 4b (uncomment and fill in the parameters below)
# print(stats.poisson.pmf(12 , 14))
```

```{code-cell} ipython3
poisson()
q_4a_4b()
q_5()
```

---

+++

## Geometric

+++

Now, imagine you work as a customer service specialist and your team receives thousands of calls a day. Your manager shared the team's performance data: the probability of an agent solving a single customer's refund issue on the first try is 44%. You know that not every call can be successfully resolved because some require multiple interactions. 

In the scenario above, a geometric distribution can help you model the probability of requiring exactly 'k' calls before the first success. In other words, each call (event) is a Bernoulli trial for a single customer. Some questions you might ask are:
- What is the probability that your coworker Elizabeth will resolve an issue on the 3rd attempt?
- Given p = 0.50, how many attempts would it likely take to solve a customer's issue at a 30% probability.

By using the Geometric Probability Mass Function (PMF), we can predict how often issues require multiple calls in order to reduce resolution time for certain cases.  

$$
P(X = k) = (1 - p)^{k-1} p, \quad k = 1, 2, 3, \dots
$$

Where P(X=k) is the probability that the first success occurs on the k-th trial.

+++

### Step-by-step: Using the geometric distribution for the call-center example

We will answer the two questions in the scenario using the geometric probability mass function (PMF):
$$
P(X = k) = (1 - p)^{k-1} p, \quad k = 1, 2, 3, \dots
$$
where \(X\) is the number of calls until the first successful resolution and \(p\) is the probability of success on any single call.

1. **Define the random variable.**  
   Let \(X\) be the number of calls an agent makes to a *single customer* until the refund issue is resolved for the first time.

2. **Check that a geometric model is appropriate.**  
   - Each call is a **Bernoulli trial** (success = issue resolved, failure = not resolved).  
   - The probability of success \(p\) is the **same on every call**.  
   - Calls are **independent** from one another for that customer.  
   This matches the conditions for using a geometric distribution.

3. **Question 1 – Probability of resolving on the 3rd attempt (p = 0.44).**  
   Here \(p = 0.44\) and we want \(P(X = 3)\):
   $$
   P(X = 3) = (1 - 0.44)^{3-1} (0.44) = (0.56)^2 (0.44).
   $$
   Compute step by step:
   $$
   (0.56)^2 = 0.3136, \quad 0.3136 \times 0.44 \approx 0.138.
   $$
   So the probability that Elizabeth resolves the issue **on the 3rd call** is about **13.8%**.

4. **Question 2 – With p = 0.50, when is the probability about 30%?**  
   Now set \(p = 0.50\). The geometric PMF becomes
   $$
   P(X = k) = (1 - 0.5)^{k-1} (0.5) = (0.5)^k.
   $$
   We want to know for which number of attempts \(k\) this probability is around 0.30. Set up the equation:
   $$
   0.30 \approx (0.5)^k.
   $$
   Take natural logs on both sides:
   $$
   \ln(0.30) = k \ln(0.5) \quad \Rightarrow \quad k = \frac{\ln(0.30)}{\ln(0.5)} \approx 1.74.
   $$
   Since \(k\) must be a whole number of calls, this tells us that a **30% chance of first success** happens **between the 1st and 2nd call**. In practice, this means that by the time you are finishing the **2nd call**, you have reached (and passed) roughly a 30% chance that the customer’s issue has been resolved for the first time.

```{code-cell} ipython3
from ipywidgets import interact, FloatSlider, IntSlider
import numpy as np
import matplotlib.pyplot as plt
from math import log


def geometric_walkthrough_visualizer(p_example=0.44, k_example=3, target_prob=0.30):
    """Interactive visualizer that mirrors the two geometric walkthrough questions."""
    max_k = 10

    # --- Scenario 1: Probability of resolving on the k-th call with given p_example ---
    ks = np.arange(1, max_k + 1)
    pmf_example = geom.pmf(ks, p_example)

    # --- Scenario 2: For p = 0.5, how many calls until probability ~ target_prob? ---
    p_q2 = 0.5
    ks_q2 = np.arange(1, max_k + 1)
    pmf_q2 = (1 - p_q2) ** (ks_q2 - 1) * p_q2

    # Solve (0.5)^k ≈ target_prob  (from the walkthrough)
    k_star = log(target_prob) / log(0.5)
    nearest_k = int(round(k_star))
    nearest_k = max(1, min(max_k, nearest_k))  # keep in range

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    # Plot for Scenario 1
    axes[0].bar(ks, pmf_example, color="lightgray", edgecolor="black")
    if 1 <= k_example <= max_k:
        axes[0].bar(k_example, pmf_example[k_example - 1], color="C0", edgecolor="black")
    axes[0].set_xticks(ks)
    axes[0].set_xlabel("Call number (k)")
    axes[0].set_ylabel("P(X = k)")
    axes[0].set_title(f"Scenario 1: P(X = k) with p = {p_example:.2f}")
    if 1 <= k_example <= max_k:
        axes[0].text(
            k_example,
            pmf_example[k_example - 1],
            f"  k={k_example}, P≈{pmf_example[k_example - 1]:.3f}",
            va="bottom",
        )

    # Plot for Scenario 2 (p fixed at 0.5)
    axes[1].bar(ks_q2, pmf_q2, color="lightgray", edgecolor="black")
    axes[1].bar(nearest_k, pmf_q2[nearest_k - 1], color="C1", edgecolor="black")
    axes[1].set_xticks(ks_q2)
    axes[1].set_xlabel("Call number (k)")
    axes[1].set_ylabel("P(X = k)")
    axes[1].set_title("Scenario 2: p = 0.5, target probability")
    axes[1].text(
        nearest_k,
        pmf_q2[nearest_k - 1],
        f"  k≈{k_star:.2f} (nearest k={nearest_k})",
        va="bottom",
    )

    fig.suptitle("Geometric distribution – call-center walkthrough", fontsize=12)
    plt.tight_layout()
    plt.show()


interact(
    geometric_walkthrough_visualizer,
    p_example=FloatSlider(value=0.44, min=0.1, max=0.9, step=0.02, description="p (example)"),
    k_example=IntSlider(value=3, min=1, max=10, description="k (call #)"),
    target_prob=FloatSlider(value=0.30, min=0.05, max=0.9, step=0.05, description="Target prob (Q2)"),
)
```

### Memorylessness Property ###

The memorylessness property is a characteristic of certain probability distributions where the probability of an event occurring in the future is independent of the past. In simpler terms, if a process has already been running for some time, the probability that it will continue for a certain amount of additional time remains the same as it was at the start. The exponential distribution (for continuous variables) and the geometric distribution (for discrete variables) are the classic examples of memoryless distributions. This property is useful in modeling situations like the time until failure of a machine or the number of trials until success in a Bernoulli process.

The probability of waiting n more trials for success does not depend on how many failures have already occured as each trial has to be independent. 

And lastly, each call attempt (trial) is for a single customer. If we're tracking multiple different customers calling about the same issue, then each call would be a new and independent event. Geometric distribution would not apply here.

+++

The Geometric Distribution has one parameter p, which is the probability of success in a single trial.

```{code-cell} ipython3
# Use this cell for help with questions 6a and 6b (uncomment and fill in the parameters below)
print(stats.geom.pmf(3 , 0.65))
```

```{code-cell} ipython3
geometric()
q_6()
```

---

+++

## Conclusion

+++

In this notebook, you learned various scenarious in which bernoulli, binomial, poisson, and geometric distributions apply. There are several others you can utilize depending on the problem you are trying to solve. The probability mass function lets you obtain the probability that a discrete random variable is exactly equal to some value. Additionally, you interacted with parameters for each probability distribution function to observe how they behave. 

+++

### Run the cell below to check your answers

```{code-cell} ipython3
grader = otter.Notebook()
run_tests()
```

## 📋 Post-Notebook Reflection Form

Thank you for completing the notebook! We’d love to hear your thoughts so we can continue improving and creating content that supports your learning.

Please take a few minutes to fill out this short reflection form:

👉 **[Click here to fill out the Reflection Form](https://docs.google.com/forms/d/e/1FAIpQLSc6Ekczw9VexhqkEqd52zhMd_bIBojn7umv4fTLZXA3FWE1Yw/viewform?usp=dialog)**

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

**Congratulations on making it to the end!**
