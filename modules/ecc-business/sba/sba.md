---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.2
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# U.S. Small Business Association

+++

**Estimated Time**: 60 Minutes <br>
**Developers**: James Geronimo, Suparna Kompalli

+++

> Run the cell below before running any other code cells!

```{code-cell} ipython3
from utils import *
```

### Table of Contents
1. Background
2. About the Data
3. Inspecting the Data
4. Top States by SBA-Approved Loan Amounts
5. Top Cities by SBA-Approved Loan Amounts
6. Top Industries by SBA-Approved Loan Amounts
7. SBA Loan Counts and Proportions
8. Spotlight on Los Angeles

+++

---

+++

## 1. Background

Small businesses serve as a core component of innovation, employment, and community development in the United States. Since its founding in 1953, the **U.S. Small Business Administration (SBA)** has played a critical role in expanding access to capital by offering loan guarantees to small enterprises that may struggle to obtain funding through traditional credit markets.

The importance of supporting small businesses goes beyond economics — it fosters entrepreneurship, reduces unemployment, and strengthens local economies. However, these loans are not without risk; defaults and charge-offs are also part of the picture, especially in volatile or highly competitive industries.

+++

**Question 1.1**: What small business(es) in your local community hold importance in your everyday life?

+++

*Your Answer Here*

+++

**Question 1.2**: If you were to start your own small business, what would it specialize in and why?

+++

*Your Answer Here*

+++

---

+++

## 2. About the Data

In this notebook, we will analyze a comprehensive dataset from the SBA, originally sourced from Kaggle: 

