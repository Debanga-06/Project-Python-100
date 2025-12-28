import random
import string

def generate_password(length=12):
    if length < 6:
        raise ValueError("Password length should be at least 6 characters.")
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password

# Example usage
print(generate_password(12))
