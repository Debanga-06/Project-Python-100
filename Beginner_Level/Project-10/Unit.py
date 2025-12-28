def km_to_miles(km):
    return km * 0.621371


def miles_to_km(miles):
    return miles * 1.60934


def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32


def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9


def kg_to_lbs(kg):
    return kg * 2.20462


def lbs_to_kg(lbs):
    return lbs * 0.453592


def cm_to_inches(cm):
    return cm * 0.393701


def inches_to_cm(inches):
    return inches * 2.54


def liters_to_gallons(liters):
    return liters * 0.264172


def gallons_to_liters(gallons):
    return gallons * 3.78541


def main():
    print("=" * 50)
    print("           UNIT CONVERTER")
    print("=" * 50)
    
    conversions = {
        "1": ("Kilometers to Miles", km_to_miles, "km", "miles"),
        "2": ("Miles to Kilometers", miles_to_km, "miles", "km"),
        "3": ("Celsius to Fahrenheit", celsius_to_fahrenheit, "°C", "°F"),
        "4": ("Fahrenheit to Celsius", fahrenheit_to_celsius, "°F", "°C"),
        "5": ("Kilograms to Pounds", kg_to_lbs, "kg", "lbs"),
        "6": ("Pounds to Kilograms", lbs_to_kg, "lbs", "kg"),
        "7": ("Centimeters to Inches", cm_to_inches, "cm", "inches"),
        "8": ("Inches to Centimeters", inches_to_cm, "inches", "cm"),
        "9": ("Liters to Gallons", liters_to_gallons, "L", "gal"),
        "10": ("Gallons to Liters", gallons_to_liters, "gal", "L"),
    }
    
    while True:
        print("\n" + "-" * 50)
        print("Select conversion type:")
        print("-" * 50)
        
        for key, (name, _, _, _) in conversions.items():
            print(f"  {key}. {name}")
        
        print("  q. Quit")
        print("-" * 50)
        
        choice = input("\nYour choice: ").strip()
        
        if choice.lower() == 'q':
            print("\nGoodbye!")
            break
        
        if choice not in conversions:
            print("Invalid choice. Please try again.")
            continue
        
        name, func, from_unit, to_unit = conversions[choice]
        
        try:
            value = float(input(f"\nEnter value in {from_unit}: "))
            result = func(value)
            
            print("\n" + "=" * 50)
            print(f"  {value} {from_unit} = {result:.2f} {to_unit}")
            print("=" * 50)
            
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue


if __name__ == "__main__":
    main()
