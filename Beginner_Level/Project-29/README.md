# Age Calculator 🎂   ![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=yellow)

A comprehensive age calculator application built with Python's tkinter GUI library. This project demonstrates DateTime module usage, date arithmetic, and advanced GUI programming concepts.

## 📋 Features

### Core Functionality
- 📅 **Precise Age Calculation**: Calculate exact age in years, months, and days
- 🎯 **Multiple Time Units**: View age in days, weeks, hours, minutes, and seconds
- 🎉 **Next Birthday Countdown**: See how many days until your next birthday
- ⭐ **Zodiac Sign**: Automatically determine your zodiac sign
- 🌸 **Birth Season**: Identify which season you were born in
- 📊 **Milestone Tracking**: Days until reaching 100 years old
- ✨ **Birth Day Details**: Find out which day of the week you were born

### User Interface
- Clean and modern dark theme design
- Dropdown menus for easy date selection
- Real-time validation of dates
- Comprehensive information display
- User-friendly error messages
- Quick action buttons (Use Today, Clear)

### Advanced Calculations
- Accurate month/year calculations accounting for varying month lengths
- Leap year handling
- Future date validation
- Season determination
- Zodiac sign calculation

## 🎓 Learning Objectives

This project demonstrates:

1. **DateTime Module**:
   - `datetime.datetime()` - Creating date objects
   - `datetime.now()` - Getting current date/time
   - `strftime()` - Formatting dates
   - Date comparison and validation
   - Working with timezones (basic)

2. **Date Arithmetic**:
   - `relativedelta` - Accurate date differences
   - `timedelta` - Time span calculations
   - Days, weeks, months, years calculations
   - Birthday and milestone calculations
   - Handling leap years and varying month lengths

3. **Additional Modules**:
   - `calendar` - Month names and day calculations
   - `dateutil` - Advanced date manipulation

4. **GUI Programming**:
   - Combobox widgets for dropdown menus
   - Text widget for multi-line display
   - LabelFrame for organized sections
   - State management (NORMAL/DISABLED)
   - Input validation and error handling

5. **Control Flow**:
   - Try-except error handling
   - Conditional logic for validation
   - Dictionary lookups for zodiac signs
   - Date range validations

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- tkinter (usually included with Python)
- python-dateutil (external package)

### Install Required Packages

```bash
pip install python-dateutil
```

### Verify Installation

```bash
python -c "from dateutil.relativedelta import relativedelta; print('Success!')"
```

## 💻 Usage

### Running the Age Calculator

```bash
python age_calculator.py
```

### Using the Application

1. **Select Birth Date**:
   - Choose Day from dropdown (1-31)
   - Choose Month from dropdown (January-December)
   - Choose Year from dropdown (current year to 120 years ago)

2. **Calculate Age**:
   - Click the "CALCULATE AGE" button
   - View your detailed age information

3. **Quick Actions**:
   - Click "Use Today" to set current date
   - Click "Clear" to reset all fields

### Understanding the Results

The application displays:

```
🎂 AGE BREAKDOWN:
   • Years: 25
   • Months: 6
   • Days: 15

⏱️ YOU HAVE LIVED:
   • 9,328 days
   • 1,332 weeks
   • 223,872 hours
   • 13,432,320 minutes
   • 805,939,200 seconds

🎉 NEXT BIRTHDAY:
   • Date: June 15, 2025
   • In: 165 days
   • Day: Sunday

✨ BIRTH DETAILS:
   • Day of Week: Wednesday
   • Zodiac Sign: Gemini
   • Season: Summer
```

## 📸 Application Layout

```
┌──────────────────────────────────────────┐
│         🎂 AGE CALCULATOR                │
├──────────────────────────────────────────┤
│  ┌─ Enter Birth Date ─────────────────┐  │
│  │                                     │  │
│  │  Day: [15▼] Month: [June▼]        │  │
│  │  Year: [1998▼]                     │  │
│  │                                     │  │
│  │      [CALCULATE AGE]                │  │
│  └─────────────────────────────────────┘  │
│                                           │
│  ┌─ Age Details ──────────────────────┐  │
│  │ Your Age: 25 Years 6 Months 15 Days│  │
│  │                                     │  │
│  │ ╔════════════════════════════════╗ │  │
│  │ ║  DETAILED AGE INFORMATION      ║ │  │
│  │ ╚════════════════════════════════╝ │  │
│  │ 📅 Birth Date: June 15, 1998      │  │
│  │ ...                                │  │
│  └─────────────────────────────────────┘  │
│                                           │
│     [Use Today]        [Clear]            │
└──────────────────────────────────────────┘
```

## 🔧 Code Structure

### Main Components

```python
class AgeCalculator:
    def __init__(self, root)              # Initialize GUI
    def setup_ui(self)                    # Create all widgets
    def validate_date(self, d, m, y)      # Validate date input
    def calculate_age(self)               # Calculate and display age
    def get_zodiac_sign(self, m, d)       # Determine zodiac sign
    def get_season(self, month)           # Determine birth season
    def use_today(self)                   # Set today's date
    def clear_all(self)                   # Clear all fields
    def run(self)                         # Start main loop
```

### Key DateTime Operations

```python
# Create date object
birth_date = datetime(year, month, day)

# Get current date
current_date = datetime.now()

# Calculate age (accurate with varying month lengths)
from dateutil.relativedelta import relativedelta
age = relativedelta(current_date, birth_date)

# Access components
years = age.years
months = age.months
days = age.days

# Calculate total days
total_days = (current_date - birth_date).days

# Format date for display
formatted = birth_date.strftime("%B %d, %Y")  # June 15, 1998

# Find day of week
day_name = birth_date.strftime("%A")  # Wednesday
```

