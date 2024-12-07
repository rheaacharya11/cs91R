import pandas as pd
import csv

def compare_arguments(arg1, arg2):
    """
    Compare two arguments based on their upvotes.
    Returns the better argument ('arg1' or 'arg2') based on the number of upvotes.
    """
    if arg1[1] > arg2[1]:
        return "arg1"
    elif arg1[1] < arg2[1]:
        return "arg2"
    else:
        return "equal"  # If upvotes are tied


def check_for_cycle(pref_ab, pref_bc, pref_ca):
    """
    Check if the preferences form a cycle.
    A cycle exists if A > B, B > C, and C > A.
    """
    return pref_ab == "arg1" and pref_bc == "arg1" and pref_ca == "arg2"


def analyze_arguments(input_csv, output_csv):
    """
    Analyze the extracted arguments for pairwise comparisons and cycles.
    """
    # Read the input CSV
    df = pd.read_csv(input_csv)

    # Group by thread (OP_Title)
    grouped = df.groupby('OP_Title')

    # Prepare output file
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Thread_Title", "Arg1_Text", "Arg2_Text", "Arg3_Text",
                         "Arg1_Upvotes", "Arg2_Upvotes", "Arg3_Upvotes",
                         "A_vs_B", "B_vs_C", "C_vs_A", "Cycle"])

        # Process each thread
        for thread_title, group in grouped:
            # Ensure there are exactly 3 arguments in the thread
            if len(group) != 3:
                continue

            # Extract arguments and their upvotes
            args = group[['Argument_Text', 'Upvotes']].values.tolist()
            arg1, arg2, arg3 = args

            # Perform pairwise comparisons
            pref_ab = compare_arguments(arg1, arg2)
            pref_bc = compare_arguments(arg2, arg3)
            pref_ca = compare_arguments(arg3, arg1)

            # Check for cycles
            cycle = check_for_cycle(pref_ab, pref_bc, pref_ca)

            # Write results to CSV
            writer.writerow([
                thread_title,
                arg1[0], arg2[0], arg3[0],  # Argument texts
                arg1[1], arg2[1], arg3[1],  # Upvotes
                pref_ab, pref_bc, pref_ca,  # Pairwise preferences
                cycle                        # Cycle status
            ])
    print(f"Results saved to {output_csv}")


# Example usage
input_csv = '../data/arguments_with_upvotes_sample.csv'  # Path to the dataset we created earlier
output_csv = '../data/pairwise_analysis_with_cycles.csv'  # Path to save the results

analyze_arguments(input_csv, output_csv)
