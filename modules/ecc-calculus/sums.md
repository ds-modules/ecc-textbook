---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.3
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Exploring Riemann Sums: Approximating the Area Under a Curve

+++

**Estimated Time**: 30-60 Minutes  
**Developers**: Jonathan Ferrari

+++

## Table of Contents

+++

1. **Introduction**  
   1.1. Learning Objectives  
   1.2. What are Riemann Sums?  
   1.3. Overview of Approximation Methods  
2. **Riemann Sum Fundamentals**  
   2.1. Partitioning the Interval  
   2.2. Left, Right, and Midpoint Approximations  
   2.3. The Trapezoidal Rule  
   2.4. Code Example: Basic Riemann Sum  
3. **Interactive Visualizations**  
   3.1. Visualizing Riemann Sums for a Fixed Function  
   3.2. Dynamic Function Exploration  
4. **Mathematical Derivations**  
   4.1. Derivation of the Trapezoidal Rule  
5. **Free Response Questions and Reflections**  
6. **Conclusion**

+++

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++

## 1. Introduction

+++

### 1.1. Learning Objectives

In this lesson, you will:

- Understand the concept of Riemann sums and how they are used to approximate the definite integral.
- Explore different approximation methods including the Left Endpoint, Right Endpoint, Midpoint, and the Trapezoidal Rule.
- Analyze how the choice of method and number of partitions affect the accuracy of the approximation.
- Interact with visualizations that illustrate these methods.
- Follow through a derivation of the trapezoidal rule using LaTeX and symbolic manipulation.
- Reflect and answer free response questions that prompt deeper understanding.

+++

### 1.2. What are Riemann Sums?

Riemann sums approximate the area under a curve by breaking it into small shapes (usually rectangles) and summing their areas. This process is useful when an antiderivative is difficult to obtain or when working with discrete data.

+++

### 1.3. Overview of Approximation Methods

We will cover several key methods:

- **Left Endpoint Approximation:** Uses the left endpoint of each subinterval to form rectangles.
- **Right Endpoint Approximation:** Uses the right endpoint of each subinterval.
- **Midpoint Approximation:** Uses the midpoint of each subinterval, often yielding a better result.
- **Trapezoidal Rule:** Uses trapezoids rather than rectangles, which can better approximate the area when the function is nearly linear over each subinterval.

+++

### Free Response Question 1.1:
> *Why might one choose a midpoint approximation over a simple left or right endpoint approximation?*

+++

Your Answer Here

+++

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++

## 2. Riemann Sum Fundamentals

+++

### 2.1. Partitioning the Interval

Before calculating a Riemann sum, we divide the interval $[a, b]$ into $n$ equal subintervals:

$$
\Delta x = \frac{b-a}{n}
$$

For each subinterval, we calculate areas based on the chosen evaluation point.

+++

### 2.2. Left, Right, and Midpoint Approximations

- **Left Endpoint:** Uses the left side of each subinterval, $f(x_i)$.  
- **Right Endpoint:** Uses the right side, $f(x_{i+1})$.  
- **Midpoint:** Uses the midpoint, $f\Big(x_i + \frac{\Delta x}{2}\Big)$.

These methods yield different approximations. Typically, the midpoint method gives a better approximation when the function does not change drastically over each interval.

+++

### Free Response Question 2.1:
> *Explain in your own words the advantages and limitations of using left, right, and midpoint approximations. When might each be most appropriate?*

+++

Your Answer Here

+++

### 2.3. The Trapezoidal Rule

The trapezoidal rule uses trapezoids rather than rectangles. For a subinterval $[x_i, x_{i+1}]$, the area of a trapezoid is calculated as:

$$
\text{Area}_i = \frac{\Delta x}{2}\Big[f(x_i) + f(x_{i+1})\Big]
$$

This method often yields a better approximation, particularly when the function is nearly linear over each subinterval.

+++

### 2.4. Code Example: Basic Riemann Sum

Below is a code example to compute the Riemann sum for the function 
$$
f(x) = x(x-1)(x-2).
$$

