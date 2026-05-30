#!/usr/bin/env python
import sys
import warnings
from datetime import date
from datetime import datetime

from travelplanneragent.crew import Travelplanneragent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """

#   user_prompt = input("Enter your travel request: ")

    inputs = {
        'destination': "Delhi",
        'origin': "Indore",
        'start_date': str(date(2026, 5, 31)),
        'end_date': str(date(2026, 6, 5)),
        'trip_type': "Solo",
        'mode_of_transport': "Flight",
        'budget_total': 20000,
        'budget_currency': "INR",
        'num_travelers': 2
    }
    
    try:
        Travelplanneragent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }

    try:
        Travelplanneragent().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Travelplanneragent().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        Travelplanneragent().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
