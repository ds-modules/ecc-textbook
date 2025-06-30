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

```{code-cell} ipython3
:deletable: false
:editable: false

# Initialize Otter
import otter
grader = otter.Notebook("intro.ipynb")
```

+++ {"cell_id": "00001-eedf9a46-cb0c-42bc-a90f-96265663c0d3", "deepnote_cell_type": "markdown", "tags": ["ignore"]}

# Introduction to Jupyter Notebooks and Python

## Jupyter Notebooks

Welcome to a Jupyter Notebook! **Notebooks** are documents that support interactive computing in which code is interwoven with text, visualizations, and more.

The way notebooks are formatted encourages **exploration**, allowing users to iteratively update code and document the results. In use cases such as **data exploration and communication**, notebooks excel. Science (and computational work in general) has become quite sophisticated: models are built upon experiments that are conducted on large swaths of data, methods and results are abstracted away into symbols, and papers are full of technical jargon. *A static document like a paper might not be sufficient to both effectively communicate a new discovery and allow someone else to discover it for themselves*.

+++

## Introduction to Author

+++

Run the cell below to display a YouTube video about the author!

```{code-cell} ipython3
from IPython.display import YouTubeVideo

YouTubeVideo("jprUTEihBTo", width=560, height=315)
```

<div class="alert alert-block alert-danger">
    <p style="font-size:15px">In this notebook, there are some more advanced topics that are <i>"optional"</i>. This means you can just read over these sections, don't worry about fully understanding these parts unless you are really interested.
</div>

+++

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++

## Learning Outcomes
Working through this notebook, you will learn about:
1. The history behind **Jupyter notebooks** and why they are used in computing
2. How Jupyter notebooks are **structured** and **how to use them**
3. Python fundamentals and working with **tabular data**

+++

<div class="alert alert-block alert-info">
    <p style="font-size":15px"><b>Note: </b>This notebook introduces a number of Python concepts that will be new to some and review to others. Take a look at the entire notebook to guage your familiarity with the content before getting started. Start early, and don't be discouraged if each section requires a different time commitment!</p>
</div>

+++

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++

## Notebook Walk through 
In addition to the instructions in the notebook, we also have a video walkthrough of the entire process. We encourage you to refer to the video if you need help or even follow along with the instructor as you complete the task.

```{code-cell} ipython3
from IPython.display import YouTubeVideo

YouTubeVideo("Y2syTbw1ruI", width=560, height=315)
```

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++ {"cell_id": "00003-a9cd1167-2276-4e0f-85b6-43d803731627", "deepnote_cell_type": "markdown"}

