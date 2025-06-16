---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.2
kernelspec:
  display_name: venv
  language: python
  name: python3
---

## Notebook 1: Introduction to Jupyter Notebooks and Marketing Analytics

Welcome to a Jupyter Notebook! **Notebooks** are documents that support interactive computing in which code is interwoven with text, visualizations, and more.

The way notebooks are formatted encourages **exploration**, allowing users to iteratively update code and document the results. In use cases such as **data exploration and communication**, notebooks excel. Science (and computational work in general) has become quite sophisticated: models are built upon experiments that are conducted on large swaths of data, methods and results are abstracted away into symbols, and papers are full of technical jargon. *A static document like a paper might not be sufficient to both effectively communicate a new discovery and allow someone else to discover it for themselves*.

### Why Use Notebooks?
Notebooks are used for _literate programming_, a programming paradigm introduced by [Donald Knuth](https://en.wikipedia.org/wiki/Donald_Knuth) in 1984, in which a programming language is accompanied with **plain, explanatory language**.

This approach to programming treats software as works of literature ([Knuth](http://www.literateprogramming.com/knuthweb.pdf), "Literate Programming"), supporting users to have a strong conceptual map of what is happening in the code.

In addition to code and natural language, notebooks can include diagrams, visualizations, and rich media, making them useful in any discipline. They are also popular in education as a tool for engaging students at various skill levels with scaffolded and diverse lessons. 

```{code-cell} ipython3
print("Hello World!") # Run the cell by using one of the methods we mentioned above!
```

## Editing the Notebook

You can change the text in a markdown cell by clicking it twice. Text in markdown cells is written in [**Markdown**](https://daringfireball.net/projects/markdown/), a formatting language for plain text, so you may see some funky symbols should you try and edit a markdown cell we've already written. Once you've made changes to a markdown cell, you can exit editing mode by running the cell the same way you'd run a code cell. **Try double-clicking this text to see what some markdown formatting looks like**.

+++

### Manipulating Cells

Cells can be added or deleted anywhere in a notebook. You can add cells by pressing the plus sign icon in the menu bar, to the right of the save icon. This will add (by default) a code cell immediately below your current highlighted cell.

To convert a cell to markdown, you can press 'Cell' in the menu bar, select 'Cell Type', and finally pick the desired option. This works the other way around too!

To delete a cell, simply press the scissors icon in the menu bar. A common fear is deleting a cell that you needed -- but don't worry! This can be undone using 'Edit' > 'Undo Delete Cells'! If you accidentally delete content in a cell, you can use `Ctrl` + `Z` to undo.


### Saving and Loading

Your notebook will automatically save your text and code edits, as well as any results of your code cells. However, you can also manually save the notebook in its current state by using `Ctrl` + `S`, clicking the floppy disk icon in the toolbar at the top of the page, or by going to the 'File' menu and selecting 'Save and Checkpoint'.

Next time you open your notebook, it will look the same as when you last saved it!

Let's get started. Run the cell below to import all necessary libraries for this assignment!

```{code-cell} ipython3
from IPython.display import display
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from ipywidgets import *

def display_data(df, keyword):
    x = pd.to_datetime(df['Week'])
    y = df[keyword].astype("int64")
    sns.lineplot(x=x, y=y)
    plt.ylim((min(y), 100))

def state_name_to_abbreviation(state_name):
    state_abbreviations = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
        'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
        'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
        'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
        'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC'
    }
    return state_abbreviations.get(state_name, None)
```

## Case Study: Fast Food Frenzy

*Authored by Suparna Kompalli, James Geronimo*

Today we are going to do a deeper dive into **The 4 P's of Marketing** and **Search Engine Optimization (SEO)**. 

Search Engine Optimization (SEO) analytics play a critical role in the success of modern marketing campaigns. By analyzing data such as keyword performance, search trends, website traffic, and user behavior, businesses can optimize their online content to appear more prominently in search engine results. This ensures that advertisements and promotional efforts are not only high in quality but also strategically designed to reach the right audience at the right time—maximizing visibility, engagement, and conversions.

The 4 P’s of Marketing—product, price, placement, and promotion—are the key building blocks of any solid marketing strategy. They help businesses figure out what they’re selling, how much to charge, where to make it available, and how to let people know about it. When used together, these four elements help companies connect with their target customers in a way that feels thoughtful, strategic, and effective. Whether you're launching a new product or improving an existing one, the 4 P’s guide decisions that keep the brand relevant and competitive.

Let's do a quick warm up! What is the most important part of any marketing strategy? *the customer* 

To properly market anything, you'll need to have an understanding of your customer. 

As you know there are multiple factors that impact **consumer decision making.** These include:
- Price of the product
- Frequent purchase
- Length of time to research or available time to research
- Impulse buys
- Long term or temporary involvement

**Question 1:** If you were trying to sell apples on instagram what might be some keywords you'd want to include as hastags in your advertisements?

*Run the cell below to fill in your answer.*

```{code-cell} ipython3
widgets.Textarea(placeholder = 'Your answer here')
```


### Your Task:

You were hired to lead the marketing team at *Cluck & Co.,* a new fast food chain that has only one item on the menu: a chicken wrap. 

It’s a bold, flavorful item aimed at attracting Gen Z and millennial foodies who love spice, portability, and value. Leadership has asked your team to develop a marketing campaign for a regional test launch, and they want a strategy that’s both digitally savvy and grounded in classic marketing principles.

In this case study, we will walk you through building out the marketing strategy for Cluck & Co.


### Section 1: Product

**Product:** what you’re selling. Whether it's a physical good, a service, or a digital product. The key is to understand what problem your product solves and how it meets the needs or wants of your target audience.
- What features or benefits does it offer? How is it different from competitors?
- What branding and design choices are involved?


**Question 1.1:** Right now, our product seems a little *boring,* especially the name. What would you rename the **chicken wrap** to make it more enticing?

*Run the cell below to fill in your answer.*

```{code-cell} ipython3
widgets.Textarea(placeholder = 'Your answer here')
```

**Question 1.2:** We studied the concept of a **Total Product Offer** that consists of peripheral components to the product that provide more value to the customer than just the core product itself. We used the example of the iPhone, where customers buy the iPhone for more than just its core functions of calling, texting, and using apps. Consumers buy the iPhone for its total product offer that includes peripheral components such as accessories (iWatch or Ear Pods), interpretability across Apple devices, community of users, badge value of having an iPhone, Facetime, use of the Genius Bar at Apple stores and others. 

In the case of **Cluck and Co.'s chicken wrap**, consumers should buy it for more than the functionailty it serves as food--all restaurants fill this need. Why should customers eat at Cluck & Co? Design **TWO** peripheral componets of the chicken wrap's **Total Product Offer** that Cluck & Co. can highlight in the product or campaign. Why will these additions make the chicken wrap more desirable?

```{code-cell} ipython3
widgets.Textarea(placeholder = 'Your answer here')
```

### Section 2: Price

**Price:** how much you charge for your product. Price affects not only your profit margins but also how your product is perceived in the market.


**Question 2.1:** The pricing of Cluck & Co. is mid-tier: it's more expensive than McDonalds, and competitive with brands like Raising Cane's and Chick-fil-a. How does this pricing tier reflect the perceived value?

```{code-cell} ipython3
widgets.Textarea(placeholder = 'Your answer here')
```

**Question 2.2:** What role does price play in your digital advertising and promotions?

```{code-cell} ipython3
widgets.Textarea(placeholder = 'Your answer here')
```

### Section 3: Placement

**Placement:** where and how your product is distributed and made available to customers. It’s all about getting the product to the right place at the right time.
- Are you selling online? in physical stores?
- Where does your target market usually shop?

+++

When we think about placement we also want to consider geolocation. Let's take a look at where popular chicken only fast food chains are located. Run the cell below to load an *interactive* graph. 

```{code-cell} ipython3
restaurants = pd.read_csv('FastFoodRestaurants.csv')[['name', 'city', 'latitude', 'longitude', 'province', 'country']]
regional_chains = ['Waffle House', 'In-N-Out Burger', "Taco John's", "Whataburger", "Chick-fil-A"]
regional_restaurants = restaurants[restaurants['name'].isin(regional_chains)]

px.scatter_geo(regional_restaurants, lat = 'latitude', lon = 'longitude', color = 'name',
             locationmode='USA-states', scope = 'usa', title = 'Regional Fast Food Chains Across the US')
```

Location can help create a strong brand identity. Help Cluck & Co. decide what region to open their first stores. 

We will be visualizing Google Trends data to futher our search. This is a *free* tool you can access [here](https://trends.google.com/trends/) to explore the usage of search terms over time and by location. Feel free to try it out on your own time!

```{code-cell} ipython3
df = pd.read_csv('chicken_by_subregion.csv')
df["state_abbr"] = df["Region"].apply(state_name_to_abbreviation)

fig = px.choropleth(
    df, locations="state_abbr", locationmode="USA-states",
    color="chicken wrap", ## replace 'chicken wrap' in this line to change the visual below!
    scope="usa", hover_name="Region", hover_data={"chicken wrap": True, "chicken tenders": True, "chicken": True, "fried chicken": True})

fig.update_layout(
    title_text="Chicken Wrap Popularity by State",
    margin={"r":0,"t":30,"l":0,"b":0})

fig.show()
```

The numbers in each state toolbox represents in which location your term was most popular during the specified time frame. A value of 100 is the location with the most popularity as a fraction of total searches in that location. A value of 50 means that the term is *half as popular*. A score of 0 means there was not enough data for this term.

Note: A higher value means a higher proportion of all queries, not a higher absolute query count. So a tiny country where 80% of the queries are for "bananas" will get twice the score of a giant country where only 40% of the queries are for "bananas".

*You can color the map by the term **'chicken wrap'**, **'chicken tenders'**, **'fried chicken'**, or just **'chicken'**. 
Follow the comment in the code above and run the cell again to modify the visualization.*

**Question 3.1:** Cluck & Co. has the funding to open a location in **MAX THREE** states. Where should they choose? Why?

```{code-cell} ipython3
widgets.Textarea(placeholder='Your response here')
```

The above graph uses pre-selected keywords. Now it's time to choose your own!

**Question 3.2:** Using the [Google Trends](https://trends.google.com/trends/) website we explored above, what are THREE distinct keywords/search terms that you would use to market the chicken wrap? Be sure to discuss usage over time, geographic popularity, and related search queries. 

```{code-cell} ipython3
widgets.Textarea(placeholder='Your response here')
```

### Section 4: Promotion

**Promotion:** how you communicate the value of your product to your audience. It’s all about increasing awareness and persuading people to buy.
- What advertising channels do you use (TV, social media, influencer marketing, etc.)?
- What’s your messaging and tone?


##### The Promotion Mix (a.k.a. How You Get the Word Out)
When a company is trying to promote a product they usually don’t rely on just one method. Instead, they use a promotion mix, which is a combination of different strategies to grab attention, create interest, and encourage people to take action. There are four main parts of the promotion mix: advertising, personal selling, public relations, and sales promotion.

- **Advertising** is paid communication that’s shared through mass media—things like TV commercials, social media ads, etc.
- **Personal selling** describes real, face-to-face interaction like someone giving out samples, answering questions at a food truck, or even chatting with customers in-store.
- **Public relations (PR)** is about building an image and maintaining strong relationships with the public.
- **Sales promotion** is about limited-time deals and special offers that encourage people to act fast.

**Question 4.1:** The key to a strong marketing campaign is figuring out which mix of these strategies works best for your target audience. Cluck & Co. only has the funding to select **TWO** of the above elements for their **promotional mix** at the moment. Which two should they focus on and why?

*Hint: consider target market’s size, geographic or demographic influences, characteristics of the product (good, service, idea) and how the product is consumed, the price of the product (Intensive, Selective, Exclusive)

```{code-cell} ipython3
widgets.Textarea(placeholder='Your response here')
```

**Question 4.2:** Today we focused a lot on keyword searches, but customers derive information and opinions from many different sources. How successfully marketers use promotion to maintain positive relationships depends on some extent on the quantity and quality of information the organization receives.

What are some impactful **promotional channels** that Cluck & Co. can use to increase their presence? What are some other sources of information that would help inform a sucessful marketing campaign? 

```{code-cell} ipython3
widgets.Textarea(placeholder='Your response here')
```

###  Targeting Strategies

In marketing, there are three general targeting strategies: 
- The **undifferentiated strategy** involves offering one product or message to the entire market, treating all consumers as having the same needs. This approach aims for mass appeal and broad reach, like Coca-Cola promoting its classic drink to everyone. 
- The **concentrated strategy** focuses on a single, specific market segment. This is a niche approach where a company directs all its efforts toward serving one group exceptionally well, such as Rolex targeting only high-end luxury watch buyers. 
- The **differentiated strategy** targets multiple segments of the market by tailoring different products or marketing messages for each group. This allows a company to connect with diverse customer needs—like how Nike markets uniquely to runners, basketball players, and casual sneaker fans.

**Question 4.3:** Explain how each targeting strategy could be helpful or not helpful to Cluck & Co. Which targeting strategy would be most helpful to Cluck & Co.?

```{code-cell} ipython3
widgets.Textarea(placeholder='Your response here')
```

**Congratulations!!** You've successfully built out the marketing campaign for Cluck & Co.