> [Should This Loan Be Approved or Denied?](https://www.kaggle.com/datasets/mirbektoktogaraev/should-this-loan-be-approved-or-denied)

The dataset contains **899,164 SBA loan records** and includes detailed information about:

- Borrowers: business name, city, state, number of employees, franchise status
- Financials: approved loan amount, disbursed funds, charged-off amount
- Loan characteristics: approval year, loan term, revolving credit flag, LowDoc status
- Industry codes: using the NAICS classification system
- Job creation and retention estimates

This dataset provides a comprehensive view into the **geographic, demographic, and financial dimensions** of small business lending in the U.S. It offers a unique opportunity to explore a variety of questions regarding SBA-backed funding, successful industries, and loan approval trends.

Throughout this notebook, we will use **data visualizations, descriptive statistics**, and interactive tools to uncover insights about how and where SBA loans are distributed — and what that might say about the broader startup ecosystem.

For further academic insight, see the associated article by Li, Mickel, and Taylor (2018):  

> ["Should This Loan Be Approved or Denied?" A Large Dataset with Class Assignment Guidelines](https://www.tandfonline.com/doi/full/10.1080/10691898.2018.1434342)

+++

**Question 2**: Skim through the introduction of the paper linked above. What was the main purpose for the construction of the SBA's dataset?

+++

*Your Answer Here*

+++

---

+++

## 3. Inspecting the Data

We begin by importing the SBA loan dataset and displaying a `DataFrame` in the cell below.

To get a feel for the structure and contents of the dataset, we are showing the first 5 rows of the data in chunks of 9 columns at a time. This allows us to explore the **attributes associated with each loan**. For example, we can look into loan identifiers and business info, bank and loan approval information, and disbursement and financial data. Also, we've provided a data dictionary below:

### Data Dictionary

| Variable Name       | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| LoanNr_ChkDgt       | Identifier (Primary key)                                                    |
| Name                | Borrower name                                                               |
| City                | Borrower city                                                               |
| State               | Borrower state                                                              |
| Zip                 | Borrower zip code                                                           |
| Bank                | Bank name                                                                   |
| BankState           | Bank state                                                                  |
| NAICS               | North American Industry Classification System code                          |
| ApprovalDate        | Date SBA commitment was issued                                              |
| ApprovalFY          | Fiscal year of SBA commitment                                               |
| Term                | Loan term in months                                                         |
| NoEmp               | Number of business employees                                                |
| NewExist            | 1 = Existing business, 2 = New business                                     |
| CreateJob           | Number of jobs created                                                      |
| RetainedJob         | Number of jobs retained                                                     |
| FranchiseCode       | Franchise code (00000 or 00001 = No franchise)                              |
| UrbanRural          | 1 = Urban, 2 = Rural, 0 = Undefined                                         |
| RevLineCr           | Revolving line of credit (Y = Yes, N = No)                                  |
| LowDoc              | LowDoc Loan Program (Y = Yes, N = No)                                       |
| ChgOffDate          | Date when the loan was charged off (defaulted)                              |
| DisbursementDate    | Date when the loan was disbursed                                            |
| DisbursementGross   | Amount disbursed                                                            |
| BalanceGross        | Gross amount still outstanding                                              |
| MIS_Status          | Loan status (`CHGOFF` = charged off, `PIF` = paid in full)                  |
| ChgOffPrinGr        | Principal amount charged off                                                |
| GrAppv              | Gross amount of loan approved by the bank                                   |
| SBA_Appv            | SBA’s guaranteed portion of the approved loan                               |


This initial inspection is important for identifying which columns will be most useful in answering questions about geographic, financial, and industry-based trends in startup funding.

```{code-cell} ipython3
initial_inspection()
```

**Question 3**: How might using a data dictionary be useful when looking through our dataset?

+++

*Your Answer Here*

+++

## 4. Top States by SBA-Approved Loan Amounts

In this section, we investigate how SBA-approved funding is distributed geographically across U.S. states. Using a horizontal bar chart, we highlight the **top 15 states** by total approved loan volume.

The visualization uses a **green color gradient** to emphasize differences in loan volume, making it easier to compare across states.

This type of visualization helps reveal regional disparities in startup funding support. It also raises key analytical questions for further exploration:
- Are these funding trends proportional to state population?
- Do certain industries in these states receive preferential lending?
- Could local economic development policies be influencing loan approvals?

This sets the stage for deeper geographic or industry-specific analysis.

```{code-cell} ipython3
top_states_by_amount()
```

**Question 4.1**: What are the top states in this plot? Why might this be the case?

+++

*Your Answer Here*

+++

**Question 4.2**: What states did you expect to be higher (or lower) on this list?

+++

*Your Answer Here*

+++

---

+++

## 5. Top Cities by SBA-Approved Loan Amount

In this section, we drill down from states to individual cities to see where SBA-backed loans are most heavily concentrated. 

Down below, we plot the **top 20 cities** by total SBA-guaranteed approval amount, coloring bars by the state for additional geographic context.

```{code-cell} ipython3
top_cities_by_amount()
```

**Question 5.1**: Which three cities top this chart, and what factors (industry makeup, population, policies) might explain their high SBA-approved volumes?

+++

*Your Answer Here*

+++

**Question 5.2**: Do any states appear more than once among the top 20 cities? What might that tell you about how SBA funding is distributed within those states?

+++

*Your Answer Here*

+++

**Question 5.3**: How does the city-level picture compare to the state-level chart from Section 4? Do the same places dominate, or do we see different hotspots emerge?

+++

*Your Answer Here*

+++

---

+++

## 6. Top Industries by SBA-Approved Loan Amount

Having examined SBA-approved funding across **geography** (states in Section 4, cities in Section 5), we now turn to the **industry-level** to understand which economic sectors receive the most support. By grouping North American Industry Classification System (NAICS) codes by their first two digits, we aggregate individual industries into broader sectors (e.g., “72” = Accommodation & Food Services, “44” = Retail Trade). This enables us to compare sectors on a level playing field and uncover where SBA guarantees are most heavily concentrated.

Below, we have provided the **NAICS Sector Descriptions** table for you to reference the codes with their corresponding industries.

+++

| NAICS Code | Sector Description                                                               |
|------------|-----------------------------------------------------------------------------------|
| 11         | Agriculture, forestry, fishing and hunting                                       |
| 21         | Mining, quarrying, and oil and gas extraction                                    |
| 22         | Utilities                                                                         |
| 23         | Construction                                                                      |
| 31–33      | Manufacturing                                                                     |
| 42         | Wholesale trade                                                                   |
| 44–45      | Retail trade                                                                      |
| 48–49      | Transportation and warehousing                                                    |
| 51         | Information                                                                       |
| 52         | Finance and insurance                                                             |
| 53         | Real estate and rental and leasing                                                |
| 54         | Professional, scientific, and technical services                                  |
| 55         | Management of companies and enterprises                                           |
| 56         | Administrative and support and waste management and remediation services         |
| 61         | Educational services                                                              |
| 62         | Health care and social assistance                                                 |
| 71         | Arts, entertainment, and recreation                                               |
| 72         | Accommodation and food services                                                   |
| 81         | Other services (except public administration)                                     |
| 92         | Public administration                                                             |

+++

The chart generated below presents a horizontal bar plot of total SBA-approved loan amounts by NAICS sector code. The length and color intensity of each bar correspond to the scale of funding. These insights can help highlight sectoral priorities in small business financing, inform risk assessments, and guide entrepreneurs toward areas with robust SBA backing.

```{code-cell} ipython3
top_industries_by_amount()
```

**Question 6.1**: Which NAICS sector tops this chart, and why might it receive such high SBA support?

+++

*Your Answer Here*

+++

**Question 6.2**: Do any sectors surprise you with unexpectedly high or low funding levels? What factors might explain these outliers?  

+++

*Your Answer Here*

+++

**Question 6.3**: How do the industry-level patterns compare to the geographic trends we saw earlier? Are certain sectors clustered in particular states or cities? 

+++

*Your Answer Here*

+++

---

+++

## 7. SBA Loan Counts and Proportions

Up to now, we’ve focused on **total dollar‐value metrics**—total SBA-approved amounts by state, city, and industry. In this section, we examine two complementary views of SBA activity:

1. **Loan Count per State**: Shows the total number of SBA loans issued in each state, highlighting where the SBA is most active.
2. **Average SBA-Approved Amount per Loan**: Calculates the mean guaranteed loan amount per loan for each state, revealing where individual loans tend to be larger or smaller.

By comparing these two [choropleth](https://en.wikipedia.org/wiki/Choropleth_map) maps, we can see whether states with high loan volume also have high average loan sizes, or other trends are present.

```{code-cell} ipython3
loan_count_per_state()
```

```{code-cell} ipython3
avg_amount_per_loan_by_state()
```

**Question 7.1**: Which states have the highest loan counts, and do they also exhibit high average loan amounts? Does this differ from what we saw in Section 4?

+++

*Your Answer Here*

+++

**Question 7.2**: Identify any states with a high number of loans but a low average loan size (or vice versa). What might this indicate about small-business lending patterns in those states?

+++

*Your Answer Here*

+++

## 8. Spotlight on Los Angeles

In this section, we zero in on **Los Angeles, CA**, one of the country’s largest and most diverse startup ecosystems. First, we filter all SBA loans to those issued in Los Angeles and compute a concise **summary table** showing:
- **Total number of loans** backed by the SBA  
- **Total and average SBA-guaranteed amount** per loan  
- **Total jobs created** and **retained** by these businesses  

Next, we parse through the approval dates and plot a **year-over-year line chart** of total SBA-approved dollars, revealing how funding in LA has evolved over time.

```{code-cell} ipython3
los_angeles_summary()
```

```{code-cell} ipython3
annual_sba_approved_amount_la()
```

**Question 8.1**: Based on the summary table, which metric surprised you most, and what might explain that result in the context of LA’s economy?  

+++

*Your Answer Here*

+++

**Question 8.2**: Examine the annual line chart—identify any sharp increases or declines. What local or national events (like policy changes or economic events) could correlate with those inflection points?  

+++

*Your Answer Here*

+++

---

+++

### ✅ Congrats! You've completed the SBA loan exploration notebook! 🎉
