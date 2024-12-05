import json
import bz2
import csv
from collections import defaultdict

def parse_bz2_file(filepath):
    """
    Load a .bz2 file and parse its JSON lines.
    """
    data = []
    with bz2.open(filepath, 'rt') as file:
        for line in file:
            data.append(json.loads(line))
    return data

def group_comments_by_thread(reddit_data):
    """
    Group comments by their thread ID or context.
    
    Parameters:
        reddit_data (list): List of threads with comments from the dataset.
    
    Returns:
        dict: A dictionary where keys are thread IDs and values are lists of comments.
    """
    threads = defaultdict(list)
    
    for thread in reddit_data:
        # Replace 'op_name' with the actual field for thread ID
        context = thread.get("op_name", "Unknown Context")
        
        # Access the 'comments' field (adjust if nested)
        comments = thread.get("comments", [])
        
        for comment in comments:
            # Ensure the comment has a body
            if "body" in comment:
                threads[context].append(comment["body"])
    
    return threads

def generate_csv_with_three_responses(reddit_data, output_csv):
    """
    Generate a CSV file with threads containing at least three responses.
    
    Parameters:
        reddit_data (list): List of threads with comments from the dataset.
        output_csv (str): Path to the output CSV file.
    """
    # Group comments by thread
    threads = group_comments_by_thread(reddit_data)
    
    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Thread_ID", "Response_A", "Response_B", "Response_C"])
        
        for thread_id, responses in threads.items():
            # Skip threads with fewer than three responses
            if len(responses) < 3:
                continue
            
            # Write rows with three responses
            for i in range(len(responses) - 2):  # Sliding window of 3 comments
                response_a = responses[i]
                response_b = responses[i + 1]
                response_c = responses[i + 2]
                
                writer.writerow([thread_id, response_a, response_b, response_c])
    
    print(f"CSV generated with threads having at least three responses: {output_csv}")

# Example Usage
reddit_dataset_file = "pair_task/train_pair_data.jsonlist.bz2"  # Path to Reddit dataset
output_csv_file = "reddit_three_responses.csv"

# Parse the Reddit dataset
reddit_data = parse_bz2_file(reddit_dataset_file)

# Generate the CSV
generate_csv_with_three_responses(reddit_data, output_csv_file)
