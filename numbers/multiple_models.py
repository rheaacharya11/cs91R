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

def query_comparison(X, Y, question, model, temperature):
    """
    Query OpenAI API to compare two numbers based on the given question and model.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers with just one number."},
        {"role": "user", "content": f"{question} {X} or {Y}? Respond with just the number."}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=5,
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

def save_preferences_multiple_models_and_temps(filename, question, models, temperatures, min_digits=1, max_digits=10, trials_per_digit=100):
    """
    Run a series of comparisons for multiple digit lengths, models, and temperatures, then save results to a CSV file.
    
    Parameters:
        filename (str): The name of the file to save results to.
        question (str): The question to ask OpenAI for comparisons.
        models (list): List of models to test (e.g., ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo']).
        temperatures (list): List of temperatures to test (e.g., [0, 0.7]).
        min_digits (int): Minimum digit length (default is 1).
        max_digits (int): Maximum digit length (default is 10).
        trials_per_digit (int): Number of trials for each digit length (default is 100).
    """
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Header includes model-temperature-specific columns
        header = ["Digit_Length", "A", "B", "C"] + [
            f"{model}_temp_{temp}_A_vs_B" for model in models for temp in temperatures
        ] + [
            f"{model}_temp_{temp}_B_vs_C" for model in models for temp in temperatures
        ] + [
            f"{model}_temp_{temp}_C_vs_A" for model in models for temp in temperatures
        ]
        writer.writerow(header)

        for x_digits in range(min_digits, max_digits + 1):
            print(f"Processing {x_digits}-digit numbers...")
            for _ in range(trials_per_digit):
                # Generate a random triple
                A, B, C = generate_triple(x_digits)
                
                # Store results for all models and temperatures
                results = [x_digits, A, B, C]
                
                for model in models:
                    for temp in temperatures:
                        # Query all comparisons for this model and temperature
                        ab = query_comparison(A, B, question, model, temp)
                        bc = query_comparison(B, C, question, model, temp)
                        ca = query_comparison(C, A, question, model, temp)
                        
                        # Append model-temperature-specific results
                        results.extend([ab, bc, ca])
                
                # Write results to the CSV
                writer.writerow(results)
        print(f"Data saved to {filename}")

# Example usage
save_preferences_multiple_models_and_temps(
    filename="../results/number_hire_gpt.csv",
    question="Which number should I hire",
    models=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"],
    temperatures=[0, 0.7],
    min_digits=1,
    max_digits=10,
    trials_per_digit=100
)
