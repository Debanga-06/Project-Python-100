# Text Analyzer

def analyze_text(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        
        # Calculate statistics
        word_count = len(text.split())
        line_count = len(text.splitlines())
        char_count = len(text)
        
        # String methods
        text_upper = text.upper()
        text_lower = text.lower()
        text_title = text.title()
        
        # Display results
        print(f"Word Count: {word_count}")
        print(f"Line Count: {line_count}")
        print(f"Character Count: {char_count}")
        print(f"Uppercase Text: {text_upper}")
        print(f"Lowercase Text: {text_lower}")
        print(f"Title Case Text: {text_title}")
        
    except FileNotFoundError:
        print("The specified file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
analyze_text('sample.txt')
