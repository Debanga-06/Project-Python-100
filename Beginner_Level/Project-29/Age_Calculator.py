"""
Age Calculator Application
Demonstrates: DateTime Module, Date Arithmetic, GUI (tkinter)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar


class AgeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Age Calculator")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # Setup GUI
        self.setup_ui()
        
    def setup_ui(self):
        """Create and configure GUI elements"""
        
        # Title Label
        title_label = tk.Label(
            self.root,
            text="🎂 AGE CALCULATOR",
            font=('Helvetica', 18, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=15)
        
        # Input Frame
        input_frame = tk.LabelFrame(
            self.root,
            text="Enter Birth Date",
            font=('Helvetica', 12, 'bold'),
            bg='#34495e',
            fg='#ecf0f1',
            relief=tk.GROOVE,
            bd=3
        )
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Date Input Fields
        date_entry_frame = tk.Frame(input_frame, bg='#34495e')
        date_entry_frame.pack(pady=15, padx=10)
        
        # Day
        tk.Label(
            date_entry_frame,
            text="Day:",
            font=('Helvetica', 11),
            bg='#34495e',
            fg='#ecf0f1'
        ).grid(row=0, column=0, padx=5, sticky='e')
        
        self.day_var = tk.StringVar()
        self.day_entry = ttk.Combobox(
            date_entry_frame,
            textvariable=self.day_var,
            values=[str(i) for i in range(1, 32)],
            width=8,
            font=('Helvetica', 11),
            state='readonly'
        )
        self.day_entry.grid(row=0, column=1, padx=5)
        self.day_entry.set("1")
        
        # Month
        tk.Label(
            date_entry_frame,
            text="Month:",
            font=('Helvetica', 11),
            bg='#34495e',
            fg='#ecf0f1'
        ).grid(row=0, column=2, padx=5, sticky='e')
        
        self.month_var = tk.StringVar()
        months = [calendar.month_name[i] for i in range(1, 13)]
        self.month_entry = ttk.Combobox(
            date_entry_frame,
            textvariable=self.month_var,
            values=months,
            width=12,
            font=('Helvetica', 11),
            state='readonly'
        )
        self.month_entry.grid(row=0, column=3, padx=5)
        self.month_entry.set("January")
        
        # Year
        tk.Label(
            date_entry_frame,
            text="Year:",
            font=('Helvetica', 11),
            bg='#34495e',
            fg='#ecf0f1'
        ).grid(row=0, column=4, padx=5, sticky='e')
        
        self.year_var = tk.StringVar()
        current_year = datetime.now().year
        years = [str(i) for i in range(current_year, current_year - 120, -1)]
        self.year_entry = ttk.Combobox(
            date_entry_frame,
            textvariable=self.year_var,
            values=years,
            width=10,
            font=('Helvetica', 11),
            state='readonly'
        )
        self.year_entry.grid(row=0, column=5, padx=5)
        self.year_entry.set(str(current_year))
        
        # Calculate Button
        calc_btn = tk.Button(
            input_frame,
            text="CALCULATE AGE",
            command=self.calculate_age,
            font=('Helvetica', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            width=20,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        calc_btn.pack(pady=10)
        
        # Results Frame
        results_frame = tk.LabelFrame(
            self.root,
            text="Age Details",
            font=('Helvetica', 12, 'bold'),
            bg='#34495e',
            fg='#ecf0f1',
            relief=tk.GROOVE,
            bd=3
        )
        results_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Age Display
        self.age_label = tk.Label(
            results_frame,
            text="Your Age: -- Years -- Months -- Days",
            font=('Helvetica', 14, 'bold'),
            bg='#34495e',
            fg='#3498db'
        )
        self.age_label.pack(pady=15)
        
        # Detailed Information
        self.info_text = tk.Text(
            results_frame,
            font=('Courier', 10),
            bg='#2c3e50',
            fg='#ecf0f1',
            height=15,
            width=50,
            relief=tk.FLAT,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.info_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        # Today's Date Button
        today_btn = tk.Button(
            button_frame,
            text="Use Today",
            command=self.use_today,
            font=('Helvetica', 10, 'bold'),
            bg='#3498db',
            fg='white',
            width=12,
            relief=tk.RAISED,
            bd=2,
            cursor='hand2'
        )
        today_btn.grid(row=0, column=0, padx=5)
        
        # Clear Button
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_all,
            font=('Helvetica', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            width=12,
            relief=tk.RAISED,
            bd=2,
            cursor='hand2'
        )
        clear_btn.grid(row=0, column=1, padx=5)
        
    def validate_date(self, day, month, year):
        """Validate the entered date"""
        try:
            month_num = list(calendar.month_name).index(month)
            date_obj = datetime(year, month_num, day)
            
            # Check if date is in the future
            if date_obj > datetime.now():
                messagebox.showerror(
                    "Invalid Date",
                    "Birth date cannot be in the future!"
                )
                return None
            
            return date_obj
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                f"Invalid date: {day} {month} {year}"
            )
            return None
    
    def calculate_age(self):
        """Calculate age and display detailed information"""
        try:
            day = int(self.day_var.get())
            month = self.month_var.get()
            year = int(self.year_var.get())
            
            birth_date = self.validate_date(day, month, year)
            if not birth_date:
                return
            
            current_date = datetime.now()
            
            # Calculate age using relativedelta for accurate months/years
            age = relativedelta(current_date, birth_date)
            
            # Update main age display
            self.age_label.config(
                text=f"Your Age: {age.years} Years {age.months} Months {age.days} Days"
            )
            
            # Calculate additional information
            total_days = (current_date - birth_date).days
            total_hours = total_days * 24
            total_minutes = total_hours * 60
            total_seconds = total_minutes * 60
            
            # Calculate weeks
            total_weeks = total_days // 7
            
            # Next birthday calculation
            next_birthday = datetime(
                current_date.year,
                birth_date.month,
                birth_date.day
            )
            
            if next_birthday < current_date:
                next_birthday = datetime(
                    current_date.year + 1,
                    birth_date.month,
                    birth_date.day
                )
            
            days_to_birthday = (next_birthday - current_date).days
            
            # Day of week born
            day_of_week = birth_date.strftime("%A")
            
            # Zodiac sign
            zodiac = self.get_zodiac_sign(birth_date.month, birth_date.day)
            
            # Build detailed information text
            info = f"""
