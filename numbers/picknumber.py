from openai import OpenAI
import random
import os

# Initialize the OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to generate a random x-digit number
def generate_number(x):
    return random.randint((10**(x-1)), (10**(x))-1)


# Function to generate random triples (A, B, C)
def generate_triple(x):
    A = generate_number(x)
    B = generate_number(x)  
    C = generate_number(x)  
    return A, B, C

# Function to query OpenAI API about comparison
def query_comparison(X, Y):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers with just one number"},
        {"role": "user", "content": f"Which number should I pick, {X} or {Y}? Respond with just the number"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=1,
        temperature=0
    )
    
    # Parse response 
    answer = response.choices[0].message.content.strip()
    return answer

# Main loop to generate and test triples with randomized query order
def main():
    for x in range(7, 12):
        print(f"{x}-digit number")
        total = 0
        for _ in range(3): # 3 trials
            n = 0
            for _ in range(100):  # Generate and test 100 triples
                A, B, C = generate_triple(x)
                
                # Define comparison pairs and shuffle them to randomize the query order
                comparisons = [(A, B), (B, C), (C, A)]
                random.shuffle(comparisons)
                
                # Dictionary to store preferences or "less than" results
                preferences = {}
                
                # Perform each comparison in the randomized order
                for X, Y in comparisons:
                    preferred = query_comparison(X, Y)
                    if preferred:
                        preferences[(X, Y)] = preferred

                ab = preferences.get((A, B))
                bc = preferences.get((B, C))
                ca = preferences.get((C, A))
        
                # Check for cycles
                cycle = len({ab, bc, ca}) == 3

                # Print the triple if any cycle is detected
                if (cycle):
                    n += 1
            print(f"Number of cycles detected: {n}")
            total += n
        print(f"Average: {total / 3}")

# Run the main function
main()
