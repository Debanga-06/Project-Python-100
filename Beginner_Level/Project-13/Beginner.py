# Fibonacci Sequence Generator

def fibonacci_sequence(n):
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

# Example usage
n = 10  # Change this value to generate more or fewer numbers
print(fibonacci_sequence(n))
