# 📊 Expense Tracker System

A Python-based application to **record, analyze, and visualize daily expenses**.
This system helps users **track their spending habits**, understand **category-wise expenditure**, and make **better financial decisions**.

---

## 🎯 Aim of the Project

To develop a system that allows users to **store expense data**, **analyze patterns**, and **visualize spending** using graphs to help manage finances effectively.

---

## 📝 Objectives

* Record daily expenses with **date, category, and amount**.
* Store expense data in a **persistent database** (SQLite).
* Analyze total and category-wise expenses using **Pandas**.
* Visualize expense patterns using **Matplotlib** (bar & pie charts).
* Provide a **simple and user-friendly interface** for everyday use.

---

## ✨ Features

* Add, view, and analyze expenses.
* Category-wise expense summary.
* Graphical visualization (bar chart & pie chart).
* Automatic storage in SQLite database.
* Command-line interface for easy interaction.

---

## ⚙️ Requirements

* Python 3.8+
* Libraries:

  * `pandas`
  * `matplotlib`
  * `sqlite3` (built-in)

Install dependencies:

```bash
pip install pandas matplotlib
```

---

## 📂 Project Structure

```
ExpenseTracker/
│── expense.py       # Main Python program
│── README.md        # Project documentation

## 🚀 How to Run

1. Make sure all dependencies are installed.
2. Run the program:

```bash
python expense.py
```

3. Follow the menu options:

   * Add Expense
   * Analyze Expense
   * Visualize Expense
   * Exit

---

## 🧩 Code Overview

* **create_db()** → Initializes SQLite database and table.
* **add_expense(date, category, amount)** → Adds a new expense record.
* **load_data()** → Loads data into Pandas DataFrame.
* **analyze_expense()** → Prints total and category-wise expenses.
* **visualize_expense()** → Displays bar and pie charts for expense analysis.
* **main()** → Command-line menu for user interaction.

---

## 🧾 Database Structure

**Table:** `expenses`

| Column   | Type    | Description             |
| -------- | ------- | ----------------------- |
| id       | INTEGER | Primary key             |
| date     | TEXT    | Date of the expense     |
| category | TEXT    | Category of the expense |
| amount   | REAL    | Amount spent            |

---

## 🖥️ Sample Output

```
--- Expense Tracker ---
1. Add Expense
2. Analyze Expense
3. Visualize Expense
4. Exit

Enter choice: 1
Enter date (YYYY-MM-DD) or press enter for today: 2026-02-09
Enter category: Food
Enter amount: 500
Expense added successfully!

Enter choice: 2
Total Expenses: 500
Category-wise Expenses:
Food    500

Enter choice: 3
# Bar chart and pie chart appear
```

---

## 🔮 Future Enhancements

* Add **monthly and yearly reports**.
* Set **budget limits and alerts**.
* Export data to **CSV or Excel**.
* Add **GUI or web-based interface**.
* Include **search and filter functionality** for expenses.

---

## 👤 Developer

**Name:** Jiban Maji
**GitHub:** [https://github.com/Jiban0507](https://github.com/Jiban0507)