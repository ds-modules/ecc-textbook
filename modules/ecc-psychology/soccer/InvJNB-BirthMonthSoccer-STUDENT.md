---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.1
kernelspec:
  display_name: R
  language: R
  name: ir
---

<div class="alert alert-block alert-danger">

# InvJNB: Why Are Soccer Stars Born in January?

**Standalone Investigation Notebook**  
**Use with CourseKata intro chapters or as standalone**  
**Kernel: R**

</div>

+++

<div class="alert alert-block alert-warning">

## Summary of Notebook

Have you noticed that many professional soccer players seem to be born in January, February, or March? This investigation explores the "relative age effect"—a phenomenon where players born early in the year have advantages in youth sports due to age cutoffs. Students will examine birth month distributions of professional soccer players, compare observed patterns to expected uniform distributions, and explore how the effect varies across countries and positions.

### Includes

- Distribution analysis of birth months
- Expected vs. observed frequency comparisons
- Visualization of categorical distributions
- Cross-group comparisons (countries, positions)
- Optional: Quantifying the effect and historical trends

</div>

+++

<div class="alert alert-block alert-success">

## Approximate time to complete Notebook: 60-90 mins (depends on optional sections)

**Core sections (1.0-5.0): 60-75 mins**  
**With all optional advanced sections: 85-90 mins**

</div>

+++

<div class="alert alert-block alert-success">

### Intro — Approximate Time: 3-5 mins

</div>

+++

### The Relative Age Effect in Soccer

If you look at professional soccer players, you might notice something surprising: many of them were born in January, February, or March. This isn't a coincidence—it's called the **relative age effect**.

**The Problem:**
- Youth sports teams group players by birth year (e.g., all players born in 2005 play together)
- A player born in January 2005 is nearly a full year older than a player born in December 2005
- Older players in the same age group tend to be bigger, stronger, and more coordinated
- They get more playing time, better coaching, and more opportunities
- This advantage compounds over years, leading to overrepresentation of early-born players in professional leagues

**Research Question:**
Are professional soccer players born disproportionately in the first few months of the year?

**Study References:**
- Musch, J., & Grondin, S. (2001). Unequal competition as an impediment to personal development: A review of the relative age effect in sport. *Developmental Review*, 21(2), 147-167.
- Helsen, W. F., et al. (2005). The relative age effect in youth soccer across Europe. *Journal of Sports Sciences*, 23(6), 629-636.

+++

At the beginning of each notebook, load the packages you will use. Always run this first.

```{code-cell}
---
vscode:
  languageId: r
---
# Install coursekata if not already installed
if (!require("coursekata", quietly = TRUE)) {
    install.packages("coursekata", repos = "https://cloud.r-project.org")
}

suppressPackageStartupMessages({
    library(coursekata)
    library(dplyr)
    library(lubridate)
    library(tidyr)
})
```

<div class="alert alert-block alert-success">

### 1.0 — Approximate Time: 10-12 mins

</div>

+++

## 1.0 — Data Exploration

Let's start by loading and exploring the FIFA player data.

1.1 — Load the data and check its dimensions. How many players are in the dataset? What variables do we have?

```{code-cell}
---
vscode:
  languageId: r
---
# Load data from the same folder as this notebook
df <- read.csv("fifa_players.csv")

# Check dimensions
dim(df)

# Look at variable names
names(df)

# Look at first few rows
head(df[, c("name", "birth_date", "nationality", "positions")], 10)
```

__Type your answer here__

+++

1.2 — We need to extract the birth month from the birth_date. Run the code below to create a new variable called `birth_month` that contains just the month (1-12, where 1 = January, 12 = December).

```{code-cell}
---
vscode:
  languageId: r
---
# Convert birth_date to date format and extract month
df <- df %>%
  mutate(
    birth_date_parsed = as.Date(birth_date, format = "%m/%d/%Y"),
    birth_month = month(birth_date_parsed)
  )

# Check a few examples
head(df[, c("name", "birth_date", "birth_month")], 10)

# Verify we have all 12 months
table(df$birth_month)
```

<div class="alert alert-block alert-success">

### 2.0 — Approximate Time: 12-15 mins

</div>

+++

## 2.0 — Birth Month Distribution

Now let's examine the distribution of birth months among professional soccer players.

2.1 — Run the code below to count how many players were born in each month. Which months have the most players? Which have the fewest?

```{code-cell}
---
vscode:
  languageId: r
---
# Count players by birth month
tally(~ birth_month, data = df)

# Create a summary table with month names
month_names <- c("January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December")

birth_month_counts <- df %>%
  group_by(birth_month) %>%
  summarize(count = n()) %>%
  mutate(month_name = month_names[birth_month]) %>%
  arrange(birth_month)

birth_month_counts
```

__Type your answer here__

+++

2.2 — Run the code below to visualize the birth month distribution using `gf_bar()`. What pattern do you see?

```{code-cell}
---
vscode:
  languageId: r
---
# Create month name variable for better labels
df <- df %>%
  mutate(month_name = factor(month_names[birth_month], levels = month_names))

# Bar chart showing counts
gf_bar(~ month_name, data = df) %>%
  gf_labs(x = "Birth Month", y = "Number of Players",
          title = "Distribution of Birth Months Among Professional Soccer Players")
```

