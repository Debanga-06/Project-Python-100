# Palindrome Finder

A Python program that checks if a word or number is a palindrome (reads the same forward and backward).

## What is a Palindrome?

A palindrome is a word, phrase, or sequence that reads the same backward as forward, ignoring spaces, punctuation, and capitalization.

### Examples

- **radar** → Palindrome
- **12321** → Palindrome
- **A man a plan a canal Panama** → Palindrome
- **hello** → Not a palindrome
- **racecar** → Palindrome

## Features

- Checks words, phrases, and numbers
- Ignores spaces, punctuation, and case
- Shows the reversed version for non-palindromes
- Interactive command-line interface
- Continuous checking until user quits

## Requirements

- Python 3.x

## How to Run

1. Save the program as `palindrome_finder.py`
2. Open your terminal or command prompt
3. Navigate to the directory containing the file
4. Run the program:

```bash
python palindrome_finder.py
```

## Usage

```
==================================================
           PALINDROME FINDER
==================================================

A palindrome reads the same forward and backward!
Examples: radar, 12321, A man a plan a canal Panama

Enter a word or number (or 'q' to quit): radar
✓ 'radar' IS a palindrome! 🎉

Enter a word or number (or 'q' to quit): hello
✗ 'hello' is NOT a palindrome.
  Reversed: olleh

Enter a word or number (or 'q' to quit): q

Goodbye!
```

## How It Works

The program:
1. Takes user input (word, phrase, or number)
2. Removes all non-alphanumeric characters
3. Converts to lowercase for case-insensitive comparison
4. Compares the cleaned string with its reverse
5. Reports whether it's a palindrome

## Code Structure

- `is_palindrome(text)` - Core function that checks if text is a palindrome
- `main()` - Handles user interaction and program flow

## License

Free to use and modify.