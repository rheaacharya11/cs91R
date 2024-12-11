import csv
import random
from openai import OpenAI
import os

# Initialize the OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_comparison(arg1, arg2, question, model, temperature):
    """
    Query OpenAI API to compare two arguments based on the given question and model.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant that evaluates which argument is more convincing."},
        {"role": "user", "content": f"{question} \nArgument 1: {arg1} \nArgument 2: {arg2}. Respond with just '1' or '2'."}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=50,
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

def save_argument_comparisons(filename, question, models, temperatures, data):
    """
    Compare arguments from the dataset and save preferences for different models and temperatures to a CSV file.
    
    Parameters:
        filename (str): Name of the output file.
        question (str): The question to ask OpenAI for comparisons.
        models (list): List of models to test (e.g., ['gpt-3.5-turbo', 'gpt-4']).
        temperatures (list): List of temperatures to test (e.g., [0, 0.7]).
        data (list of dict): List of data entries containing arguments to compare.
    """
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Header includes model-temperature-specific comparison columns
        header = ["OP_Title", "OP_Text", "Argument_1_Text", "Argument_2_Text", "Argument_3_Text"] + [
            f"{model}_temp_{temp}_Arg1_vs_Arg2" for model in models for temp in temperatures
        ] + [
            f"{model}_temp_{temp}_Arg2_vs_Arg3" for model in models for temp in temperatures
        ] + [
            f"{model}_temp_{temp}_Arg3_vs_Arg1" for model in models for temp in temperatures
        ]
        writer.writerow(header)

        for entry in data:
            op_title = entry["OP_Title"]
            op_text = entry["OP_Text"]
            arg1 = entry["Argument_1_Text"]
            arg2 = entry["Argument_2_Text"]
            arg3 = entry["Argument_3_Text"]

            # Store results for all models and temperatures
            results = [op_title, op_text, arg1, arg2, arg3]

            for model in models:
                for temp in temperatures:
                    # Query comparisons for this model and temperature
                    arg1_vs_arg2 = query_comparison(arg1, arg2, question, model, temp)
                    arg2_vs_arg3 = query_comparison(arg2, arg3, question, model, temp)
                    arg3_vs_arg1 = query_comparison(arg3, arg1, question, model, temp)

                    # Append model-temperature-specific results
                    results.extend([arg1_vs_arg2, arg2_vs_arg3, arg3_vs_arg1])
            
            # Write results to the CSV
            writer.writerow(results)

# Example dataset
with open("../data/three_arguments.csv", mode="r", newline="", encoding="utf-8") as file:
    data = list(csv.DictReader(file))

# Example usage
save_argument_comparisons(
    filename="argument_comparisons.csv",
    question="Which argument is better?",
    models=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"],
    temperatures=[0, 0.7],
    data=data
)