__Type your answer here__

+++

2.3 — Now run the code below to create a bar chart using `gf_props()` to show proportions instead of counts. Does this change how you interpret the pattern?

```{code-cell}
---
vscode:
  languageId: r
---
# Bar chart showing proportions
gf_props(~ month_name, data = df) %>%
  gf_labs(x = "Birth Month", y = "Proportion of Players",
          title = "Proportion of Players by Birth Month")
```

__Type your answer here__

+++

<div class="alert alert-block alert-success">

### 3.0 — Approximate Time: 15-18 mins

</div>

+++

## 3.0 — Expected vs. Observed

If birth months were completely random (uniformly distributed), what would we expect to see?

3.1 — Run the code below. If birth months were uniformly distributed, how many players would we expect in each month? (Hint: total players divided by 12)

```{code-cell}
---
vscode:
  languageId: r
---
# Calculate expected count per month (uniform distribution)
total_players <- nrow(df)
expected_per_month <- total_players / 12

cat("Total players:", total_players, "\n")
cat("Expected players per month (if uniform):", round(expected_per_month, 2), "\n")

# Add expected values to our summary
birth_month_summary <- df %>%
  group_by(birth_month, month_name) %>%
  summarize(observed = n(), .groups = 'drop') %>%
  mutate(expected = expected_per_month,
         difference = observed - expected)

birth_month_summary
```

__Type your answer here__

+++

3.2 — Run the code below to create a visualization that compares observed and expected counts. Which months are overrepresented (observed > expected)? Which are underrepresented (observed < expected)?

```{code-cell}
---
vscode:
  languageId: r
---
# Prepare data for comparison plot
comparison_data <- birth_month_summary %>%
  select(month_name, observed, expected) %>%
  pivot_longer(cols = c(observed, expected), 
               names_to = "type", 
               values_to = "count")

# Create comparison plot
gf_col(count ~ month_name, fill = ~ type, data = comparison_data, position = "dodge") %>%
  gf_labs(x = "Birth Month", y = "Number of Players", fill = "Type",
          title = "Observed vs. Expected Birth Month Distribution") %>%
  gf_hline(yintercept = ~ expected_per_month, linetype = "dashed", color = "gray")
```

__Type your answer here__

+++

3.3 — Run the code below to look at the differences (observed - expected). What's the largest positive difference? The largest negative difference? What does this tell us?

```{code-cell}
---
vscode:
  languageId: r
---
# Show differences sorted
birth_month_summary %>%
  arrange(desc(difference)) %>%
  select(month_name, observed, expected, difference)
```

__Type your answer here__

+++

<div class="alert alert-block alert-success">

### 4.0 — Approximate Time: 10-12 mins

</div>

+++

## 4.0 — The Relative Age Effect Explained

Now that we've seen the pattern, let's understand why it happens.

4.1 — In youth soccer, players are typically grouped by birth year. If the cutoff is January 1st, who would be in the same age group: a player born January 15, 2005 and a player born December 20, 2005, or a player born January 15, 2005 and a player born January 15, 2006?

4.2 — Why does being older within the same age group give an advantage? Think about physical and cognitive development.

+++

__Type your answer here__

+++

4.3 — Why is the effect especially strong in Italy? (Hint: Think about how Italy structures their youth leagues differently from other countries.)

+++

__Type your answer here__

+++

<div class="alert alert-block alert-success">

### 5.0 — Approximate Time: 12-15 mins

</div>

+++

## 5.0 — Comparing Across Groups

Does the relative age effect vary by country or position? Let's find out.

5.1 — Run the code below to compare the birth month distribution for Italian players versus players from other countries. Is the effect stronger in Italy?

```{code-cell}
---
vscode:
  languageId: r
---
# Create Italy vs. Other comparison
df <- df %>%
  mutate(country_group = ifelse(nationality == "Italy", "Italy", "Other Countries"))

# Count by country group and month (include birth_month to use later)
italy_comparison <- df %>%
  group_by(country_group, month_name, birth_month) %>%
  summarize(count = n(), .groups = 'drop') %>%
  group_by(country_group) %>%
  mutate(proportion = count / sum(count)) %>%
  ungroup()

# Show summary
italy_comparison %>%
  group_by(country_group) %>%
  summarize(
    jan_mar = sum(proportion[birth_month %in% 1:3]),
    oct_dec = sum(proportion[birth_month %in% 10:12]),
    .groups = 'drop'
  )
```

```{code-cell}
---
vscode:
  languageId: r
---
# Visualize with faceted plot
gf_props(~ month_name, data = df) %>%
  gf_facet_grid(. ~ country_group) %>%
  gf_labs(x = "Birth Month", y = "Proportion of Players",
          title = "Birth Month Distribution: Italy vs. Other Countries")
```

__Type your answer here__

+++

5.2 — Run the code below to see if the effect varies by position. Compare goalkeepers, defenders, midfielders, and forwards.

