from datetime import datetime, date

def calculate_age(birthdate_str):
    # Accept both "-" and "/" separators
    if "-" in birthdate_str:
        birthdate = datetime.strptime(birthdate_str, "%d-%m-%Y").date()
    elif "/" in birthdate_str:
        birthdate = datetime.strptime(birthdate_str, "%d/%m/%Y").date()
    else:
        raise ValueError("Please enter date in DD-MM-YYYY or DD/MM/YYYY format")

    today = date.today()

    # Direct date arithmetic
    age_days = (today - birthdate).days   # total days difference
    age_years = age_days // 365           # rough years
    age_months = (age_days % 365) // 30   # rough months
    age_remaining_days = (age_days % 365) % 30

    return age_years, age_months, age_remaining_days

# Example usage
if __name__ == "__main__":
    dob = input("Enter your Date of Birth (DD-MM-YYYY or DD/MM/YYYY): ")
    years, months, days = calculate_age(dob)
    print(f"Your Age: {years} years, {months} months, {days} days")