```{code-cell} ipython3
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from ipywidgets import interact
import ipywidgets as widgets
%matplotlib inline

# Use the fivethirtyeight style
matplotlib.style.use('fivethirtyeight')

def f(x):
    return x * (x - 1) * (x - 2)

def basic_riemann(approx_type, num_rects):
    fig, ax = plt.subplots(figsize=(8, 4))
    xs = np.linspace(0, 2.5, 300)
    ax.plot(xs, f(xs), 'k-', label="f(x)")
    
    rectangle_width = 2.5 / num_rects
    rectangle_xs = np.arange(0, 2.5, rectangle_width)
    area_approx = 0
    for x in rectangle_xs:
        if approx_type == 'Trapezoids':
            x1 = x
            x2 = x + rectangle_width
            y1 = f(x1)
            y2 = f(x2)
            ax.add_patch(plt.Polygon([[x1, 0], [x1, y1], [x2, y2], [x2, 0]], alpha=0.5, facecolor='orange'))
            area_approx += 0.5 * rectangle_width * (y1 + y2)
        else:
            if approx_type == 'Left Endpoints':
                y = f(x)
            elif approx_type == 'Right Endpoints':
                y = f(x + rectangle_width)
            elif approx_type == 'Center Points':
                y = f(x + rectangle_width/2)
            ax.add_patch(Rectangle((x, 0), rectangle_width, y, alpha=0.5, facecolor='skyblue'))
            area_approx += rectangle_width * y

    ax.set_title(f"{approx_type} Approximation with {num_rects} Rectangles")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    plt.show()
    print("Approximated Area:", area_approx)
    actual_area = 0.25 * (2.5**4) - (2.5**3) + (2.5**2)
    print("Computed Actual Area:", actual_area)
    print("Error (Approx - Actual):", area_approx - actual_area)

approx_type_dropdown = widgets.Dropdown(options=['Left Endpoints', 'Right Endpoints', 'Center Points', 'Trapezoids'])
num_rects_slider = widgets.IntSlider(description='Rectangles', min=1, max=50, step=1)

interact(basic_riemann, approx_type=approx_type_dropdown, num_rects=num_rects_slider);
```

### Free Response Question 2.2:
> After running the above code, describe how the number of rectangles influences the approximation error. How does the choice of method (rectangle vs. trapezoid) affect the result?

+++

Your Answer Here

+++

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++

## 3. Interactive Visualizations

+++

### 3.1. Visualizing Riemann Sums for a Fixed Function

In this section, we revisit the function
$$
f(x) = x(x-1)(x-2)
$$
and compare different approximation methods interactively. Adjust the number of rectangles and observe how the estimated area converges as you refine the partition.

```{code-cell} ipython3
def compare_riemann_methods(approx_type, num_rects):
    fig, ax = plt.subplots(figsize=(8, 4))
    xs = np.linspace(0, 2.5, 300)
    ax.plot(xs, f(xs), 'k-', label="f(x)")
    
    rectangle_width = 2.5 / num_rects
    rectangle_xs = np.arange(0, 2.5, rectangle_width)
    area_approx = 0
    for x in rectangle_xs:
        if approx_type == 'Trapezoids':
            x1 = x
            x2 = x + rectangle_width
            y1 = f(x1)
            y2 = f(x2)
            ax.add_patch(plt.Polygon([[x1, 0], [x1, y1], [x2, y2], [x2, 0]], alpha=0.5, facecolor='green'))
            area_approx += 0.5 * rectangle_width * (y1 + y2)
        else:
            if approx_type == 'Left Endpoints':
                y = f(x)
            elif approx_type == 'Right Endpoints':
                y = f(x + rectangle_width)
            elif approx_type == 'Center Points':
                y = f(x + rectangle_width/2)
            ax.add_patch(Rectangle((x, 0), rectangle_width, y, alpha=0.5, facecolor='purple'))
            area_approx += rectangle_width * y

    ax.set_title(f"{approx_type} Approximation with {num_rects} Rectangles")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    plt.show()
    print("Approximated Area:", area_approx)

interact(compare_riemann_methods, approx_type=approx_type_dropdown, num_rects=num_rects_slider);
```

### Free Response Question 3.1:
> Compare the output from different approximation methods for the fixed function. Which method appears to be the most accurate in your opinion and why?

+++

Your Answer Here

+++

### 3.2. Dynamic Function Exploration

Now extend your exploration to a dynamic function where you can adjust the coefficients in the cubic function
$$
f(x) = ax^3 + bx^2 + cx + d.
$$
Experiment with different shapes and observe how the Riemann sum approximation changes.