╔══════════════════════════════════════════════╗
║           DETAILED AGE INFORMATION           ║
╚══════════════════════════════════════════════╝

📅 Birth Date: {birth_date.strftime("%B %d, %Y")}
📆 Current Date: {current_date.strftime("%B %d, %Y")}

🎂 AGE BREAKDOWN:
   • Years: {age.years}
   • Months: {age.months}
   • Days: {age.days}

⏱️ YOU HAVE LIVED:
   • {total_days:,} days
   • {total_weeks:,} weeks
   • {total_hours:,} hours
   • {total_minutes:,} minutes
   • {total_seconds:,} seconds

🎉 NEXT BIRTHDAY:
   • Date: {next_birthday.strftime("%B %d, %Y")}
   • In: {days_to_birthday} days
   • Day: {next_birthday.strftime("%A")}

✨ BIRTH DETAILS:
   • Day of Week: {day_of_week}
   • Zodiac Sign: {zodiac}
   • Season: {self.get_season(birth_date.month)}

📊 MILESTONES:
   • Age in Months: {age.years * 12 + age.months}
   • Days to 100 years: {36500 - total_days:,}
            """
            
            # Update text widget
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info)
            self.info_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def get_zodiac_sign(self, month, day):
        """Determine zodiac sign based on birth date"""
        zodiac_signs = {
            (1, 20): "Capricorn", (2, 19): "Aquarius",
            (3, 21): "Pisces", (4, 20): "Aries",
            (5, 21): "Taurus", (6, 21): "Gemini",
            (7, 23): "Cancer", (8, 23): "Leo",
            (9, 23): "Virgo", (10, 23): "Libra",
            (11, 22): "Scorpio", (12, 22): "Sagittarius"
        }
        
        for (end_month, end_day), sign in zodiac_signs.items():
            if month < end_month or (month == end_month and day <= end_day):
                return sign
        return "Capricorn"
    
    def get_season(self, month):
        """Determine season based on month"""
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"
    
    def use_today(self):
        """Set date inputs to today's date"""
        today = datetime.now()
        self.day_entry.set(str(today.day))
        self.month_entry.set(calendar.month_name[today.month])
        self.year_entry.set(str(today.year))
    
    def clear_all(self):
        """Clear all inputs and results"""
        self.day_entry.set("1")
        self.month_entry.set("January")
        self.year_entry.set(str(datetime.now().year))
        self.age_label.config(text="Your Age: -- Years -- Months -- Days")
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.config(state=tk.DISABLED)
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


def main():
    """Main function to run the age calculator application"""
    root = tk.Tk()
    
    # Check if dateutil is available
    try:
        from dateutil.relativedelta import relativedelta
    except ImportError:
        messagebox.showwarning(
            "Missing Module",
            "This application requires 'python-dateutil' module.\n\n"
            "Install it using:\npip install python-dateutil"
        )
        root.destroy()
        return
    
    calculator = AgeCalculator(root)
    calculator.run()


if __name__ == "__main__":
    main()