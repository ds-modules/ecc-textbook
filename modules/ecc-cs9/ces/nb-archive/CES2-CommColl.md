---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.2
kernelspec:
  display_name: base
  language: python
  name: python3
---

```{code-cell} ipython3
import pandas as pd
```

```{code-cell} ipython3
#cd EnviroScreen4
CES4 = pd.read_excel("calenviroscreen40resultsdatadictionary_F_2021.xlsx", sheet_name='CES4.0FINAL_results')
```

```{code-cell} ipython3
CES4
```

```{code-cell} ipython3
!ls
```

```{code-cell} ipython3
CollegeCodes= pd.read_excel("College_codes_EVDtype.xlsx")
CollegeCodes
```

```{code-cell} ipython3
#count if EVDCode = 1
CollegeCodes['EVDCode'].value_counts()
```

```{code-cell} ipython3
#drop rows where EVDCode = 4
CollegeCodes_Public = CollegeCodes[CollegeCodes['EVDCode'] != 4]
```

```{code-cell} ipython3
#merge CollegeCodes_Public with CES4
CES4_Public = pd.merge(CES4, CollegeCodes_Public, how='inner', left_on='ZIP', right_on='Zip')
```

```{code-cell} ipython3
# Find the most polluted zip codes and show the college there
CES4_Public.sort_values(by='CES 4.0 Score', ascending=False).head(10)
```

```{code-cell} ipython3
# Find the least polluted zip codes and show the college there
CES4_Public.sort_values(by='CES 4.0 Score', ascending=True).head(10)
```

```{code-cell} ipython3
# what is the score at El Camino College
CES4_Public[CES4_Public['College'] == 'EL CAMINO COLLEGE']
```
