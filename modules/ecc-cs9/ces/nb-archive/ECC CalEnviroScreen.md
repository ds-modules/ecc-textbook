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

# [El Camino College] Notebook: CalEnviroScreen Exploration

**This notebook will put together everything you've learned so far and include new ways of interpreting data .**

### Learning Objectives

In this notebook, you will learn about:
- *insert learning objectives*

### Table of Contents
   
1. [Introduction](#0) <br>

-------------------------------------------------------------------

+++

## 1. Introduction <a id='0'></a>

+++

→ Explore the data, observe how many rows/columns and what they correspond to \
→ Subset different LA census tracts including El Camino's (create interactive graph they can play around with) \
→ Local rates of (asthma, pollution ) , LA wide rates, Cal  state wide (ex. compare local to higher level state averages)

```{code-cell} ipython3
import numpy as np
import pandas as pd
```

```{code-cell} ipython3
enviro = pd.read_csv('enviro.csv')
enviro
```

Let's take a look at El Camino College's census tract data. Their tract # is **6037603702**.

```{code-cell} ipython3
ecc = enviro[enviro['Census Tract'] == 6037603702]
ecc
```

## 2. Exploring by Region <a id='1'></a>

+++

→ Split data into different neighborhoods of LA \
→ Focus subsetting health outcomes (PM2.5, lead, groundwater threats, pollution burden, asthma), particularly in lower-income neighborhoods

```{code-cell} ipython3

```