## A Brief History
The Jupyter Notebook is an _interactive computational environment_ that supports over **40** different programming languages. [Fernando Perez](https://bids.berkeley.edu/people/fernando-p%C3%A9rez), a professor in the Statistics department at UC Berkeley, co-founded [Project Jupyter](https://bids.berkeley.edu/jupyter) in 2014. 

Though the Jupyter Notebook interface has been around only about a decade, the first notebook interface, [Mathematica](https://www.mathematica.org/), was released over 30 years ago in 1988.

+++

**Fun Etymology Fact!** \
Project Jupyter's name is a reference to the three core programming languages supported by Jupyter, which are `Julia`, `Python` and `R` (`"ju"` from `"Julia"`, `"pyt"` from `"Python"`, and `"er"` from `"R"`; all together you get `"ju" + "pyt" + "er" = "jupyter"`). The word notebook is an homage to Galileo's notebooks in which he documents his discovery of the moons of Jupiter.

+++ {"cell_id": "00004-6505161d-0615-4da6-bdf1-11b7204319a9", "deepnote_cell_type": "markdown"}

## Why Use Notebooks?
Notebooks are used for _literate programming_, a programming paradigm introduced by [Donald Knuth](https://en.wikipedia.org/wiki/Donald_Knuth) in 1984, in which a programming language is accompanied with **plain, explanatory language**.

This approach to programming treats software as works of literature ([Knuth](http://www.literateprogramming.com/knuthweb.pdf), "Literate Programming"), supporting users to have a strong conceptual map of what is happening in the code.

In addition to code and natural language, notebooks can include diagrams, visualizations, and rich media, making them useful in any discipline. They are also popular in education as a tool for engaging students at various skill levels with scaffolded and diverse lessons. 

+++

<div class="alert alert-block alert-info">
<b>Note:</b> In our class, we'll be using Jupyter Notebooks to introduce you to how data scientists work with data, to learn about issues of sociology/ ethnic studies using real-world data sets.
</div>

+++

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++ {"cell_id": "00003-058e2913-9587-45ac-8c2f-f284333ac4f3", "deepnote_cell_type": "markdown"}

## Notebook Structure

### Cell Types
A notebook is composed of rectangular sections called **cells**. There are 2 kinds of cells: markdown and code. 
- A **markdown cell**, such as this one, contains text. You will use this when answering writen question, mainly about drawing conclusions from our data. 
- A **code cell** contains code. In this class, we'll be using Python

### Running Cells
To "run" a code cell (i.e. tell the computer to perform the programmed instructions in the cell), select it and either:
- Press `Shift` + `Enter` to run the cell and move to (select) the following cell.
- Press `Command/Control` + `Enter` to run the cell but stay on the same cell. _This can be used to re-run the same cell repeatedly._

- Click the Run button in the toolbar at the top of the screen. 

### Results and Outputs of a Cell
When you run a code cell, a number of things can happen, depending on the type and contents of the cell:
1. Running a markdown cell renders the text inside of it.
2. Running a code cell returns the result of the code below the cell.
    - This output may be text, a number, a visualization, or nothing at all, depending on the code!

If a code cell is running, you will see an asterisk (\*) appear in the square brackets to the left of the cell. Once the cell has finished running, a number in brackets will replace the asterisk and any output from the code will appear under the cell. This number goes up by one each time you run a code cell, telling you the **order in which the code cells in your notebook have been run**.

Let's try it! **Run the cell below to see the output.** Feel free to play around with the code—try changing 'World' to your name, and re-run it multiple times to see how the number to the left increments.

```{code-cell} ipython3
:cell_id: 00004-a9f5f74b-a641-44a7-8dd5-2f9f58c10236
:deepnote_cell_type: code
:tags: [ignore]

print("Hello World!") # Run the cell by using one of the methods we mentioned above!
```

+++ {"cell_id": "00005-7327a678-bcb7-4a12-b09a-a4054660c9af", "deepnote_cell_type": "markdown", "tags": ["ignore"]}

### Comments
Notice the blue text that starts with a `#` in the code cell above. This is a **comment**. The leading `#` tells the computer to ignore whatever text follows it. Comments help programmers organize their code and make it easier interpret. Writing helpful comments is an essential tool when collaborating on a notebook.

+++

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++ {"cell_id": "00006-dadd2623-2173-4cdb-8c95-207741ecc765", "deepnote_cell_type": "markdown", "tags": ["ignore"]}

## Editing the Notebook

You can change the text in a markdown cell by clicking it twice. Text in markdown cells is written in [**Markdown**](https://daringfireball.net/projects/markdown/), a formatting language for plain text, so you may see some funky symbols should you try and edit a markdown cell we've already written. Once you've made changes to a markdown cell, you can exit editing mode by running the cell the same way you'd run a code cell. **Try double-clicking this text to see what some markdown formatting looks like**.

+++

<div class="alert alert-block alert-warning">
        <b>
            This cell is still a Markdown cell, but it uses HTML formatting to change its color and style. Try double-clicking on this text to see what some HTML formatting looks like.
        </b>
</div>

+++ {"cell_id": "00007-068d7862-911b-48aa-aa89-fe1376726a4f", "deepnote_cell_type": "markdown", "tags": ["ignore"]}

### Manipulating Cells

Cells can be added or deleted anywhere in a notebook. You can add cells by pressing the plus sign icon in the menu bar, to the right of the save icon. This will add (by default) a code cell immediately below your current highlighted cell.

To convert a cell to markdown, you can press 'Cell' in the menu bar, select 'Cell Type', and finally pick the desired option. This works the other way around too!

To delete a cell, simply press the scissors icon in the menu bar. A common fear is deleting a cell that you needed -- but don't worry! This can be undone using 'Edit' > 'Undo Delete Cells'! If you accidentally delete content in a cell, you can use `Ctrl` + `Z` to undo.

+++

<h3>Shortcuts</h3>

+++

<div class="alert alert-block alert-success">
    <p style="font-size:15px">This section is optional.
</div>

+++

Select a cell by clicking on the empty space to the left of the text (there will be a blue bar to the left of the cell at this point)
<ul>
<li>To <b>add a cell <i>below</i></b> the selected one, press the <code>b</code> key (<i>b for below</i>) </li>
<li>To <b>add a cell <i>above</i></b> the selected one, press the <code>a</code> key (<i>a for above</i>) </li>
<li>To <b>delete a cell</b>, press the <code>d</code> key (<i>d for delete</i>) </li>
<li>To <b>copy a cell</b>, press the <code>c</code> key (<i>c for copy</i>) </li>
<li>To <b>cut a cell</b>, press the <code>x</code> key (<i>same as the general cut text command</i>) </li>
<li>To <b>delete a cell</b>, press the <code>d</code> key <b><i>twice</i></b> (<i>d for delete, twice to ensure the action</i>) </li>
<li>To <b>paste a cell</b>, press the <code>v</code> key (<i>same as the general paste text command</i>) </li>
<li>To <b>convert a cell to a markdown cell</b>, press the <code>m</code> key (<i>m for markdown</i>) </li>
<li>To <b>convert a cell to a code cell</b>, press the <code>y</code> key </li>
</ul>

+++ {"cell_id": "00008-50df70cb-c544-42c2-8146-20897007051c", "deepnote_cell_type": "markdown", "tags": ["ignore"]}

### Saving and Loading

Your notebook will automatically save your text and code edits, as well as any results of your code cells. However, you can also manually save the notebook in its current state by using `Ctrl` + `S`, clicking the floppy disk icon in the toolbar at the top of the page, or by going to the 'File' menu and selecting 'Save and Checkpoint'.

Next time you open your notebook, it will look the same as when you last saved it!

+++

<div class="alert alert-block alert-info">
        <b>Note:</b> When you load a notebook you will see all the outputs from your last saved session (such as graphs, computations, etc.) but you won't be able to use any of the variables you assigned in your code without running it again. An easy way to reload your previous work is to select the cell you left off on and click <b>"Run all above"</b> from the <b>Cell</b> tab in the menu at the top of the screen.
</div>

+++

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++

## Python Basics
[**Python**](https://www.python.org/) is a programming language—a way for us to communicate with the computer and give it instructions.

Just like any language, Python has a set vocabulary made up of words it can understand, and a syntax which provides the rules for how to structure our commands and give instructions.

+++

### Math
Python is a great language for math, as it is easy to understand, and looks very similar to what it would look like in a regular scientific calculator.

- `+` Is the addition operator
- `-` Is the subtraction operator and can also act as a negative sign if next to a number (e.g., `-2` vs `- 2`)
- `*` Is the multiplication operator
- `**` Is the exponentiation operator
- `/` Is the division operator
- `()` Is the grouping operator

There are two types of numbers in python: Integers, also known as `int`, (e.g., `4`, `1000`) and decimal numbers, which are referred to as a `float` (e.g., `12.0`, `3.1415`). 

When using the `/` operator, even if the result is a whole number, the result will be a `float`. For example, `10 / 5` returns `2.0`, not `2`.

<div class="alert alert-block alert-info">
        
Let's look at some examples of using these operators. As usual, feel free to play around with these cells or even add new ones to explore how these operations work!

```{code-cell} ipython3
3 / 4
```

```{code-cell} ipython3
1 + 3
```

```{code-cell} ipython3
2 ** 3
```

```{code-cell} ipython3
4 ** .5
```

```{code-cell} ipython3
(6 + 4) * 2 - 15
```

### Practice

+++

<div class="alert alert-block alert-warning">
In the next cell, set x equal to 2 plus 7 multiplied by 40. Use the symbol key and the example cells above for guidance.
                                                                                                           </div>

```{code-cell} ipython3

```

### Strings
Strings are what we call words or text in Python. A string is surrounded in either single ('') or double ("") quotes. Here are some examples of strings

```{code-cell} ipython3
"This is a string"
```

```{code-cell} ipython3
'This is too'
```

You can even do math with strings, using `+` or `*` operators to modify them.

```{code-cell} ipython3
'Ha' * 10
```

```{code-cell} ipython3
"Ha" + " " + "Ha" + "     " + "Ha"
```

### Practice

+++

<div class="alert alert-block alert-warning">
     In the next cell, type in your favorite food in a string format. Don't forget to use quotation marks. 
</div>

```{code-cell} ipython3

```

+++ {"cell_id": "00012-b219d532-3d18-4f5b-8c0b-8300087fd4fc", "deepnote_cell_type": "markdown", "tags": ["ignore"]}

### Errors
Errors in programming are common and to be expected! Don't be afraid when you see an error because more likely than not the solution lies in the error code itself. Let's see what an error looks like. **Run the cell below to see the output.**

```{code-cell} ipython3
:cell_id: 00013-eb788b09-06e6-46f1-b6fd-5f63d3beaf17
:deepnote_cell_type: code
:tags: [ignore]

print('This line is missing something.' # We are missing a closing parenthesis here!
```

+++ {"cell_id": "00014-7e39cbe6-b521-4466-8200-3a4f652750f9", "deepnote_cell_type": "markdown", "tags": ["ignore"]}

The last line of the error output attempts to tell you what went wrong. 

The *syntax* of a language is its structure, and this `SyntaxError` tells you that you have created an illegal structure. Specifically, the error message `incomplete input` lets you know that the **computer expected a character in your code that wasn't found**. In this case, we forgot to add a closing parenthesis `)` to the end of our `print` statement.

There's a lot of terminology in programming languages, but you don't need to know it all in order to program effectively. If the terms in an error message confuse you, copying the entire message and searching it online is a tried and true first step.

+++ {"cell_id": "00015-6798c00d-6c61-4fb9-9db5-391b056d479c", "deepnote_cell_type": "markdown", "tags": ["ignore"]}

### Variables

In this Jupyter Notebook you will be assigning data, figures, numbers, text, or other objects to **variables**.  Variables are stored in a computer's **memory**, and can be used over and over again in future calculations.

Sometimes, instead of trying to work with raw information all the time in a long calculation you will want to store it as a **variable** for easy access in future calculations. **Check out how we can use variables to our advantage below!**

+++

<div class="alert alert-block alert-warning">
<b>Warning:</b> In Python, variable names must be a combination of letters (capital and/or lowercase), numbers, and underscores ( _ ). <b>Variable names <i>cannot</i> begin with a number.</b>
</div>

+++

- The following are all valid variable names:
    - `pants`, `pan_cakes`, `_`, `_no_fun`, `potato940`, `bowser_32`, `FOO`, `BaR`, `bAr`
    
- These are invalid names: 
    - `123`, `1_fun`, `f@ke`, `fun time`, `fun_times!!`, `00f00`

+++

## Assignment Statements
We use **assignment statements** to create a variable:

```{code-cell} ipython3
x = 1 + 2 + 3 + 4 
```

The first part of the statment is the name of the **variable**, in this case, `x`.

After the variable name, we write an equal sign (`=`).

On the right side of the equal sign, we give the variable a **value**. In this case, we assign x to be the result of adding `1 + 2 + 3 + 4`. 

+++

<div class="alert alert-block alert-info">
        <b>Note:</b> Notice above that a cell which contains an assignment statement doesn't output anything when run. If the last line of the cell "calls" the name of a variable that has already been assigned, however, it returns that variable's value. Pay attention to this behavior in the cells below.
</div>

```{code-cell} ipython3
x #just run this cell
```

You can also use previously assigned variables when assigning new ones, such as:

```{code-cell} ipython3
y = x * 2
y
```

### Variable Scope
Variable **scope** is a relatively complex topic that we don't need to be overly concerned with yet. That said, when a variable is used in the definition of another, we can encounter behavior we don’t expect if we aren't careful. **Run the following five cells in sequence.**

```{code-cell} ipython3
x = 5 # Assigns `x` to the value 5
```

```{code-cell} ipython3
y = x * 2 # Assigns `y` to the result of `x` * 2
```

```{code-cell} ipython3
y # Returns the current value of `y`
```

```{code-cell} ipython3
x = 10 # Re-assigns `x` to a new value
```

```{code-cell} ipython3
y # Returns the current value of `y`
```

_Why did the value of `y` stay the same after we changed the value of `x`?_

If a variable that is used in the definition of another variable (`x`) changes, the cell containing the assignment of the **outer** variable (`y`) must be re-run to take the **inner** variable’s new value into account.

Try rerunning the second and third cells above where we assign `y` and return its output. Notice how the value of `y`  only takes in the updated value of `x` after we re-run the cell where it is assigned!

+++

### Variable Examples
Let's look at a couple examples of when using variables can help us immensely!

+++

#### Example 1: Seconds in a Year
Let's say we want to find out how many seconds are in a year. We could calcluate it raw as following: $$60 \cdot 60 \cdot 24 \cdot 365$$ However, someone reading this may not understand what we are calculating or why, and we have no way to use the components or result of this calculation in other cells. Let's see how we can improve this process using variables:

```{code-cell} ipython3
days = 365 # The days in a year
hours = 24 # The hours in a day
minutes = 60 # The minutes in an hour
seconds = 60 # The seconds in a minute
seconds_per_year = days * hours * minutes * seconds # The seconds in a year
seconds_per_year
```

While lengthier, this method is far easier to understand, and we can use our new variable `seconds_per_year` to answer other questions!

Say we wanted to find the number of seconds in half a year, $7$ years, $234$ years, or even $3.1415$ years. Without variables, we calculating the number of seconds in each time period would be tedious and repetitive. With variables, it's much easier:

```{code-cell} ipython3
print("Seconds in half a year:", seconds_per_year / 2)
print("Seconds in seven years:", seconds_per_year * 7)
print("Seconds in two hundred and thirty-four years:", seconds_per_year * 243)
print("Seconds in 3.1415 years:", seconds_per_year * 3.1415)
```

#### Example 2: Equation of a Line
The equation of a line is: $$y = mx + b$$ We can use variables to easily calculate the $y$ for any $x$, and we can set $m$ (the slope) and $b$ (the intercept).

```{code-cell} ipython3
m = 1 # The slope
b = 5 # The intercept
x = 4 # Try changing this value to see how the output changes!
y = m * x + b
print(f"On the line y = {m}x + {b}, at x = {x}, y is equal to {y}")
```

### Practice 

+++

<div class="alert alert-block alert-warning">
Go back to the cell above where we defined m, b, x, and y, and change the numbers to create your own line.
</div>

+++

## Lists
The value of a variable can take on any number of **types**—it isn't limited to being an `integer`, `float`, or `string`.

One such type is a `list`, which can be used to store multiple values of any type. **Run the cells below.**

```{code-cell} ipython3
list_of_integers = [4,9,16]
list_of_integers
```

```{code-cell} ipython3
mixed_list = ["string", 2]
mixed_list
```

### Practice

+++

<div class="alert alert-block alert-warning">
Now create a list of your favorite songs (include more than one). Remember to write each song title as a string.
</div>

```{code-cell} ipython3
fav_songs= [] 
```

You can add and remove values from a list. In the following example, we add new elements to the list `running_totals`, which is the sum of all of the numbers in the list already.

+++

<div class="alert alert-block alert-success">
    <p style="font-size:15px">This example is advanced/optional.
</div>

```{code-cell} ipython3
running_totals = [1]
running_totals = running_totals + [sum(running_totals)]
running_totals = running_totals + [sum(running_totals)]
running_totals = running_totals + [sum(running_totals)]
running_totals = running_totals + [sum(running_totals)]
running_totals = running_totals + [sum(running_totals)]
running_totals = running_totals + [sum(running_totals)]
running_totals
```

<h2>Loops</h2>

+++

<div class="alert alert-block alert-success">
    <p style="font-size:15px">This section is advanced/optional.
</div>

+++

That code above is repetitive. Instead of typing that out, we can use a **for loop**. The cell below does the exact same thing as the cell above, but it is shorter and more straightforward. Check out [this documentation](https://www.w3schools.com/python/python_for_loops.asp) on for loops if you want to learn how this code works.

```{code-cell} ipython3
running_totals = [1]
for _ in range(6): 
    running_totals = running_totals + [sum(running_totals)]
running_totals
```

+++ {"cell_id": "00022-ad81de6d-4f04-4922-8b42-b54b01daeb8c", "deepnote_cell_type": "markdown"}

## Functions
We've seen that we can use **variables** to store and name values, but operations can also be named. A named operation is called a **function**. Python has some functions built into it.

```{code-cell} ipython3
:cell_id: 00023-7a1ac018-a44a-4e08-a681-2479fd06afed
:deepnote_cell_type: code

round # A built-in function.
```

To learn more about what a function does, follow its name with a question mark (?) to return its documentation.

```{code-cell} ipython3
round?
```

+++ {"cell_id": "00024-61af2610-4945-4252-86a1-a4f67e1cf4ce", "deepnote_cell_type": "markdown"}

Functions get used in **call expressions**, where a function is named and given values to operate on inside a set of parentheses. The `round` function returns the number it was given, rounded to the nearest whole number.

```{code-cell} ipython3
:cell_id: 00025-ddd3aeb9-2868-4a79-8404-5c5052baab1b
:deepnote_cell_type: code

round(1988.74699) # A call expression using the `round` function
```

+++ {"cell_id": "00027-27b5ba99-fd19-4093-9b69-1d42154c979f", "deepnote_cell_type": "markdown"}

The values a function is called on are called **arguments**, and each function places limitations on the number and type of arguments it can be called on. 

For instance, the minimum, `min`, and maximum, `max`, summation,`sum`, function will take as many integers or floats as you'd like, separated by commas, or a single `list`, and returns the smallest value.

```{code-cell} ipython3
:cell_id: 00027-26d2e33c-79e0-44b3-aad9-59361b3dba09
:deepnote_cell_type: code

min(9, -34, 0, 99)
```

```{code-cell} ipython3
max(9, -34, 0, 99)
```

Lets look at more examples of these functions and lists 

```{code-cell} ipython3
list_of_integers = [4,9,16] # this is the same list from above feel free to add more number to this list to see how the results change 
list_of_integers
```

```{code-cell} ipython3
sum(list_of_integers) 
```

```{code-cell} ipython3
max(list_of_integers)
```

```{code-cell} ipython3
min(list_of_integers) 
```

### Practice

+++

<div class="alert alert-block alert-warning">
    In the cell below, try to use one of the functions above on your fav_song list. 
</div>

```{code-cell} ipython3
  
```

### User-Defined Functions

+++

<div class="alert alert-block alert-success">
    <p style="font-size:15px">This section is advanced/optional
</div>

+++

One of the most useful features in python is the ability to define your own functions using a `def` statement.  Here is an example of one such function based on our earier example of seconds in one year:

```{code-cell} ipython3
def seconds(x): # Returns the number of seconds in `x` years
    days = 365
    hours = 24
    minutes = 60
    seconds = 60
    per_year = days * hours * minutes * seconds
    return per_year * x
```

Now we can use this function just like a built-in function!

```{code-cell} ipython3
seconds
```

```{code-cell} ipython3
seconds?
```

```{code-cell} ipython3
print("Seconds in one year:", seconds(1))
print("Seconds in 57 years:", seconds(57))
print("Seconds in 6.022 years:", round(seconds(6.022)))
print("Seconds since Berkeley was founded (the year 1868):", seconds(2022-1868))
```

### Practice

+++ {"cell_id": "00028-85d551d0-1121-4f0d-9b6d-da0049cad3e7", "deepnote_cell_type": "markdown"}

<div class="alert alert-block alert-warning">
    <li>The <code>abs</code> function takes one argument (just like <code>round</code>)</li>
    <li>The <code>max</code> function takes one or more arguments (just like <code>min</code>)</li>
</div>

+++


Try calling <code>abs</code> and <code>max</code> in the cell below. What does each function do?

Also try calling each function <i>incorrectly</i>, such as with the wrong number of arguments. What kinds of error messages do you see?

```{code-cell} ipython3
:cell_id: 00029-ba5cb6d4-659b-4236-87ba-a1cddd93da6f
:deepnote_cell_type: code

... # replace the "..." with calls to abs and max
```

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++ {"cell_id": "00009-52f60190-e21f-4107-99a9-d42ab128df40", "deepnote_cell_type": "markdown", "tags": ["ignore"]}

### Setting up an Environment

Now that we are comfortable working with notebooks, let's load some **libraries** that can help us explore the data we are working with. Python **libraries** (which you may also hear referred to as **packages**), contain individual Python files, called **modules**, written by other people that define **functions** we might find useful. We can **import** new **libraries**, or single **modules** into our active Python **environment** to access these functions without having to define them ourselves, or even understand how they work. This is an example of [**abstraction**](https://en.wikipedia.org/wiki/Abstraction_(computer_science)), a fundamental principle of computer science that values the utility gained from generalization and interchangibility.

You may have heard of popular data science **libraries** like `pandas`, `matplotlib`, or `numpy`, which provide functions to easily create and manipulate tables, produce visualizations, and calculate common statistics. Below we import the `datascience` library, as well as `numpy`, `math`, `random`, and `otter`.

```{code-cell} ipython3
:cell_id: 00010-be6eaa80-c135-4a5e-b17e-afa03953823b
:deepnote_cell_type: code
:tags: [ignore]

from datascience import * 
import numpy as np 
import math, random 
import otter 
import helper as hp
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Latex, Markdown
%matplotlib inline
import plotly.express as px
generator = otter.Notebook()
%matplotlib inline
```

Let's break down one of the import statements above: 

```python
import numpy as np
```

In the first half of the statement we import the NumPy library, equipping ourselves with the ability to use any of the functions defined in that library. In the second half, we use the `as` keyword to specify that we want to use some other name to refer to `numpy`; in this context we told python we want to call it `np`.

Lets say we want to use the `numpy.mean` function (this takes the mean of a list of numbers). Because we imported "`numpy`" as "`np`", we could now call `np.mean([...])` on any list.

Note: We name `numpy` as "`np`" because it is the standard name in the industry, however we could have said:

```python
import numpy as harrystyles
```
Which would've allowed us to run `harrystyles.mean()`. However, this would be confusing for a reader, so its considered best practice to use standard names such as "`np`" for "`numpy`" so that different people can read your work and not be confused as to what function you are using or what module it came from.

The cell below runs what we just talked about. Feel free to play around and try things out!

```{code-cell} ipython3
import numpy as harrystyles
import numpy as np
print("harrystyles and np are both NumPy?", harrystyles == np)
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
print(f"Harry Styles' mean of {numbers}:", harrystyles.mean(numbers))
print(f"NumPy's mean of {numbers}:", np.mean(numbers))

# This line delete the silly import of `harrystyles` that we just made. We'll use `np` from now own.
del harrystyles
```

+++ {"cell_id": "00030-114d6671-9eff-4835-a25c-11b521f0f643", "deepnote_cell_type": "markdown"}

#### Dot Notation
Python has a lot of [built-in functions](https://docs.python.org/3/library/functions.html) (that is, functions that are already named and defined in Python), but even more functions are stored in collections called **modules**. Earlier, we imported the `math` module so we could use it later. Like with the `np.mean()` example above, we can access a module's  functions by typing the name of the module, then the name of the function you want from it, separated with a `.`.

+++

<div class="alert alert-block alert-info">
<p style='font-size:15px'><b>Note:</b> If you type the name of a <i>module</i>, but can't remember the name of the function you're looking for, type a dot <code>.</code>, then press the <code>Tab</code> key to bring up an auto-complete menu to help you find the function you're looking for!
    </p>
</div>

```{code-cell} ipython3
:cell_id: 00031-9b6fdd99-2357-45c8-a6b2-ba29f6dfc470
:deepnote_cell_type: code

math.factorial(5) # A call expression with the factorial function from the math module
```

### Practice

+++ {"cell_id": "00032-6d349935-df0f-4c4d-96de-7d0769f50c3f", "deepnote_cell_type": "markdown"}

<div class="alert alert-block alert-warning">
    `math` also has a function called `sqrt` that takes one argument and returns the square root. Call `sqrt` on 16 in the next cell.
</div>

```{code-cell} ipython3

```

<!-- END QUESTION -->

### Random numbers and sampling
Random sampling plays a key role in data science. The random module implements functions for random sampling and random number generation. For example, the cell below generates a random integer between 1 and 50. 

Note that any whole number between 1 and 50 has an equal probability of being selected --- the sampling probabilities are uniform.

Try running this cell multiple times by holding `Command (mac)/Control (windows)` and pressing `Enter` repeatedly; notice how the output changes even though the code stays the same

```{code-cell} ipython3
random.randint(1,50)
```

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++ {"cell_id": "00021-9acaedfa-35c8-4480-9195-ff3f525895da", "deepnote_cell_type": "markdown", "tags": ["ignore"]}

## Tables

In most data science contexts, when interacting with data you will be working with **tables**. In this section, we will cover how to examine and manipulate data using Python. 

**Tables** are the fundamental way we organize and display data. 
**Run the cell below to load a dataset.** We'll be working with this data in a future notebook.

+++

It's important to understand where our data comes from. 

Our data is from the Neighborhood Data for Social Change (NDSC) is a project within the USC Lusk Center for Real Estate focused on using data to help local civic actors track measurable change, improve local policies and programs, and ultimately advocate for a better quality of life within their communities. The project includes a free, publicly available online resource that helps tell the stories of Los Angeles County neighborhoods in collaboration with local community leaders.

If you liked look at this data set, feel free to explore more at; https://map.myneighborhooddata.org/, after you finish the notebook 

We are going to look at the rates of diabities in various neighborhoods in LA, in the year 2021. Lets start by looking at our data set. 

```{code-cell} ipython3
diabetes = hp.diabetes
diabetes
```

+++ {"cell_id": "00023-b637dc20-fcb7-42c5-870f-622525214c86", "deepnote_cell_type": "markdown", "tags": ["ignore"]}

This table is organized into **columns**, one for each category of information collected, and rows, each containing all the information collected about a particular instance of data. In this case, each row contains information about a *different* neighborhood (no repeats).

    Neighborhoods:
    The name of the area or community in Los Angeles County being reported on.
    
    year:
    The year the data was collected — in this case, 2021.
    
    Population:
    The adult population (18 and over) of the neighborhood.
    
    Diabetes:
    The number of adults diagnosed with diabetes in that neighborhood.
    
    Median Household Income:
    The median income of households in that area, measured in U.S. dollars.
    
    Percent Diabetes:
    The proportion of the adult population with diabetes, calculated as Diabetes / Population. Expressed as a decimal (e.g., 0.00285 = 0.285%).
    
    Income Level:
    A categorical label indicating the general income tier of the neighborhood (e.g., High, High-Medium, Medium-High).
    

Every table has **attributes** that give information about the table, such as the number of rows and the number of columns. Attributes you'll use frequently include `num_rows` and `num_columns`, which give the number of rows and columns in the table, respectively. These are accessed using something called **dot notation** which means we won't be using any parentheses like in our print statement (Hello World!) earlier.

```{code-cell} ipython3
:cell_id: 00024-091f5f30-458c-4e85-8849-95aa1cad6cef
:deepnote_cell_type: code
:tags: [ignore]

diabetes.num_columns # Get the number of columns
```

```{code-cell} ipython3
:cell_id: 00025-381b6bb9-ff4a-4e83-8246-2de7e57405e8
:deepnote_cell_type: code
:tags: [ignore]

diabetes.num_rows # Get the number of rows
```

+++ {"cell_id": "00026-2e8333db-5536-4fdf-baae-ce481cd4cde1", "deepnote_cell_type": "markdown", "deletable": false, "editable": false, "tags": ["include"]}

<!-- BEGIN QUESTION -->



<div class="alert alert-block alert-danger">
<b>Question 1:</b>
Observe the output of the cell above. How many neighbors are included in our data set?
</div>


+++ {"tags": ["otter_answer_cell"]}

_Type your answer here, replacing this text._

+++ {"deletable": false, "editable": false}

<!-- END QUESTION -->

## Table Manipulation 
Below, we'll go through some basic table operations. Don't worry if this feels confusing at first—these are skills we'll build over time. For now, the goal is just to get familiar with these functions! 

+++

### Drop 
Our data is entirely from the year 2021, making the year column repetitive. Here's how we can remove: 

#### table.drop('column_name')

We need to reassign `diabetes` to the new table because this function creates a duplicate table and leaves the original unchanged.

```{code-cell} ipython3
diabetes = diabetes.drop('year')
diabetes
```

### Sort

Let's explore which neighborhood has the highest and lowest percentages of diabetes. One way to do this is by sorting the data.

In this case, we want to sort the rows by the `Percent Diabetes` column. Here’s the general format of the function:

#### table.sort('column name', ascending=True/False)

descending=False ,  arranges the rows from lowest to highest values in that column.

descending=True ,  arranges the rows from highest to lowest values in that column.

```{code-cell} ipython3
diabetes.sort('Percent Diabetes', descending=True)
```

### Practice 

+++

<div class="alert alert-block alert-warning">
    Change the code below so `descending = False` to see which neighborhood has the lowest diabetes rate 
</div>

```{code-cell} ipython3
diabetes.sort('Percent Diabetes', descending= ...)
```

+++ {"deletable": false, "editable": false}

<!-- BEGIN QUESTION -->



<div class="alert alert-block alert-danger">
<b>Question 2:</b>
Write your observations about our finding above. Answer the following questions below. 
What Neighborhood has the highest Diabetes rate? What Neighborhood has the lowest Diabetes rate? How does Median Household Income vary in the lowest versus highest Diabete rates?
</div>


+++ {"tags": ["otter_answer_cell"]}

_Type your answer here, replacing this text._

+++ {"cell_id": "00028-e7bb87b6-8935-4c5b-a6bf-9a27a890b69b", "deepnote_cell_type": "markdown", "deletable": false, "editable": false, "tags": ["ignore"]}

<!-- END QUESTION -->

<!-- END QUESTION -->

In other situations, we will want to sort, filter, or group our data. In order to manipulate our data stored in a table, we will be using various table functions. These will be explained as we go through them as to not overwhelm you!

#### A Note on Tables

In this notebook, we worked with the [datascience](http://data8.org/datascience/) library to work with tables (which is also used in Data-8). In future courses (such as Data-100) and in industry, you'll most likely use [pandas](https://pandas.pydata.org/) to manipulate tabular data. The datascience library is more user friendly, but pandas is more powerful overall. In this course, we'll use both.


Now that you have a basic grasp on Python and the kinds of information we'll be working with, we can move on to where our data came from and how to interact with it.

+++

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++

## Graphing
Looking at data tables is a great way to explore and analyze information, allowing us to identify patterns and trends. However, raw data alone can sometimes be overwhelming or difficult to interpret at a glance. That's where data visualization comes in—graphing your data provides a clearer, more intuitive way to spot trends, compare values, and communicate insights effectively. By using visual tools such as bar charts, scatter plots, and line graphs, we can make complex data more accessible and easier to understand.

There are lot of grpahs that we will be exploring in future notebooks, but for now will will just look at the basics 

+++

### Scatter 
A scatter plot is a type of graph that helps visualize the relationship between two numerical variables. Each point on the graph represents a single observation, with its position determined by the values of the two variables being compared. Scatter plots are particularly useful for identifying patterns, correlations, and outliers in data. 
                                                                                                                                                                                                                                                              
In the previous question, we asked you to consider the relationship between neighborhood diabetes rates and their average household income. Now, we’ll create a scatter plot to visualize this relationship.

    
By plotting diabetes rates on one axis and average household income on the other, we can observe whether there is a trend—do higher-income neighborhoods tend to have lower diabetes rates, or is there no clear pattern? This visualization will help us better understand how socioeconomic factors might influence health outcomes.

```{code-cell} ipython3
diabetes.scatter('Median Household Income', 'Diabetes')
plt.show()

#this is just extra for you to look at 
diabetes_df = diabetes.to_df()
sns.jointplot(data=diabetes_df, x='Median Household Income', y='Diabetes', kind='scatter', hue='Income Level' )
```

Neighborhoods with lower incomes often have higher rates of diabetes due to a combination of socioeconomic and environmental factors. Limited access to affordable, healthy food options can lead to higher consumption of processed and sugary foods, which increase the risk of diabetes. Additionally, lower-income areas may have fewer recreational spaces, making it harder for residents to engage in regular physical activity. Healthcare access also plays a significant role—without adequate insurance or nearby medical facilities, preventive care and early diagnosis become less common. Chronic stress from financial instability can further contribute to poor health outcomes, exacerbating conditions like diabetes.

+++

<hr style="border: 2px solid #003262">
<hr style="border: 2px solid #C9B676">

+++ {"cell_id": "00033-cdd8d4fd-d181-4b60-84c6-53fce944a344", "deepnote_cell_type": "markdown"}

## Notebooks in Practice

With proprietary software like *Mathematica*, users are supposed to trust the results returned and are unable to check the code. In contrast, *Jupyter* is open-source, which fosters **transparency** and encourages programmers to understand and **reproduce** the work of others.

[Theodore Gray](http://home.theodoregray.com/), the co-founder of [Wolfram Research](https://en.wikipedia.org/wiki/Wolfram_Research) who was also involved in creating the *Mathematica* interface, said about *Jupyter*,
>*"I think what they have is **acceptance from the scientific community** as a tool that is considered to be **universal**."*

In other words, *Jupyter Notebooks* support the computational work of researchers from different fields, enabling new ways for researchers in very different domains to **share research tools, methods, and learn from one another**.

The versatility of the Notebook has important consequences for data science and the workflows that are involved when working with data in settings other than research, such as for **education and community science projects**. The process of working with data can be messy and nonlinear, which a Jupyter notebook handles well because of its **flexibility**.

The power of the notebook lies in its ability to include a **variety of media** with the computation as a means to maintain **accountability, integrity, and transparency** for both the author of the notebook and the audiences that you share your work with. 

<div class="alert alert-block alert-warning">
In a world in which algorithms and data analysis inform many aspects of life and where computation is getting more and more abstract, the ability to understand and reason about computational work is more important than ever.
</div>

+++ {"deletable": false, "editable": false}

<!-- BEGIN QUESTION -->

<!-- BEGIN QUESTION -->

<div class="alert alert-block alert-danger">
<b>Question 3:</b> As we mentioned above, notebooks are used to make programming easier to read by interleaving code with text and other media types. Just as literature allows for creativity and supports multiple interpretations, we can treat notebooks as a medium that lets us tell complex stories that incorporate programming. What does that imply about notebooks as a medium and us as readers? Can you think of ways to incorporate them into justice projects?
</div>


<!--
BEGIN QUESTION
name: q3
points: 1
manual: true
-->

+++ {"tags": ["otter_answer_cell"]}

_Type your answer here, replacing this text._

+++ {"deletable": false, "editable": false}

<!-- END QUESTION -->

**Congratulations on finishing Notebook 1!**

The cell below generates a link to download your notebook as a zip file, which you can then submit.

**Before downloading, run all cells and save the notebook using `command`/`control` + `s` *or* clicking the save icon in the toolbar at the top of notebook. This is very important to ensure that all of your work shows up in the downloaded file!**

+++ {"deletable": false, "editable": false}

## Submission

Make sure you have run all cells in your notebook in order before running the cell below, so that all images/graphs appear in the output. The cell below will generate a zip file for you to submit. **Please save before exporting!**

```{code-cell} ipython3
:deletable: false
:editable: false

# Save your notebook first, then run this cell to export your submission.
grader.export()
```
