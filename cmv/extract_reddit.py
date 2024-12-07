import json
import bz2
import pandas as pd

def extract_arguments_with_upvotes(file_path, max_threads=100):
    """Extract up to 3 arguments with upvotes from each thread."""
    data = []
    thread_count = 0  # Counter to keep track of valid threads processed
    
    with bz2.open(file_path, 'rt') as f:
        for line_idx, line in enumerate(f):
            # Stop if we've processed the maximum number of valid threads
            if thread_count >= max_threads:
                break
            
            # Parse the thread
            thread = json.loads(line)
            op_title = thread.get('op_title', '')
            op_text = thread.get('op_text', '')
            
            # Skip threads with "Unknown" in title or text (case-insensitive)
            if "unknown" in op_title.lower() or "unknown" in op_text.lower():
                continue
            
            comments = thread.get('comments', [])
            
            # Debugging: Print details of the thread
            print(f"Thread {thread_count + 1}: Title: {op_title}")
            
            # Extract up to 3 arguments from comments
            extracted_args = []
            for comment in comments:
                # Extract relevant information from each comment
                body = comment.get('body', '')
                success = 'delta' in body.lower()  # Heuristic for success
                upvotes = comment.get('ups', 0)  # Get upvotes (defaults to 0 if missing)
                extracted_args.append({'text': body, 'success': success, 'upvotes': upvotes})
                
                # Stop once we've collected 3 arguments
                if len(extracted_args) >= 3:
                    break
            
            # Debugging: Print extracted arguments
            print(f"Extracted Arguments for Thread {thread_count + 1}: {extracted_args}")
            
            # Add arguments to the dataset
            for arg in extracted_args:
                data.append({
                    'OP_Title': op_title,
                    'OP_Text': op_text,
                    'Argument_Text': arg['text'],
                    'Success': arg['success'],
                    'Upvotes': arg['upvotes']
                })
            
            # Increment valid thread count
            thread_count += 1
    
    return data

# Process only the first 100 valid threads from training data
train_data = extract_arguments_with_upvotes('../data/all/train_period_data.jsonlist.bz2', max_threads=100)

# Convert to DataFrame and save
df = pd.DataFrame(train_data)
df.to_csv('../data/arguments_with_upvotes_sample.csv', index=False)

print("Sample dataset with upvotes successfully created and saved!")
