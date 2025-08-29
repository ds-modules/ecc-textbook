---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.3
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from ipywidgets import interact
import ipywidgets as widgets
from sympy import Symbol, Eq, solve_undetermined_coeffs, apart
```

```{code-cell} ipython3
def f(x):
    return x * (x - 1) * (x - 2)
```

```{code-cell} ipython3
approx_type_dropdown = widgets.Dropdown(options=['Left Endpoints', 'Right Endpoints', 'Center Points', 'Trapezoids'])
num_rects_slider = widgets.IntSlider(description='Points', min=1, max=50, step=1)

def render_riemann_sum(approx_type, num_rects):
    fig, ax = plt.subplots()
    
    xs = np.arange(0, 2.51, 0.05)
    ys = f(xs)
    ax.plot(xs, ys)

    rectangle_width = 2.5 / num_rects
    rectangle_xs = np.arange(0, 2.5, rectangle_width)
    area_approx = 0
    for x in rectangle_xs:
        if approx_type == 'Trapezoids':
            x1 = x
            x2 = x + rectangle_width
            y1 = f(x1)
            y2 = f(x2)

            color = 'r' if y1 + y2 < 0 else 'b'
            ax.add_patch(plt.Polygon([[x1, 0], [x1, y1], [x2, y2], [x2, 0]], alpha=0.5, facecolor=color))
            area_approx += 0.5 * rectangle_width * (y1 + y2)
        else:
            match approx_type:
                case 'Left Endpoints':
                    y = f(x)
                case 'Right Endpoints':
                    y = f(x + rectangle_width)
                case 'Center Points':
                    y = f(x + rectangle_width * 0.5)
            color = 'r' if y < 0 else 'b'
            ax.add_patch(Rectangle((x, 0), rectangle_width, y, alpha=0.5, facecolor=color))
            area_approx += rectangle_width * y

    print('approximated area', area_approx)
    actual_area = 0.25 * 2.5 ** 4 - 2.5 ** 3 + 2.5 ** 2
    print('actual area', actual_area)
    print('error', area_approx - actual_area)


interact(render_riemann_sum, approx_type = approx_type_dropdown, num_rects=num_rects_slider)
```
