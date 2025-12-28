# Advanced Level

def is_leap_year(year):
    """
    Check if a year is a leap year.
    
    Rules:
    - Divisible by 4: potential leap year
    - If divisible by 100: NOT a leap year
    - UNLESS also divisible by 400: IS a leap year
    """
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False


def main():
    print("=" * 40)
    print("      LEAP YEAR CHECKER")
    print("=" * 40)
    
    while True:
        try:
            year = input("\nEnter a year (or 'q' to quit): ")
            
            if year.lower() == 'q':
                print("\nGoodbye!")
                break
            
            year = int(year)
            
            if year < 1:
                print("Please enter a positive year.")
                continue
            
            if is_leap_year(year):
                print(f"✓ {year} is a LEAP YEAR! 🎉")
                print(f"  February {year} has 29 days.")
            else:
                print(f"✗ {year} is NOT a leap year.")
                print(f"  February {year} has 28 days.")
                
        except ValueError:
            print("Invalid input. Please enter a valid year.")


if __name__ == "__main__":
    main()