import csv
from openai import OpenAI
import random
import os

# Initialize the OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_persuasiveness(response1, response2, context):
    """
    Query OpenAI API to compare the persuasiveness of two responses.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers with just one response."},
        {"role": "user", "content": f"Here is the context: {context}\n\nWhich response is more persuasive?\n1: {response1}\n2: {response2}\nRespond with '1' or '2' only."}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=1,
        temperature=0
    )
    return response.choices[0].message.content.strip()

def detect_comparison_cycles(dataset, output_csv, trials=100):
    """
    Perform comparisons and detect cycles, saving results to a CSV file.
    
    Parameters:
        dataset (list): List of rows from the CSV file with context and responses.
        output_csv (str): Path to the CSV file to save results.
        trials (int): Number of random trials to perform.
    """
    total_cycles = 0
    
    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow([
            "Trial", "Context1", "Response1_1", "Response2_1", "Preferred1",
            "Context2", "Response1_2", "Response2_2", "Preferred2",
            "Context3", "Response1_3", "Response2_3", "Preferred3", "Cycle_Detected"
        ])
        
        for trial in range(trials):
            cycle_detected = False
            
            # Randomly sample three pairs from the dataset
            sampled_rows = random.sample(dataset, 3)
            response_pairs = [
                (sampled_rows[0], sampled_rows[1]),
                (sampled_rows[1], sampled_rows[2]),
                (sampled_rows[2], sampled_rows[0])
            ]
            
            # Compare responses and store preferences
            preferences = []
            for i, (row1, row2) in enumerate(response_pairs):
                context1 = row1["Context"]
                response1_1 = row1["Response1_Text"]
                response2_1 = row2["Response1_Text"]
                
                preferred = query_persuasiveness(response1_1, response2_1, context1)
                preferences.append(preferred)
            
            # Check for cycles
            if len(preferences) == 3 and len(set(preferences)) == 3:
                cycle_detected = True
                total_cycles += 1
            
            # Write results to CSV
            writer.writerow([
                trial + 1,
                response_pairs[0][0]["Context"], response_pairs[0][0]["Response1_Text"], response_pairs[0][1]["Response1_Text"], preferences[0],
                response_pairs[1][0]["Context"], response_pairs[1][0]["Response1_Text"], response_pairs[1][1]["Response1_Text"], preferences[1],
                response_pairs[2][0]["Context"], response_pairs[2][0]["Response1_Text"], response_pairs[2][1]["Response1_Text"], preferences[2],
                cycle_detected
            ])
    
    print(f"Total cycles detected: {total_cycles}")
    print(f"Results saved to {output_csv}")

# Load the dataset
def load_dataset(csv_file):
    """
    Load the dataset from the prepared CSV file.
    """
    dataset = []
    with open(csv_file, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dataset.append(row)
    return dataset

# Example usage
csv_file = "comparison_dataset.csv"  # Input dataset
output_csv = "comparison_results.csv"  # Output file
dataset = load_dataset(csv_file)

# Perform comparison cycles
detect_comparison_cycles(dataset, output_csv, trials=100)


