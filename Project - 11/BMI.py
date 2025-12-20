"""
BMI Calculator 
Calculate Body Mass Index and provide health category classification.
"""


def calculate_bmi(weight_kg, height_m):
    """
    Calculate BMI using the formula: BMI = weight(kg) / height(m)^2
    
    Args:
        weight_kg (float): Weight in kilograms
        height_m (float): Height in meters
    
    Returns:
        float: Calculated BMI value
    """
    return weight_kg / (height_m ** 2)


def get_bmi_category(bmi):
    """
    Determine BMI category based on WHO standards.
    
    Args:
        bmi (float): BMI value
    
    Returns:
        tuple: (category, description, emoji)
    """
    if bmi < 16.0:
        return ("Severe Underweight", "Seek medical attention", "🔴")
    elif bmi < 18.5:
        return ("Underweight", "Consider gaining weight", "🟡")
    elif bmi < 25.0:
        return ("Normal Weight", "Maintain healthy lifestyle", "🟢")
    elif bmi < 30.0:
        return ("Overweight", "Consider losing weight", "🟡")
    elif bmi < 35.0:
        return ("Obese Class I", "Consult healthcare provider", "🟠")
    elif bmi < 40.0:
        return ("Obese Class II", "Medical supervision recommended", "🔴")
    else:
        return ("Obese Class III", "Immediate medical attention needed", "🔴")


def get_weight_input():
    """Get weight input with unit conversion."""
    print("\nWeight Input:")
    print("  1. Kilograms (kg)")
    print("  2. Pounds (lbs)")
    
    choice = input("Select unit (1 or 2): ").strip()
    
    if choice == "2":
        weight_lbs = float(input("Enter weight in pounds: "))
        weight_kg = weight_lbs * 0.453592
        print(f"  Converted: {weight_kg:.2f} kg")
        return weight_kg
    else:
        return float(input("Enter weight in kilograms: "))


def get_height_input():
    """Get height input with unit conversion."""
    print("\nHeight Input:")
    print("  1. Meters (m)")
    print("  2. Centimeters (cm)")
    print("  3. Feet and Inches")
    
    choice = input("Select unit (1, 2, or 3): ").strip()
    
    if choice == "2":
        height_cm = float(input("Enter height in centimeters: "))
        height_m = height_cm / 100
        print(f"  Converted: {height_m:.2f} m")
        return height_m
    elif choice == "3":
        feet = float(input("Enter feet: "))
        inches = float(input("Enter inches: "))
        total_inches = (feet * 12) + inches
        height_m = total_inches * 0.0254
        print(f"  Converted: {height_m:.2f} m")
        return height_m
    else:
        return float(input("Enter height in meters: "))


def display_bmi_chart():
    """Display BMI reference chart."""
    print("\n" + "=" * 60)
    print("BMI REFERENCE CHART (WHO Standards)")
    print("=" * 60)
    print("BMI Range          | Category               | Status")
    print("-" * 60)
    print("Below 16.0         | Severe Underweight     | 🔴")
    print("16.0 - 18.4        | Underweight            | 🟡")
    print("18.5 - 24.9        | Normal Weight          | 🟢")
    print("25.0 - 29.9        | Overweight             | 🟡")
    print("30.0 - 34.9        | Obese Class I          | 🟠")
    print("35.0 - 39.9        | Obese Class II         | 🔴")
    print("40.0 and above     | Obese Class III        | 🔴")
    print("=" * 60)


def main():
    """Main program execution."""
    print("=" * 60)
    print("                BMI CALCULATOR")
    print("=" * 60)
    print("\nBody Mass Index (BMI) is a measure of body fat based on")
    print("height and weight that applies to adult men and women.")
    
    while True:
        print("\n" + "-" * 60)
        
        try:
            # Get user inputs
            weight_kg = get_weight_input()
            height_m = get_height_input()
            
            # Validate inputs
            if weight_kg <= 0 or height_m <= 0:
                print("\n❌ Error: Weight and height must be positive values.")
                continue
            
            if height_m > 3.0 or weight_kg > 500:
                print("\n❌ Warning: Values seem unrealistic. Please check inputs.")
                continue
            
            # Calculate BMI
            bmi = calculate_bmi(weight_kg, height_m)
            category, description, emoji = get_bmi_category(bmi)
            
            # Display results
            print("\n" + "=" * 60)
            print("YOUR BMI RESULTS")
            print("=" * 60)
            print(f"Weight:       {weight_kg:.2f} kg")
            print(f"Height:       {height_m:.2f} m")
            print(f"\nBMI:          {bmi:.1f}")
            print(f"Category:     {category} {emoji}")
            print(f"Advice:       {description}")
            print("=" * 60)
            
            # Show reference chart
            show_chart = input("\nShow BMI reference chart? (y/n): ")
            if show_chart.lower() == 'y':
                display_bmi_chart()
            
            # Disclaimer
            print("\n⚠️  Note: BMI is a screening tool and does not diagnose")
            print("   health conditions. Consult a healthcare provider for")
            print("   personalized health advice.")
            
        except ValueError:
            print("\n❌ Error: Please enter valid numeric values.")
            continue
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            continue
        
        # Continue or exit
        again = input("\nCalculate another BMI? (Y/n): ")
        if again.lower() == 'n':
            print("\nThank you for using BMI Calculator!")
            print("Stay healthy! 💪")
            break


if __name__ == "__main__":
    main()