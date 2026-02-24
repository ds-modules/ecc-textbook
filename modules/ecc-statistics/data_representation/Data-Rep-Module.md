---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
# Run this cell
from IPython.display import YouTubeVideo
from repfunctions.vis import *

import numpy as np
import pandas as pd
import scipy.stats as stats
```

___
**Estimated Time:** ~30 minutes  
**Developer:** Mark David Barranda
___

+++

- Introduction: Representation in Data
- Video: Diversity in Healthcare
- Data
- Visualizing Representation 
    - Race vs Occupation by Region
    - Race vs Educational Achievement by Region
- Discussion
    - Short Answer Question
- Conclusion

+++

# Introduction: Representation in Data

+++

The makeup of the health workforce plays a critical role in shaping health outcomes, especially for historically underserved populations. Despite the growing diversity of the U.S. population, racial and ethnic minorities remain underrepresented in many healthcare professions. For instance, although Black Americans make up over 12% of the working-age population, they account for just [5.4% of physicians](https://newsroom.ucla.edu/releases/proportion-black-physicians-little-change). Hispanic individuals—who represent 18.5% of the population—make up less than 6% of the physician workforce. These gaps reflect systemic barriers to access, education, and advancement in healthcare careers, and they raise concerns about the ability of the system to serve all communities equitably.

[Another research](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2772682) also shows that patients often experience better outcomes and greater trust when treated by healthcare providers who share their racial or cultural background. This connection can foster better communication, more accurate diagnoses, and improved patient satisfaction. A diverse health workforce also brings a wider range of perspectives, helping institutions identify and address health disparities more effectively. In this notebook, we’ll explore the relationship between race, occupation, and education in healthcare using real-world data, and reflect on why representation is not only a matter of justice—but also one of quality care. But first, let's hear some insights from two industry professionals below.

+++

## Video: Diversity in Healthcare

+++

Please watch the videos below titled "Lack of Diversity in Health Care: A Health Disparity" by Dr. Kiaana Howard, a physical therapist specializing in outpatient orthopedic and sports therapy and "How to get serious about diversity and inclusion in the workplace" by Janet Stovall. Their discussions focus on the critical issue of underrepresentation within the healthcare workforce, contributing to significant health disparities among marginalized communities. Advocating for *increased* inclusivity in healthcare professions is important as a means to enhance patient care and outcomes across diverse groups. 

```{code-cell} ipython3
YouTubeVideo('9W_kzItWm28', width=650, height=400)
```

```{code-cell} ipython3
YouTubeVideo('kvdHqS3ryw0', width=650, height=400)
```

## Data

+++

### Health Workforce Education Data - Race & Ethnicity

+++

**Source:** https://catalog.data.gov/dataset/health-workforce-education-data-85288    
**Data collection date:** July 1st, 2023

The dataset we will be working with contains statistically weighted estimates of initial education levels, highest education levels, and initial education locations for 43 key health workforce professions actively licensed in California as of July 1st, 2023. These metrics can be compared by workforce category, license type, time since license issue date (in years), race & ethnicity group, assigned sex at birth, and CHIS region.

**Run the cell below to load in the provided dataset**

```{code-cell} ipython3
file_path = "health-workforce-education-data-raceethnicity.xlsx"
xls = pd.ExcelFile(file_path)
xls.sheet_names
workforce_data = pd.read_excel(xls, sheet_name='Race & Ethnicity data')
```

**Feel free to uncomment the cell below to view the data**

```{code-cell} ipython3
#workforce_data
```

## Visualizing Representation

+++

## Race and Occupation by Region

+++

Below is a histogram displaying the distribution of health occupations by race in several regions in California. 

+++

_NOTE_: Use the interactive plot below to explore how representation in the health workforce changes across regions and occupations.

You can **adjust the dropdown menus** to:
- Select different **regions** of California
- Focus on specific **healthcare occupations**

As you change these options, watch how the histogram updates to show how the distribution of race and ethnicity shifts in each context.

```{code-cell} ipython3
run_workforce_plot(workforce_data)
```

## Race and Educational Achievement by Region

+++

Below is a histogram displaying the distribution of highest education level achieved by race in several regions in California.

+++

_NOTE_: Use the interactive plot below to explore how **highest education level** varies by race and ethnicity across regions.

You can **adjust the dropdown menus** to:
- Select different **regions** of California
- Focus on specific **highest education levels**

As you change these options, watch how the histogram updates to show how educational attainment is distributed across different race and ethnicity groups.

```{code-cell} ipython3
run_highedu_plot(workforce_data)
```

## Discussion

+++

The visualizations on race vs. occupation and race vs. education level paint a clear picture: systemic gaps in representation persist across healthcare professions. This matters not only for equity in employment but also for patient outcomes. Studies (listed below) have shown that patients often feel more understood, respected, and better cared for when treated by providers who share their cultural or linguistic background.    
- https://pmc.ncbi.nlm.nih.gov/articles/PMC1484660/pdf/jgi021-0203.pdf
- https://www.michiganmedicine.org/health-lab/minority-patients-benefit-having-minority-doctors-thats-hard-match-make     
- https://www.pennmedicine.org/news/news-releases/2020/november/study-finds-patients-prefer-doctors-who-share-their-same-race-ethnicity  
                                                                                                                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                             
**Short Answer:** Healthcare doesn’t exist in a vacuum. It reflects the broader systems that shape access to education, professional development, and institutional power. As future data scientists, health professionals, or policymakers, how can we use data to inform change?

+++

**Type your answer below.**

+++

Replace with your answer.

+++

## 📋 Post-Notebook Reflection Form

Thank you for completing the notebook! We’d love to hear your thoughts so we can continue improving and creating content that supports your learning.

Please take a few minutes to fill out this short reflection form:

👉 **[Click here to fill out the Reflection Form](https://forms.gle/oxkK6oh6Sv1K648L8)**

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

## Conclusion

+++

In this notebook, we used visualization to compare racial distributions across various healthcare occupations and education levels within California. 

+++

Congratulations on finishing the notebook!
