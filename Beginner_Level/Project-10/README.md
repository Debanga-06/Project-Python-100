# Unit Converter

A Python program that converts between various units of measurement including distance, temperature, weight, length, and volume.

## Features

Convert between 10 different unit pairs:

### Distance
- Kilometers ↔ Miles

### Temperature
- Celsius ↔ Fahrenheit

### Weight
- Kilograms ↔ Pounds

### Length
- Centimeters ↔ Inches

### Volume
- Liters ↔ Gallons (US)

## Requirements

- Python 3.x

## How to Run

1. Save the program as `unit_converter.py`
2. Open your terminal or command prompt
3. Navigate to the directory containing the file
4. Run the program:

```bash
python unit_converter.py
```

## Usage

```
==================================================
           UNIT CONVERTER
==================================================

--------------------------------------------------
Select conversion type:
--------------------------------------------------
  1. Kilometers to Miles
  2. Miles to Kilometers
  3. Celsius to Fahrenheit
  4. Fahrenheit to Celsius
  5. Kilograms to Pounds
  6. Pounds to Kilograms
  7. Centimeters to Inches
  8. Inches to Centimeters
  9. Liters to Gallons
  10. Gallons to Liters
  q. Quit
--------------------------------------------------

Your choice: 1

Enter value in km: 100

==================================================
  100.0 km = 62.14 miles
==================================================
```

## Conversion Formulas

- **km to miles**: miles = km × 0.621371
- **miles to km**: km = miles × 1.60934
- **°C to °F**: °F = (°C × 9/5) + 32
- **°F to °C**: °C = (°F - 32) × 5/9
- **kg to lbs**: lbs = kg × 2.20462
- **lbs to kg**: kg = lbs × 0.453592
- **cm to inches**: inches = cm × 0.393701
- **inches to cm**: cm = inches × 2.54
- **L to gallons**: gallons = L × 0.264172
- **gallons to L**: L = gallons × 3.78541

## Common Conversions

### Distance
- 1 km = 0.62 miles
- 1 mile = 1.61 km

### Temperature
- 0°C = 32°F (freezing point)
- 100°C = 212°F (boiling point)
- 37°C = 98.6°F (body temperature)

### Weight
- 1 kg = 2.20 lbs
- 1 lb = 0.45 kg

### Length
- 1 inch = 2.54 cm
- 1 foot (12 inches) = 30.48 cm

### Volume
- 1 liter = 0.26 gallons
- 1 gallon = 3.79 liters

## Code Structure

- Individual conversion functions for each unit pair
- `main()` - Menu-driven interface with user input handling
- Results displayed with 2 decimal precision

## Use Cases

- Travel planning (distance and temperature)
- Cooking and baking (volume conversions)
- Fitness tracking (weight conversions)
- International measurements
- Educational purposes

## License

Free to use and modify.