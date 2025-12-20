# BMI Calculator 

A professional Python application that calculates Body Mass Index (BMI) with support for multiple unit systems and provides WHO-standard health category classifications.

## Features

- **Multiple Unit Support**
  - Weight: Kilograms or Pounds
  - Height: Meters, Centimeters, or Feet & Inches
  - Automatic unit conversion
- **WHO Standard Categories**: 7 BMI classification levels
- **Visual Indicators**: Color-coded emoji status indicators
- **Reference Chart**: Built-in BMI category reference table
- **Input Validation**: Comprehensive error handling
- **Health Advice**: Category-specific recommendations
- **Professional Output**: Clean, formatted results display

## Requirements

- Python 3.x

## Installation & Usage

```bash
# Save as bmi_calculator.py
python bmi_calculator.py
```

## Quick Start

```
==================================================
                BMI CALCULATOR
==================================================

Weight Input:
  1. Kilograms (kg)
  2. Pounds (lbs)
Select unit (1 or 2): 1
Enter weight in kilograms: 70

Height Input:
  1. Meters (m)
  2. Centimeters (cm)
  3. Feet and Inches
Select unit (1, 2, or 3): 2
Enter height in centimeters: 175
  Converted: 1.75 m

==================================================
YOUR BMI RESULTS
==================================================
Weight:       70.00 kg
Height:       1.75 m

BMI:          22.9
Category:     Normal Weight 🟢
Advice:       Maintain healthy lifestyle
==================================================
```

## BMI Categories (WHO Standards)

| BMI Range | Category | Status | Description |
|-----------|----------|--------|-------------|
| < 16.0 | Severe Underweight | 🔴 | Seek medical attention |
| 16.0 - 18.4 | Underweight | 🟡 | Consider gaining weight |
| 18.5 - 24.9 | Normal Weight | 🟢 | Maintain healthy lifestyle |
| 25.0 - 29.9 | Overweight | 🟡 | Consider losing weight |
| 30.0 - 34.9 | Obese Class I | 🟠 | Consult healthcare provider |
| 35.0 - 39.9 | Obese Class II | 🔴 | Medical supervision recommended |
| ≥ 40.0 | Obese Class III | 🔴 | Immediate medical attention needed |

## BMI Formula

```
BMI = weight (kg) / height² (m²)
```

### Example Calculation
- Weight: 70 kg
- Height: 1.75 m
- BMI = 70 / (1.75 × 1.75) = 22.9

## Unit Conversions

### Weight
- **Pounds to Kilograms**: kg = lbs × 0.453592
- Example: 154 lbs = 70 kg

### Height
- **Centimeters to Meters**: m = cm ÷ 100
- **Feet & Inches to Meters**: m = (feet × 12 + inches) × 0.0254
- Example: 5'9" = 1.75 m

## Code Structure

### Functions

```python
calculate_bmi(weight_kg, height_m)
# Core BMI calculation

get_bmi_category(bmi)
# Returns category, description, and status emoji

get_weight_input()
# Handles weight input with unit conversion

get_height_input()
# Handles height input with unit conversion

display_bmi_chart()
# Shows complete BMI reference table

main()
# Main program loop with error handling
```

## Health Considerations

### BMI Limitations
- **Does not measure body fat directly**
- May not be accurate for:
  - Athletes with high muscle mass
  - Pregnant women
  - Elderly individuals
  - Children and adolescents
  - Different ethnic groups

### When BMI is Useful
- Population health screening
- Tracking weight changes over time
- Initial health risk assessment
- General fitness monitoring

### Additional Health Metrics
Consider measuring:
- Waist circumference
- Body fat percentage
- Muscle mass
- Waist-to-hip ratio
- Blood pressure
- Cholesterol levels

## Sample Results

### Underweight Example
```
Weight: 50 kg
Height: 1.70 m
BMI: 17.3
Category: Underweight 🟡
```

### Normal Weight Example
```
Weight: 70 kg
Height: 1.75 m
BMI: 22.9
Category: Normal Weight 🟢
```

### Overweight Example
```
Weight: 85 kg
Height: 1.75 m
BMI: 27.8
Category: Overweight 🟡
```

## Error Handling

- **Negative values**: Rejected with error message
- **Unrealistic values**: Warning for height > 3m or weight > 500kg
- **Invalid input**: Type error handling with retry option
- **Division by zero**: Prevented by input validation

## Use Cases

- Personal health tracking
- Fitness program monitoring
- Medical screening tool
- Health education
- Nutrition counseling
- Research data collection

## Best Practices

1. **Measure consistently**: Same time of day, same conditions
2. **Use accurate measurements**: Digital scales and measuring tape
3. **Track trends**: Monitor changes over weeks/months
4. **Consult professionals**: Discuss results with healthcare provider
5. **Combine with other metrics**: Don't rely on BMI alone

## Disclaimer

⚠️ **Medical Advice**: This calculator is for informational purposes only. BMI is a screening tool and does not diagnose health conditions. Always consult with a qualified healthcare provider for personalized medical advice, diagnosis, or treatment.

## License

Free to use and modify for educational and personal purposes.