from openai import OpenAI
import random
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Function to generate a random 10-digit number
def generate_10_digit_number():
    return random.randint(10**9, 10**10 - 1)

# Function to generate random triples (A, B, C) such that A > B > C
def generate_triple():
    A = generate_10_digit_number()
    B = random.randint(10**9, A - 1)  # Ensure B < A
    C = random.randint(10**9, B - 1)  # Ensure C < B
    return A, B, C

# Function to query OpenAI API if X > Y
def query_if_greater(X, Y):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers questions with 'yes' or 'no'."},
        {"role": "user", "content": f"Is {X} greater than {Y}?"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=2,
        temperature=0
    )
    
    answer = response.choices[0].message.content.strip().lower()
    return answer == 'yes'

# Main loop to generate and test triples
def main():
    n = 0
    for _ in range(100):  # Generate and test 100 triples
        A, B, C = generate_triple()

        # Query each condition
        A_greater_B = query_if_greater(A, B)
        B_greater_C = query_if_greater(B, C)
        C_greater_A = query_if_greater(C, A)

        # Print the triple if OpenAI API says C > A incorrectly
        if C_greater_A:
            print(f"Incorrectly identified triple: A={A}, B={B}, C={C}")
            print(f"OpenAI response: C > A: {C_greater_A}")
            n += 1
        else:
            print(f"Correct response: {A}, {B}, {C}")
    print(f"Number incorrect: {n}")

# Run the main function
main()
