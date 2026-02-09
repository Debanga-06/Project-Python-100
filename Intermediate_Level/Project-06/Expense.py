import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---------------- DATABASE SETUP ----------------
def create_db():
    conn = sqlite3.connect("expense.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL
        )
    """)
    conn.commit()
    conn.close()

# ---------------- ADD EXPENSE ----------------
def add_expense(date, category, amount):
    conn = sqlite3.connect("expense.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)",
                (date, category, amount))
    conn.commit()
    conn.close()
    print("Expense added successfully!")

# ---------------- LOAD DATA ----------------
def load_data():
    conn = sqlite3.connect("expense.db")
    df = pd.read_sql("SELECT * FROM expenses", conn)
    conn.close()
    return df

# ---------------- ANALYSIS ----------------
def analyze_expense():
    df = load_data()
    if df.empty:
        print("No expense data found.")
        return

    print("\nTotal Expense:", df["amount"].sum())
    print("\nCategory-wise Expense:")
    print(df.groupby("category")["amount"].sum())

# ---------------- VISUALIZATION ----------------
def visualize_expense():
    df = load_data()
    if df.empty:
        print("No data to visualize.")
        return

    category_sum = df.groupby("category")["amount"].sum()

    # Bar Chart
    category_sum.plot(kind="bar", title="Expense by Category", color="orange")
    plt.ylabel("Amount")
    plt.show()

    # Pie Chart
    category_sum.plot(kind="pie", autopct="%1.1f%%", title="Expense Distribution")
    plt.ylabel("")
    plt.show()

# ---------------- MAIN MENU ----------------
def main():
    create_db()

    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. Analyze Expense")
        print("3. Visualize Expense")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD) or press enter for today: ")
            if date == "":
                date = datetime.now().strftime("%Y-%m-%d")
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            add_expense(date, category, amount)

        elif choice == "2":
            analyze_expense()

        elif choice == "3":
            visualize_expense()

        elif choice == "4":
            print("Exiting program...")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