```{code-cell}
---
vscode:
  languageId: r
---
# Extract primary position (first position listed)
df <- df %>%
  mutate(
    primary_position = case_when(
      grepl("GK", positions) ~ "Goalkeeper",
      grepl("CB|LB|RB|LWB|RWB", positions) ~ "Defender",
      grepl("CM|CAM|CDM|LM|RM", positions) ~ "Midfielder",
      grepl("ST|CF|LW|RW", positions) ~ "Forward",
      TRUE ~ "Other"
    )
  )

# Filter to main positions and visualize
df_main_positions <- df %>%
  filter(primary_position != "Other")

gf_props(~ month_name, data = df_main_positions) %>%
  gf_facet_grid(. ~ primary_position) %>%
  gf_labs(x = "Birth Month", y = "Proportion of Players",
          title = "Birth Month Distribution by Position")
```

5.3 — What do you notice about the patterns across countries and positions? Are there any interesting differences?

+++

__Type your answer here__

+++

<div class="alert alert-block alert-success">

### Wrap-Up — Approximate Time: 3-5 mins

</div>

+++

### Summary and Implications

- What did we learn about birth month distributions in professional soccer?

+++

__Type your answer here__

+++

- Why does the relative age effect occur, and what are its consequences?

+++

__Type your answer here__

+++

- What are the implications for fairness in youth sports?

+++

__Type your answer here__

+++

- What potential solutions could address this issue?

+++

__Type your answer here__

+++

<div class="alert alert-block alert-info">

---

## Optional Advanced Sections

The sections below explore additional aspects of the relative age effect.

*Total additional time: ~20-30 mins*

</div>

+++

<div class="alert alert-block alert-success">

### A1.0 — Optional Advanced: Quantifying the Effect — Approximate Time: 8-10 mins

</div>

+++

## A1.0 — Quantifying the Effect

A1.1 — Run the code below. What percentage of players were born in Q1 (January-March) versus Q4 (October-December)? How much larger is Q1?

A1.2 — What does the Q1/Q4 ratio tell us?

```{code-cell}
---
vscode:
  languageId: r
---
# Calculate Q1 vs Q4
quarter_summary <- df %>%
  mutate(
    quarter = case_when(
      birth_month %in% 1:3 ~ "Q1 (Jan-Mar)",
      birth_month %in% 4:6 ~ "Q2 (Apr-Jun)",
      birth_month %in% 7:9 ~ "Q3 (Jul-Sep)",
      birth_month %in% 10:12 ~ "Q4 (Oct-Dec)"
    )
  ) %>%
  group_by(quarter) %>%
  summarize(
    count = n(),
    proportion = n() / nrow(df),
    .groups = 'drop'
  )

quarter_summary

# Calculate Q1/Q4 ratio
q1_count <- sum(df$birth_month %in% 1:3)
q4_count <- sum(df$birth_month %in% 10:12)
q1_q4_ratio <- q1_count / q4_count

cat("\nQ1 (Jan-Mar) players:", q1_count, "\n")
cat("Q4 (Oct-Dec) players:", q4_count, "\n")
cat("Q1/Q4 ratio:", round(q1_q4_ratio, 2), "\n")
cat("This means there are", round(q1_q4_ratio, 2), "times more Q1 players than Q4 players\n")
```

__Type your answer here__

+++

<div class="alert alert-block alert-success">

### A2.0 — Optional Advanced: Historical Trends — Approximate Time: 8-10 mins

</div>

+++

## A2.0 — Historical Trends

A2.1 — Run the code below. Does the relative age effect vary by decade? Has awareness of the issue changed the pattern over time?

```{code-cell}
---
vscode:
  languageId: r
---
# Extract birth year and create decade groups
df <- df %>%
  mutate(
    birth_year = year(birth_date_parsed),
    birth_decade = (birth_year %/% 10) * 10
  )

# Calculate Q1 proportion by decade
decade_effect <- df %>%
  mutate(q1_born = birth_month %in% 1:3) %>%
  group_by(birth_decade) %>%
  summarize(
    total = n(),
    q1_count = sum(q1_born),
    q1_proportion = mean(q1_born),
    .groups = 'drop'
  ) %>%
  arrange(birth_decade)

decade_effect

# Visualize trend
gf_col(q1_proportion ~ factor(birth_decade), data = decade_effect) %>%
  gf_hline(yintercept = 0.25, linetype = "dashed", color = "red") %>%
  gf_labs(x = "Birth Decade", y = "Proportion Born in Q1 (Jan-Mar)",
          title = "Relative Age Effect Over Time",
          subtitle = "Red line shows expected 25% if uniform")
```

__Type your answer here__

+++

<div class="alert alert-block alert-success">

### A3.0 — Optional Advanced: Other Sports Comparison — Approximate Time: 5-7 mins

</div>

+++

## A3.0 — Other Sports Comparison

A3.1 — The relative age effect has been documented in many sports. Research shows it's particularly strong in sports where physical maturity matters. How might the effect differ between soccer (where skill and endurance matter) versus sports like ice hockey (where size and strength are more important)?

A3.2 — If you had access to NHL player data, what pattern would you expect to see? Would it be stronger or weaker than in soccer?

+++

__Type your answer here__
