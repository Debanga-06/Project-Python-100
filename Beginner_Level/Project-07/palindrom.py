# Advanced Level

def is_palindrome(text):
    """
    Check if a word or number is a palindrome.
    Ignores spaces, punctuation, and case.
    """
    # Remove spaces and convert to lowercase
    cleaned = ''.join(char.lower() for char in text if char.isalnum())
    
    # Check if it reads the same forward and backward
    return cleaned == cleaned[::-1]


def main():
    print("=" * 50)
    print("           PALINDROME FINDER")
    print("=" * 50)
    print("\nA palindrome reads the same forward and backward!")
    print("Examples: radar, 12321, A man a plan a canal Panama")
    
    while True:
        text = input("\nEnter a word or number (or 'q' to quit): ")
        
        if text.lower() == 'q':
            print("\nGoodbye!")
            break
        
        if not text.strip():
            print("Please enter something.")
            continue
        
        if is_palindrome(text):
            print(f"✓ '{text}' IS a palindrome! 🎉")
        else:
            print(f"✗ '{text}' is NOT a palindrome.")
            # Show the reverse
            cleaned = ''.join(char for char in text if char.isalnum())
            print(f"  Reversed: {cleaned[::-1]}")


if __name__ == "__main__":
    main()