```{code-cell} ipython3
def dynamic_f(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

a_slider = widgets.FloatSlider(value=1.0, min=-5.0, max=5.0, step=0.1, description='a')
b_slider = widgets.FloatSlider(value=-3.0, min=-5.0, max=5.0, step=0.1, description='b')
c_slider = widgets.FloatSlider(value=2.0, min=-5.0, max=5.0, step=0.1, description='c')
d_slider = widgets.FloatSlider(value=0.0, min=-5.0, max=5.0, step=0.1, description='d')

def render_dynamic_riemann(a, b, c, d, approx_type, num_rects):
    def f_dynamic(x):
        return dynamic_f(x, a, b, c, d)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    xs = np.linspace(0, 2.5, 300)
    ys = f_dynamic(xs)
    ax.plot(xs, ys, 'k-', label="f(x)")
    
    rectangle_width = 2.5 / num_rects
    rectangle_xs = np.arange(0, 2.5, rectangle_width)
    area_approx = 0
    for x in rectangle_xs:
        if approx_type == 'Trapezoids':
            x1 = x
            x2 = x + rectangle_width
            y1 = f_dynamic(x1)
            y2 = f_dynamic(x2)
            ax.add_patch(plt.Polygon([[x1, 0], [x1, y1], [x2, y2], [x2, 0]], alpha=0.5, facecolor='red'))
            area_approx += 0.5 * rectangle_width * (y1 + y2)
        else:
            if approx_type == 'Left Endpoints':
                y = f_dynamic(x)
            elif approx_type == 'Right Endpoints':
                y = f_dynamic(x + rectangle_width)
            elif approx_type == 'Center Points':
                y = f_dynamic(x + rectangle_width/2)
            ax.add_patch(Rectangle((x, 0), rectangle_width, y, alpha=0.5, facecolor='blue'))
            area_approx += rectangle_width * y

    ax.set_title(f"Dynamic f(x) with {approx_type} Approximation ({num_rects} Rectangles)")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    plt.show()
    print("Approximated Area:", area_approx)

interact(render_dynamic_riemann, 
         a=a_slider, b=b_slider, c=c_slider, d=d_slider, 
         approx_type=approx_type_dropdown, 
         num_rects=num_rects_slider);
```

### Free Response Question 3.2:
> By adjusting the coefficients $a$, $b$, $c$, and $d$, what changes do you observe in the shape of $f(x)$? How do these changes affect the accuracy of the Riemann sum approximation?

+++

Your Answer Here

+++

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++

## 4. Mathematical Derivations

+++

### 4.1. Derivation of the Trapezoidal Rule

Let’s derive the trapezoidal rule for approximating the integral of $f(x)$ over $[a, b]$. Divide the interval into $n$ equal subintervals where

$$
\Delta x = \frac{b-a}{n}.
$$

For a subinterval $[x_i, x_{i+1}]$, the area of the trapezoid is given by:

$$
\text{Area}i = \frac{\Delta x}{2}\Big[f(x_i) + f(x{i+1})\Big].
$$

Summing over all subintervals, we have:

$$
\int_a^b f(x),dx \approx \frac{\Delta x}{2}\Big[f(x_0) + 2f(x_1) + 2f(x_2) + \cdots + 2f(x_{n-1}) + f(x_n)\Big].
$$

Note that the interior terms are multiplied by 2 because each value is used in the area calculation of two adjacent trapezoids.

+++

### Free Response Question 4.1:
> In your own words, explain the reasoning behind multiplying the interior terms by 2 in the trapezoidal rule formula.

+++

Your Answer Here

+++

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++

## 5. Free Response Questions and Reflections

+++

### Free Response Question 5.1:
> Discuss how the error in a Riemann sum approximation changes as the number of subintervals increases. Why does the error generally decrease?

+++

Your Answer Here

+++

### Free Response Question 5.2:
> Compare the performance of the trapezoidal rule with that of the rectangle-based methods. Under what conditions might one be preferred over the others?

+++

Your Answer Here

+++

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++

## 6. Conclusion

+++

In this lesson, you explored the process of approximating the area under a curve using Riemann sums. You learned about several methods—left endpoint, right endpoint, midpoint, and the trapezoidal rule—and saw how increasing the number of subintervals improves accuracy. The interactive visualizations allowed you to experiment with both a fixed function and a dynamically adjustable function, deepening your understanding of numerical integration.

### Final Reflection:
> How might numerical integration techniques like those covered in this lesson be applied to real-world problems or other areas of mathematics?

+++

Your Answer Here

+++

Well done! Continue to experiment with the provided code, explore new functions, and reflect on the implications of these approximation methods in both theoretical and practical contexts.
