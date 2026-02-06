---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.1
kernelspec:
  display_name: base
  language: python
  name: python3
---

```{code-cell} ipython3
import pandas as pd
```

```{code-cell} ipython3

CES4 = pd.read_excel("calenviroscreen40resultsdatadictionary_F_2021.xlsx", sheet_name='CES4.0FINAL_results')
```

```{code-cell} ipython3
CES4
```

```{code-cell} ipython3
CES4.columns
```

```{code-cell} ipython3
CES4.shape
```

```{code-cell} ipython3
#How many missging values are there in each column?
CES4.isnull().sum()
```

```{code-cell} ipython3
# count the number of counties in the data
CES4['California County'].nunique()
```

```{code-cell} ipython3
# count the number of unique census tracts in the data
CES4['Census Tract'].nunique()
```

```{code-cell} ipython3
# count the number of ZIP codes in the data
CES4['ZIP'].nunique()
```

```{code-cell} ipython3
# count the number of cities in the data
CES4['Approximate Location'].nunique()
```

```{code-cell} ipython3
# how many censustracts are in each city
CES4['Approximate Location'].value_counts()
```
