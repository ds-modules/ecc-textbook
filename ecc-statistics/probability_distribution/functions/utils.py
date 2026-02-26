import pandas as pd 
import numpy as np
import ipywidgets as widgets
import matplotlib.pyplot as plt
import seaborn as sn
from scipy import stats
import otter

from functions.interact import *

grader = otter.Notebook()

# Dictionary to store user answers for Otter Grader
user_answers = {}

### ---- PLOTTING FUNCTIONS ---- ###

def plot_bernoulli(p=0.5, highlight=1):
    x = np.array([0, 1])  # Bernoulli possible outcomes (0 or 1)
    y = stats.bernoulli.pmf(x, p)  # Probability mass function for Bernoulli

    plt.figure(figsize=(8, 5))
    plt.bar(x, y, color='blue', alpha=0.6, edgecolor='black', width=0.5, label="Bernoulli PMF")

    if highlight in x:
        plt.bar(highlight, stats.bernoulli.pmf(highlight, p), color='yellow', edgecolor='black', width=0.5, label=f'P(X={highlight})')

    plt.xlabel("X (Outcome)")
    plt.ylabel("Probability")
    plt.title(f"Bernoulli Distribution: P(X=1)={p}")
    plt.xticks(x, labels=["0 (Failure)", "1 (Success)"])
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

def plot_binomial(n=8, p=1/6, highlight=2):
    x = np.arange(0, n+1)  
    y = stats.binom.pmf(x, n, p)  

    plt.figure(figsize=(8, 5))
    plt.bar(x, y, color='blue', alpha=0.6, edgecolor='black', label="Binomial PMF")

    if highlight in x:
        plt.bar(highlight, stats.binom.pmf(highlight, n, p), color='yellow', edgecolor='black', label=f'P(X={highlight})');

    plt.xlabel("Number of Success in n Trials")
    plt.ylabel("Probability")
    plt.title(f"Binomial Distribution: n={n}, p={round(p, 3)}")
    plt.xticks(x)
    plt.legend()
    plt.grid(axis='y', linestyle='-', alpha=0.7)
    plt.show();

def plot_poisson(lam=3, highlight=2):
    x = np.arange(0, 50)  # Possible number of events (0 to 40)
    y = stats.poisson.pmf(x, lam)  

    plt.figure(figsize=(12, 6))
    plt.bar(x, y, color='blue', alpha=0.6, edgecolor='black', label="Poisson PMF")

    if highlight in x:
        plt.bar(highlight, stats.poisson.pmf(highlight, lam), color='yellow', edgecolor='black', label=f'P(X={highlight})');

    plt.xlabel("Number of Events (X)")
    plt.ylabel("Probability")
    plt.title(f"Poisson Distribution: λ={lam}")
    plt.xticks(x)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.show();


def plot_geometric(p=0.5, highlight=3):
    x = np.arange(1, 15)  # Possible number of trials until first success
    y = stats.geom.pmf(x, p)  # Probability mass function for Geometric

    plt.figure(figsize=(8, 5))
    plt.bar(x, y, color='blue', alpha=0.6, edgecolor='black', width=0.5, label="Geometric PMF")

    if highlight in x:
        plt.bar(highlight, stats.geom.pmf(highlight, p), color='yellow', edgecolor='black', width=0.5, label=f'P(X={highlight})')

    plt.xlabel("X (Number of Trials Until First Success)")
    plt.ylabel("Probability")
    plt.title(f"Geometric Distribution: P(Success)={p}")
    plt.xticks(x)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

### ---- MULTIPLE-CHOICE QUESTIONS ---- ###

def display_double_mc_question(q1_text, q1_choices, q1_id, q1_correct,
                               q2_text, q2_choices, q2_id, q2_correct):
    """Displays two multiple-choice questions and checks both on one submit."""
    
    # First question
    label1 = widgets.HTML(
        value=f"<div style='white-space: normal; word-wrap: break-word; line-height: 1.5;'>{q1_text}</div>"
    )
    radio1 = widgets.RadioButtons(options=q1_choices)

    # Second question
    label2 = widgets.HTML(
        value=f"<div style='white-space: normal; word-wrap: break-word; line-height: 1.5; margin-top: 20px;'>{q2_text}</div>"
    )
    radio2 = widgets.RadioButtons(options=q2_choices)

    # Submit button and output area
    submit_button = widgets.Button(description="Submit")
    output = widgets.Output()

    def on_submit(b):
        ans1 = radio1.value
        ans2 = radio2.value
        user_answers[q1_id] = ans1
        user_answers[q2_id] = ans2

        with output:
            output.clear_output()

            if ans1 == q1_correct and ans2 == q2_correct:
                print(f"✅ Correct!")
            else:
                print(f"❌ Try again...")

    submit_button.on_click(on_submit)

    display(widgets.VBox([label1, radio1, label2, radio2, submit_button, output]))


