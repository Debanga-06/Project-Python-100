#Advanced Level

import random
import string


def generate_password(length=12, use_letters=True, use_numbers=True, use_symbols=True):
    """
    Generate a strong random password.
    """
    characters = ""
    
    if use_letters:
        characters += string.ascii_letters  # a-z, A-Z
    if use_numbers:
        characters += string.digits  # 0-9
    if use_symbols:
        characters += string.punctuation  # !@#$%^&*()_+-=[]{}|;:,.<>?
    
    if not characters:
        return "Error: Must select at least one character type!"
    
    # Generate password ensuring at least one of each selected type
    password = []
    
    if use_letters:
        password.append(random.choice(string.ascii_letters))
    if use_numbers:
        password.append(random.choice(string.digits))
    if use_symbols:
        password.append(random.choice(string.punctuation))
    
    # Fill the rest randomly
    for _ in range(length - len(password)):
        password.append(random.choice(characters))
    
    # Shuffle to avoid predictable patterns
    random.shuffle(password)
    
    return ''.join(password)


def main():
    print("=" * 50)
    print("         PASSWORD GENERATOR")
    print("=" * 50)
    
    while True:
        print("\n" + "-" * 50)
        
        try:
            length = input("Password length (8-32, default 12): ").strip()
            length = int(length) if length else 12
            
            if length < 8 or length > 32:
                print("Length must be between 8 and 32.")
                continue
            
            use_letters = input("Include letters? (Y/n): ").lower() != 'n'
            use_numbers = input("Include numbers? (Y/n): ").lower() != 'n'
            use_symbols = input("Include symbols? (Y/n): ").lower() != 'n'
            
            password = generate_password(length, use_letters, use_numbers, use_symbols)
            
            print("\n" + "=" * 50)
            print("Your generated password:")
            print(f"  {password}")
            print("=" * 50)
            
            # Password strength indicator
            strength = 0
            if use_letters: strength += 1
            if use_numbers: strength += 1
            if use_symbols: strength += 1
            if length >= 12: strength += 1
            
            if strength >= 4:
                print("Strength: 🟢 STRONG")
            elif strength >= 3:
                print("Strength: 🟡 MODERATE")
            else:
                print("Strength: 🔴 WEAK")
            
        except ValueError:
            print("Invalid input.")
            continue
        
        again = input("\nGenerate another? (Y/n): ")
        if again.lower() == 'n':
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()