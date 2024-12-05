import csv
import random
from openai import OpenAI
import os

# Initialize the OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_number(x):
    """Generate a random x-digit number."""
    return random.randint(10 ** (x - 1), 10 ** x - 1)

def generate_triple(x):
    """Generate a random triple (A, B, C) of x-digit numbers."""
    return generate_number(x), generate_number(x), generate_number(x)

def query_comparison(X, Y, question):
    """
    Query OpenAI API to compare two numbers based on the given question.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers with just one number."},
        {"role": "user", "content": f"{question} {X} or {Y}? Respond with just the number."}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=1,
        temperature=0
    )
    return response.choices[0].message.content.strip()

def save_preferences_multiple_digits(filename, question, min_digits=1, max_digits=10, trials_per_digit=100):
    """
    Run a series of comparisons for multiple digit lengths and save results to a CSV file.
    
    Parameters:
        filename (str): The name of the file to save results to.
        question (str): The question to ask OpenAI for comparisons.
        min_digits (int): Minimum digit length (default is 1).
        max_digits (int): Maximum digit length (default is 10).
        trials_per_digit (int): Number of trials for each digit length (default is 100).
    """
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Digit_Length", "A", "B", "C", "A_vs_B", "B_vs_C", "C_vs_A", "Cycle"])

        for x_digits in range(min_digits, max_digits + 1):
            print(f"Processing {x_digits}-digit numbers...")
            for _ in range(trials_per_digit):
                A, B, C = generate_triple(x_digits)
                
                # Define comparison pairs and shuffle them to randomize the query order
                comparisons = [(A, B), (B, C), (C, A)]
                random.shuffle(comparisons)
                
                # Dictionary to store preferences
                preferences = {}
                
                # Query OpenAI for each comparison
                for X, Y in comparisons:
                    preferences[(X, Y)] = query_comparison(X, Y, question)
                
                # Retrieve preferences
                ab = preferences.get((A, B), "N/A")
                bc = preferences.get((B, C), "N/A")
                ca = preferences.get((C, A), "N/A")
                
                # Check for cycles
                cycle = len({ab, bc, ca}) == 3
                
                # Write the preferences and cycle info to the CSV
                writer.writerow([x_digits, A, B, C, ab, bc, ca, cycle])
        print(f"Data saved to {filename}")

# Example usage
save_preferences_multiple_digits(
    filename="lotto_10.csv",
    question="Which number is more balanced",
    min_digits=1,
    max_digits=10,
    trials_per_digit=100
)
