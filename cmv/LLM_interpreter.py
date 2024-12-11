import pandas as pd

# Load the CSV
file_path = "argument_comparisons.csv"
df = pd.read_csv(file_path)

# Function to extract the winner and map to the original argument
def map_original_argument(evaluation_text, column_name):
    """
    Determines which argument is better and maps it to the original argument number.
    Args:
        evaluation_text: The evaluation text that states the winner.
        column_name: The column name containing model information and comparison type.
    Returns:
        The original argument number (e.g., 1, 2, or 3) that corresponds to the winner.
    """
    if pd.isna(evaluation_text):
        return None  # Handle NaN values
    evaluation_text = str(evaluation_text).lower()
    
    # Identify the comparison type from the column name
    if "Arg1_vs_Arg2" in column_name:
        comparison_type = "Arg1_vs_Arg2"
    elif "Arg2_vs_Arg3" in column_name:
        comparison_type = "Arg2_vs_Arg3"
    elif "Arg3_vs_Arg1" in column_name:
        comparison_type = "Arg3_vs_Arg1"
    else:
        return None  # If column name does not match expected patterns
    
    # Determine the winner based on the evaluation text
    if "Argument 1" in evaluation_text or "1" in evaluation_text:
        if comparison_type == "Arg1_vs_Arg2":
            return 1
        elif comparison_type == "Arg2_vs_Arg3":
            return 2
        elif comparison_type == "Arg3_vs_Arg1":
            return 3
    elif "Argument 2" in evaluation_text or "2" in evaluation_text:
        if comparison_type == "Arg1_vs_Arg2":
            return 2
        elif comparison_type == "Arg2_vs_Arg3":
            return 3
        elif comparison_type == "Arg3_vs_Arg1":
            return 1
    else:
        return None

# Process all relevant columns
winner_columns = []  # Track winner columns to retain later
for col in df.columns:
    if any(key in col for key in ["Arg1_vs_Arg2", "Arg2_vs_Arg3", "Arg3_vs_Arg1"]):
        # Create a new column for the winner
        new_col_name = f"{col}_Winner_Original_Arg"
        df[new_col_name] = df[col].apply(lambda x: map_original_argument(x, col))
        winner_columns.append(new_col_name)

# Retain only the necessary columns (non-comparison and winner columns)
final_columns = [col for col in df.columns if col not in winner_columns and not any(key in col for key in ["Arg1_vs_Arg2", "Arg2_vs_Arg3", "Arg3_vs_Arg1"])]
final_columns.extend(winner_columns)  # Add winner columns to the final list
df_final = df[final_columns]

# Save the results to a new CSV
output_file = "processed_results_only_winners.csv"
df_final.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")
