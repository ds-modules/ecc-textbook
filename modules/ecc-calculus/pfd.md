---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.18.1
---

```{code-cell}
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

# Partial Fractions

This example was copied from [Wikipedia](https://en.wikipedia.org/wiki/Partial_fraction_decomposition).

For example, we want to decompose:
$$
f(x) = \frac{1}{x^2 + 2x - 3}
$$

First, we factor:
$$
q(x) = x^2 + 2x - 3 = (x + 3)(x - 1)
$$

So we have the PFD:
$$
f(x) = \frac{1}{x^2 + 2x - 3} = \frac{A}{x + 3} + \frac{B}{x - 1}
$$

Giving us the polynomial identity:
$$
\begin{align*}
1 &= A(x - 1) + B(x + 3) \\
1 &= Ax - A + Bx + 3B \\
0x + 1 &= (A + B)x + (-A + 3B) \\
\implies \\
0 &= A + B \\
1 &= -A + 3B
\end{align*}
$$

Which we can solve using SymPy:

```{code-cell}
A = Symbol('A')
B = Symbol('B')
x = Symbol('x')
solve_undetermined_coeffs(Eq(1, A * (x - 1) + B * (x + 3)), [A, B], x)
```

[Docs for `solve_undteremined_coeffs`](https://docs.sympy.org/latest/modules/solvers/solvers.html#sympy.solvers.solvers.solve_undetermined_coeffs)

+++

We can also have SymPy perform the entire PFD but this probably defeats the purpose:

```{code-cell}
apart(1 / (x**2 + 2*x - 3))
```

$$
\frac{1}{(x-1)(x+2)^2} = \frac{A}{x-1} + \frac{B}{x+2} + \frac{C}{(x+2)^2}
$$

$$
\frac{1}{(x-1)(x^2 + 2x + 5)} = \frac{A}{x-1} + \frac{Bx + C}{x^2 + 2x + 5}
$$

$$
\frac{1}{(x-1)(x^2 + 2x + 5)^2} = \frac{A}{x - 1} + \frac{Bx + C}{x^2 + 2x + 5} + \frac{Dx + E}{(x^2 + 2x + 5)^2}
$$

+++

## question 1

$$
1 = A(x+2)^2 + B(x-1)(x+2) + C(x-1)
$$

```{code-cell}
C = Symbol('C')
solve_undetermined_coeffs(Eq(1, A * (x + 2) ** 2 + B * (x - 1) * (x + 2) + C * (x-1)), [A, B, C], x)
```

## question 3

```{code-cell}
D = Symbol('D')
E = Symbol('E')

solve_undetermined_coeffs(Eq(1, A * (x ** 2 + 2 * x + 5) ** 2 + (B * x + C) * (x - 1) * (x ** 2 + 2 * x + 5) + (D * x + E) * (x-1)), [A, B, C, D, E], x)
```
