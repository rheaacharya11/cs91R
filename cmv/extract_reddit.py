import json
import bz2
import pandas as pd

def extract_arguments_with_upvotes(file_path, max_threads=100):
    """Extract up to 3 arguments with upvotes from each thread and organize them into a single row."""
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
            
            # Add arguments to the dataset
            row = {
                'OP_Title': op_title,
                'OP_Text': op_text,
                'Argument_1_Text': extracted_args[0]['text'] if len(extracted_args) > 0 else None,
                'Argument_1_Success': extracted_args[0]['success'] if len(extracted_args) > 0 else None,
                'Argument_1_Upvotes': extracted_args[0]['upvotes'] if len(extracted_args) > 0 else None,
                'Argument_2_Text': extracted_args[1]['text'] if len(extracted_args) > 1 else None,
                'Argument_2_Success': extracted_args[1]['success'] if len(extracted_args) > 1 else None,
                'Argument_2_Upvotes': extracted_args[1]['upvotes'] if len(extracted_args) > 1 else None,
                'Argument_3_Text': extracted_args[2]['text'] if len(extracted_args) > 2 else None,
                'Argument_3_Success': extracted_args[2]['success'] if len(extracted_args) > 2 else None,
                'Argument_3_Upvotes': extracted_args[2]['upvotes'] if len(extracted_args) > 2 else None,
            }
            
            data.append(row)
            thread_count += 1
    
    return data

# Process only the first 100 valid threads from training data
train_data = extract_arguments_with_upvotes('train_period_data.jsonlist.bz2', max_threads=100)

# Convert to DataFrame and save
df = pd.DataFrame(train_data)
df.to_csv('../data/three_arguments.csv', index=False)

print("Sample dataset with upvotes successfully created and saved!")
