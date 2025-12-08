# Odd/Even Number Checker

A simple Python program that determines whether a given number is odd or even.

## Description

This program accepts a numerical input from the user and checks if the number is odd or even using the modulo operator. It then displays the result in a user-friendly format.

## Features

- User-friendly input prompt
- Accurate odd/even determination
- Clean, formatted output
- Lightweight and efficient

## Requirements

- Python 3.x

## Installation

No installation required. Simply ensure you have Python 3 installed on your system.

To check your Python version:
```bash
python --version
```

## Usage

1. Run the program:
```bash
python odd_even_checker.py
```

2. Enter a number when prompted:
```
Enter a number: 7
```

3. View the result:
```
The number 7 is Odd.
```

## Code Example

```python
def check_odd_even(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

user_input = int(input("Enter a number: "))
result = check_odd_even(user_input)
print(f"The number {user_input} is {result}.")
```

## How It Works

The program uses the modulo operator (`%`) to divide the input number by 2:
- If the remainder is 0, the number is even
- If the remainder is not 0, the number is odd

## Error Handling

**Note:** This version does not include error handling. If a non-numeric value is entered, the program will raise a `ValueError`. Consider adding try-except blocks for production use.

## License

This project is open source and available for educational purposes.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the issues page if you want to contribute.

## Author

Debanga

## Acknowledgments

- Basic Python modulo arithmetic
- Python string formatting with f-strings