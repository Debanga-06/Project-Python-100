# Age Calculator

A simple Python script to calculate a person's age in years, months, and days based on their date of birth.

## Features

- **Input Formats**: Accepts date of birth in DD-MM-YYYY or DD/MM/YYYY format.
- **Age Calculation**: Computes age as total years, months, and remaining days from today.
- **Error Handling**: Validates input format and raises an error for invalid formats.

## Requirements

- Python 3.x

## How to Run

1. Run the `Age.py` script:
   ```
   python Age.py
   ```
2. Enter your date of birth when prompted.

## Usage

- Input your birthdate in the specified format (e.g., 15-08-1990 or 15/08/1990).
- The script will output your age in years, months, and days.

## Example

```
Enter your Date of Birth (DD-MM-YYYY or DD/MM/YYYY): 15-08-1990
Your Age: 35 years, 5 months, 1 days
```

## Notes

- Age calculation is approximate (uses 365 days per year and 30 days per month).
- Does not account for leap years or varying month lengths precisely.
- Input must be in DD-MM-YYYY or DD/MM/YYYY; other formats will raise an error.