---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.18.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
obscure_packages = ["sympy"]

for pkg in obscure_packages:
    try:
        __import__(pkg)  # check if installed
    except ImportError:
        print(f":warning: {pkg} not found. Installing...")
        !pip install {pkg}
        __import__(pkg)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from ipywidgets import interact
import ipywidgets as widgets
from sympy import Symbol, Eq, solve_undetermined_coeffs, apart
```

# Understanding Partial Fraction Decomposition

**Estimated Time**: 30-45 Minutes
**Developers**: Jonathan Ferrari

---

## Table of Contents

- 1. **Introduction**
   - 1.1. Learning Objectives
   - 1.2. What is Partial Fraction Decomposition?
   - 1.3. Importance in Mathematics

- 2. **Fundamentals of Partial Fractions**
   - 2.1. Steps for Partial Fraction Decomposition
   - 2.2. Example with Detailed Steps
   - 2.3. Solving Algebraically

- 3. **Interactive Examples**
   - 3.1. Example 1: Basic Partial Fraction Decomposition
   - 3.2. Example 2: Decomposition with Repeated Factors
   - 3.3. Example 3: Decomposition with Quadratic Factors

- 4. **Free Response Questions and Reflections**

- 5. **Conclusion**

---

## 1. Introduction

### 1.1. Learning Objectives

In this lesson, you will:

- Understand the purpose and method of partial fraction decomposition.
- Learn to factor polynomial denominators effectively.
- Solve partial fraction decompositions algebraically.
- Interact with examples using symbolic computation (SymPy).
- Reflect on your understanding through guided questions.

### 1.2. What is Partial Fraction Decomposition?

Partial fraction decomposition (PFD) breaks down complex rational expressions into simpler fractions, which makes integration and other mathematical operations easier. It is especially useful in calculus and algebraic simplifications.

### 1.3. Importance in Mathematics

Partial fraction decomposition is fundamental in calculus, particularly for integrating rational functions, solving differential equations, and analyzing Laplace transforms.

---

## 2. Fundamentals of Partial Fractions

### 2.1. Steps for Partial Fraction Decomposition

To decompose a rational function:

1. Factor the denominator into irreducible factors.
2. Write the rational function as a sum of fractions with unknown numerators.
3. Multiply both sides by the common denominator.
4. Equate coefficients of corresponding powers of x to solve for unknowns.

### 2.2. Example with Detailed Steps

Given:

$$
f(x) = \frac{1}{x^2 + 2x - 3}
$$

First, factor the denominator:

$$
x^2 + 2x - 3 = (x + 3)(x - 1)
$$

Thus, we have:

$$
\frac{1}{x^2 + 2x - 3} = \frac{A}{x + 3} + \frac{B}{x - 1}
$$

### 2.3. Solving Algebraically

Multiplying through by the denominator:

$$
1 = A(x - 1) + B(x + 3)
$$

Expanding and grouping like terms:

$$
1 = Ax - A + Bx + 3B = (A + B)x + (-A + 3B)
$$

Equating coefficients:

$$
0 = A + B \quad \text{and} \quad 1 = -A + 3B
$$

We solve using SymPy:

```{code-cell} ipython3
from sympy import Symbol, Eq, solve_undetermined_coeffs

A = Symbol('A')
B = Symbol('B')
x = Symbol('x')

solve_undetermined_coeffs(Eq(1, A * (x - 1) + B * (x + 3)), [A, B], x)
```

```{code-cell} ipython3
equation1 = Eq(1, A * (x - 1) + B * (x + 3))
equation1
```

---

## 3. Interactive Examples

### 3.1. Example 1: Basic Partial Fraction Decomposition

Using SymPy to directly verify the result:

```{code-cell} ipython3
from sympy import apart

apart(1 / (x**2 + 2*x - 3))
```

### Free Response Question 3.1:
> How does verifying your result with SymPy help in understanding the algebraic process?

Your Answer Here

---

### 3.2. Example 2: Decomposition with Repeated Factors

Decompose:

$$
\frac{1}{(x-1)(x+2)^2}
$$

```{code-cell} ipython3
C = Symbol('C')
solve_undetermined_coeffs(Eq(1, A*(x+2)**2 + B*(x-1)*(x+2) + C*(x-1)), [A, B, C], x)
```

### Free Response Question 3.2:
> Explain the importance of separate terms for repeated factors.

Your Answer Here

---

### 3.3. Example 3: Decomposition with Quadratic Factors

Decompose:

$$
\frac{1}{(x-1)(x^2 + 2x + 5)}
$$

```{code-cell} ipython3
solve_undetermined_coeffs(Eq(1, A*(x**2 + 2*x + 5) + (B*x + C)*(x-1)), [A, B, C], x)
```

### Free Response Question 3.3:
> Why do quadratic terms require both a linear numerator and constant term?

Your Answer Here

---

## 4. Free Response Questions and Reflections

### Question 4.1:
> Discuss how partial fraction decomposition simplifies integration problems.

Your Answer Here

### Question 4.2:
> Reflect on algebraic vs computational methods for partial fractions.

Your Answer Here

---

## 5. Conclusion

You explored partial fraction decomposition, practiced algebraic and computational methods, and reflected on the importance of this technique.

### Final Reflection:
> What aspect of partial fraction decomposition do you find most challenging?

Your Answer Here
