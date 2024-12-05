from openai import OpenAI
import random
import os

# Initialize the OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to generate a random two-digit number
def generate_2_digit_number():
    return random.randint(10**9, 10**10 - 1)

# Function to calculate the sum of prime factors of a number
def sum_of_prime_factors(n):
    prime_factors_sum = 0
    factor = 2
    while n > 1:
        while n % factor == 0:
            prime_factors_sum += factor
            n //= factor
        factor += 1
    return prime_factors_sum

# Function to generate random triples (A, B, C) sorted by sum of prime factors
def generate_triple():
    # Generate three random two-digit numbers
    A, B, C = generate_2_digit_number(), generate_2_digit_number(), generate_2_digit_number()
    
    # Calculate sum of prime factors for each number
    triples = [(A, sum_of_prime_factors(A)), (B, sum_of_prime_factors(B)), (C, sum_of_prime_factors(C))]
    
    # Sort the triples by the sum of prime factors in descending order
    triples.sort(key=lambda x: x[1], reverse=True)
    
    # Return the numbers ordered by their sum of prime factors
    return triples[0][0], triples[1][0], triples[2][0]

# Function to query OpenAI API if the sum of prime factors of X is greater than Y
def query_if_greater(X, Y):
    sum_X = sum_of_prime_factors(X)
    sum_Y = sum_of_prime_factors(Y)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers questions with 'yes' or 'no'."},
        {"role": "user", "content": f"In one second, tell me, would you guess the sum of prime factors of {X} ({sum_X}) greater than that of {Y} ({sum_Y})?"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2,
        temperature=0.7
    )
    
    answer = response.choices[0].message.content.strip().lower()
    return answer == 'yes'

# Main loop to generate and test triples with randomized query order
def main():
    n = 0
    for _ in range(100):  # Generate and test 100 triples
        A, B, C = generate_triple()
        
        # Define comparison pairs and shuffle them to randomize the query order
        comparisons = [(A, B), (B, C), (C, A)]
        random.shuffle(comparisons)
        
        # Dictionary to store results of comparisons
        results = {}
        
        # Perform each comparison in the randomized order
        for X, Y in comparisons:
            results[(X, Y)] = query_if_greater(X, Y)

        # Retrieve results in standard order for final check
        A_greater_B = results.get((A, B), False)
        B_greater_C = results.get((B, C), False)
        C_greater_A = results.get((C, A), False)

        # Print the triple if OpenAI API says C > A incorrectly
        if C_greater_A:
            print(f"Incorrectly identified triple: A={A}, B={B}, C={C}")
            print(f"OpenAI response: C > A: {C_greater_A}")
            n += 1
        else:
            print(f"Correct response: A={A}, B={B}, C={C}")
    print(f"Number incorrect: {n}")

# Run the main function
main()
