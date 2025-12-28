# Leap Year Checker

A simple Python program that determines whether a given year is a leap year or not.

## What is a Leap Year?

A leap year is a year with 366 days instead of the usual 365. The extra day is added to February, making it 29 days long instead of 28.

## Leap Year Rules

A year is a leap year if:

1. It is divisible by 4 **AND**
2. It is NOT divisible by 100 **OR** it is divisible by 400

### Examples

- **2024** → Leap year (divisible by 4, not by 100)
- **2000** → Leap year (divisible by 400)
- **1900** → Not a leap year (divisible by 100, not by 400)
- **2023** → Not a leap year (not divisible by 4)

## Features

- Interactive command-line interface
- Input validation
- Continuous checking until user quits
- Clear visual feedback

## Requirements

- Python 3.x

## How to Run

1. Save the program as `leap_year_checker.py`
2. Open your terminal or command prompt
3. Navigate to the directory containing the file
4. Run the program:

```bash
python leap_year_checker.py
```

## Usage

```
==========================================
      LEAP YEAR CHECKER
==========================================

Enter a year (or 'q' to quit): 2024
✓ 2024 is a LEAP YEAR! 🎉
  February 2024 has 29 days.

Enter a year (or 'q' to quit): 2023
✗ 2023 is NOT a leap year.
  February 2023 has 28 days.

Enter a year (or 'q' to quit): q

Goodbye!
```

## Code Structure

The program consists of two main functions:

- `is_leap_year(year)` - Implements the leap year logic
- `main()` - Handles user input and program flow

## License

Free to use and modify.