def q_2_3():
    display_double_mc_question(
    "Q2. Coin Flips: Adjust the parameters so it simulates a series of 15 coin flips. "
    "Assume that the coin is fair. What is the probability of getting 9 heads (X=9)?",
    ['50%', '15%', '2.5%', '100%'],
    "q2",
    "15%",

    "Q3. Dice Rolls: Adjust the parameters so it simulates 10 dice rolls. "
    "Assume that each side has equal landing chances. What is the probability of getting 5 fives?",
    ['14%', '4.20%', '3.4%', '1.3%'],
    "q3",
    "1.3%"
)

def q_4a_4b():
    display_double_mc_question(
        "Q4a. You spend a day at Flynn Cafe and notice that 14 customers come in, on average, every hour.\n\n"
        "What's the probability of 12 customers coming within the next hour?",
        [ 'close to 6%', 'close to 10%', 'close to 13%', 'close to 14%'],
        "q4a",
        'close to 10%',
         "Q4b. At a popular downtown coffee shop, the barista typically completes 4 drink orders every 10 minutes, on average.\n\n"
        "The manager wants to know how likely it is that exactly 4 orders will come in during a 10-minute period, to help prep resources.\n\n"
        "Assuming the number of customer orders follows a Poisson distribution, what is the probability that exactly 4 orders are placed in the next 10 minutes?",
        [ 'close to 6%', 'close to 10.5%', 'close to 16.5%', 'close to 20%'],
        "q4b",
        'close to 20%' 
    )

def q_6():
    display_double_mc_question(
        "Q6a. Say a customer calls about a cancellation refund issue. The support agent has a 66% chance of resolving the issue per attempt. What is the probability that the first successful resolution happens exactly on the 3rd attempt?",
        ['close to 8%', 'close to 10%', 'close to 26%', 'None of the above'],
        "q6a",
        "close to 8%",
        "Q6b. What happens as we increase the n-th attempt?",
        ['success increases', 'distribution changes', 'probability gets closer to 0', 'distribution does not change'],
        "q6b",
        "probability gets closer to 0"
    )


### ---- TEXTBOX QUESTION ---- ####

def display_text_question(question_text, q_id):
    """Displays an open-ended question with a text box for manual grading."""
    question_label = widgets.Label(value=question_text)
    text_area = widgets.Textarea(placeholder="Type your answer here")

    button = widgets.Button(description="Submit Answer")
    output = widgets.Output()

    def on_button_click(b):
        user_answers[q_id] = text_area.value  
        with output:
            output.clear_output()
            print("Answer submitted for manual grading.")

    button.on_click(on_button_click)
    display(widgets.VBox([question_label, text_area, button, output]))


def q_1():
    display_text_question(
        "Q1: What do you observe from this Bernoulli distribution as you adjust p for X?",
        "q1"
    )

def q_5():
    display_text_question(
        "Q5: Does the Poisson distribution inherently follow the normal distribution? Explain.",
        "q5"
    )

### ---- TEST FUNCTIONS FOR OTTER ---- ###

def test_q2():
    """Otter Grader test for Q2"""
    assert user_answers.get("q2", None) == '15%', "Incorrect! Please try again."

def test_q3():
    """Otter Grader test for Q3"""
    assert user_answers.get("q3", None) == '1.3%', "Incorrect! Please try again."

def test_q4a():
    """Otter Grader test for Q4"""
    assert user_answers.get("q4a", None) == 'close to 10%', "Incorrect! Please try again."
    
def test_q4b():
    """Otter Grader test for Q4"""
    assert user_answers.get("q4b", None) == 'close to 20%', "Incorrect! Please try again."

def test_q6a():
    """Otter Grader test for Q6"""
    assert user_answers.get("q6a", None) == 'close to 8%', "Incorrect! Please try again."

def test_q6b():
    """Otter Grader test for Q6"""
    assert user_answers.get("q6b", None) == 'probability gets closer to 0', "Incorrect! Please try again."

### ---- FUNCTION TO RUN OTTER TESTS ---- ###

def run_tests():
    """Runs Otter Grader tests for all questions, ensuring Q1 and Q5 are filled."""
    print("Running tests...\n")
    
    # Ensure Q1 and Q5 are answered before proceeding
    if not user_answers.get("q1", "").strip():
        print("❌ Q1: Please provide an answer in the text box before submitting.\n")
        return
    
    if not user_answers.get("q5", "").strip():
        print("❌ Q5: Please provide an answer in the text box before submitting.\n")
        return

    print("✅ Q1: Answer recorded for manual grading.")
    print("✅ Q5: Answer recorded for manual grading.\n")
    
    # Run auto-graded multiple-choice tests
    test_functions = [test_q2, test_q3, test_q4a, test_q4b, test_q6a, test_q6b]
    for test in test_functions:
        try:
            test()
            print(f"{test.__name__}: ✅ Passed")
        except AssertionError as e:
            print(f"{test.__name__}: ❌ {str(e)}")

    print("\nAll tests completed. Great work!")

### ---- FUNCTION TO SHOW PLOT AND QUESTIONS ---- ###

def show_bernoulli():
    bernoulli() # bernoulli(p)
    q_1()

