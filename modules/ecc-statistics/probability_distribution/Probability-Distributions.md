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

You work at a busy hospital emergency room where ambulances arrive at an average rate of 5 per hour. Two things you notice are that each ambulance's arrival does not have an effect on when the next one will arive (independent) and that their intervals are not evenly spaced or predictable (random). A Poisson distribution can model the probability of the hospital receiving exactly 7 ambulances in an hour. It can also predict the likelihood of having 2 or fewer arrivals in a given timeframe in order to help staff prepare and come up with effective strategies for delagating shifts.

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