## 🎨 Customization

### Change Color Theme

Modify colors in `setup_ui()`:

```python
# Light theme
bg_main = '#ecf0f1'      # Light grey
bg_frame = '#ffffff'     # White
text_color = '#2c3e50'   # Dark grey
accent = '#3498db'       # Blue
```

### Add More Information

Add to the `calculate_age()` method:

```python
# Chinese Zodiac
chinese_zodiac = self.get_chinese_zodiac(year)

# Birth month flower
birth_flower = self.get_birth_flower(month)

# Famous people born on same day
famous_people = self.get_famous_birthdays(month, day)
```

### Modify Date Range

In `setup_ui()`:

```python
# Extend year range to 150 years
years = [str(i) for i in range(current_year, current_year - 150, -1)]
```

## 📚 Advanced Features to Add

Here are ideas to extend the project:

1. **Age Comparison**:
   - Compare two people's ages
   - Calculate age difference
   - Find who's older/younger

2. **Historical Events**:
   - Show major events from birth year
   - Display historical context
   - World population at birth time

3. **Export Features**:
   - Save results to PDF
   - Export to text file
   - Share via email

4. **Additional Calculations**:
   - Chinese zodiac
   - Birthstone information
   - Birth month flower
   - Numerology calculations
   - Bio-rhythm charts

5. **Life Expectancy**:
   - Average life expectancy by country
   - Percentage of life lived
   - Estimated remaining days

6. **Multiple Profiles**:
   - Save favorite birth dates
   - Family member profiles
   - Quick access to saved dates

## 🐛 Troubleshooting

### Missing python-dateutil Module

**Error:** `ModuleNotFoundError: No module named 'dateutil'`

**Solution:**
```bash
pip install python-dateutil
```

### Invalid Date Error

**Issue:** Error when calculating age

**Solutions:**
- Ensure day is valid for selected month (e.g., no Feb 30)
- Check that year is not in the future
- Verify all dropdowns have values selected

### Future Date Warning

**Issue:** "Birth date cannot be in the future" message

**Solution:**
- Check that selected date is not after today
- Verify year is correct
- Use "Use Today" button for current date

### Unicode Display Issues

**Issue:** Emojis or special characters not displaying

**Solution:**
- Ensure your terminal/console supports UTF-8
- Update Python to version 3.6+
- On Windows, use Windows Terminal instead of CMD

## 📖 Learning Resources

### Python DateTime Module
- [Official datetime documentation](https://docs.python.org/3/library/datetime.html)
- [Real Python: datetime guide](https://realpython.com/python-datetime/)
- Understanding timezones and UTC

### Date Arithmetic
- [python-dateutil documentation](https://dateutil.readthedocs.io/)
- Handling relative time deltas
- Working with complex date calculations

### Calendar Module
- [Python calendar module](https://docs.python.org/3/library/calendar.html)
- Month and day name operations
- Leap year calculations

## 📝 Project Files

```
age-calculator-project/
├── age_calculator.py      # Main application file
├── README.md             # This file
└── requirements.txt      # python-dateutil
```

### requirements.txt

```txt
python-dateutil>=2.8.0
```

## 🎯 Date Arithmetic Examples

### Basic Operations

```python
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Add/subtract days
tomorrow = datetime.now() + timedelta(days=1)
yesterday = datetime.now() - timedelta(days=1)

# Add/subtract months (accurate)
next_month = datetime.now() + relativedelta(months=1)
last_year = datetime.now() - relativedelta(years=1)

# Calculate age
birth = datetime(1998, 6, 15)
today = datetime.now()
age = relativedelta(today, birth)
print(f"Age: {age.years} years, {age.months} months")

# Find next birthday
next_bday = datetime(today.year, birth.month, birth.day)
if next_bday < today:
    next_bday = datetime(today.year + 1, birth.month, birth.day)
days_until = (next_bday - today).days
```

### Why relativedelta vs timedelta?

**timedelta** limitations:
```python
# Only supports days, seconds, microseconds
delta = timedelta(days=30)  # Not accurate for months

# 30 days ≠ 1 month (months have 28-31 days)
```

**relativedelta** advantages:
```python
# Accurate month/year calculations
delta = relativedelta(months=1)  # Always 1 month

# Handles varying month lengths
# Accounts for leap years automatically
```

## 💡 Tips for Beginners

1. **Understanding DateTime Objects**: Practice creating and manipulating date objects
2. **Date Validation**: Always validate user input for dates
3. **Format Strings**: Learn `strftime()` format codes
4. **Error Handling**: Use try-except for date operations
5. **Testing Edge Cases**: Test with leap years, month boundaries

## 🎯 Practice Challenges

1. Add a date difference calculator (days between two dates)
2. Implement a "Days Until" feature for future events
3. Create a birthday reminder system
4. Add age in dog years/cat years
5. Calculate zodiac compatibility
6. Show famous people born on the same day
7. Add a date formatter tool
8. Create an age prediction for future dates

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional zodiac systems (Chinese, Celtic, etc.)
- Localization/internationalization
- More detailed life statistics
- Historical event integration
- Unit tests

## 📄 License

This project is open source and available for educational purposes.

## 🌟 Acknowledgments

- Uses `python-dateutil` for accurate date calculations
- Inspired by online age calculators
- Built for learning Python date/time operations

---

**Happy Calculating! 🎂✨**

Made with ❤️ for learning Python DateTime programming