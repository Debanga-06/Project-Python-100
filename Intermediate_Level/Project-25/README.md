# 💰 Budget Planner (Python)

## 📌 Overview
**Budget Planner** is a Python-based application designed to help users **track income and expenses**, **analyze spending habits**, **visualize data**, and **generate financial reports**.  

This project is beginner-friendly but also scalable for more advanced features like predictive budgeting, multi-user support, and interactive dashboards.

---

## ✨ Features
- **Income & Expense Tracking** → Add, edit, and delete entries.  
- **Category-Based Analysis** → Food, Rent, Transport, Utilities, Entertainment, etc.  
- **Visualization** → Pie charts for expense distribution by category.  
- **Reports** → Export data to Excel for record keeping.  
- **Data Persistence** → All data stored in `data/budget.csv`.  
- **Error Handling** → Prevents invalid inputs (missing date, non-numeric amount).  
- **GUI Interface** → Built with Tkinter for easy interaction.  

---

## 💻 Supported Platforms
- **Windows** (10, 11)  
- **Linux** (Ubuntu, Fedora)  
- **macOS** (Catalina, Big Sur)  

> Requires **Python 3.x** and standard libraries. Works anywhere Tkinter and pandas are supported.

---

## 📦 Requirements
Python libraries required (can install via `requirements.txt`):

```text
pandas
matplotlib
seaborn
openpyxl
reportlab
````

**Install dependencies:**

```bash
pip install -r requirements.txt
```

> Note: Tkinter comes pre-installed with Python 3, no separate installation required.

---

## 🗂️ Project Structure

```text
📁 Budget-Planner
 ┣ 📄 README.md                  # Project documentation
 ┣ 📄 budget_planner.py          # Main Python script
 ┣ 📄 requirements.txt           # Dependencies
 ┣ 📁 data                       # CSV files for budget data
 ┗ 📁 assets                     # Optional: icons, charts
```

---

## 📝 Data Structure

**CSV File:** `data/budget.csv`

| Date       | Category  | Type    | Amount | Notes        |
| ---------- | --------- | ------- | ------ | ------------ |
| 2026-03-01 | Food      | Expense | 250    | Lunch        |
| 2026-03-02 | Salary    | Income  | 3000   | March Salary |
| 2026-03-03 | Transport | Expense | 50     | Taxi         |

* **Type:** Income / Expense
* **Category:** Expense category (Food, Rent, etc.)
* **Amount:** Numeric value
* **Notes:** Optional description

> All new entries are automatically saved to this CSV.

---

## ▶️ Usage

1. **Run the project**:

```bash
python budget_planner.py
```

2. **Add Entry**:

   * Fill **Date** (YYYY-MM-DD), **Category**, **Type**, **Amount**, and **Notes**.
   * Press **Add Entry** → Data will be saved and displayed in the table.

3. **View Table**:

   * Displays all existing entries. Scroll to see full data.

4. **Plot Expenses**:

   * Press **Plot Expenses** → Pie chart shows expense distribution by category.

5. **Export Report**:

   * Press **Export Report** → Save data as **Excel file** for backup or sharing.

---

## 📊 Visualization

* **Pie Chart** → Expense distribution by category
* **Bar Chart / Line Chart (Future)** → Monthly income vs expenses trends
* Charts are generated using **matplotlib** and embedded into Tkinter GUI

---

## 💾 Report Export

* Exported to **Excel (.xlsx)** using `pandas.to_excel()`
* Saves all data including date, type, category, amount, and notes
* File location selectable via **Save As dialog**

---

## 🚀 Future Improvements

* Add **monthly/yearly summaries** with graphs
* Generate **PDF reports** with charts and tables
* **Budget forecasting** → Predict next month expenses
* Add **recurring expenses/income** → Auto-add monthly bills
* **Alerts / Notifications** → Warn if budget exceeded
* Multi-user support → Personal accounts
* Web interface using **Streamlit** or **Dash**
* Export charts as images for presentations

---

## 👨‍💻 Author

Developed by **Jiban Maji**
📍 Brainware University, Barasat, West Bengal, India

GitHub Profile: [https://github.com/Jiban0507](https://github.com/Jiban0507)

---

## 📝 Notes

* Ensure **data/** folder exists (auto-created if missing).
* Tkinter GUI requires Python 3.x.
* All data stored locally in CSV; no internet required.
* Pie charts are interactive and dynamically update with new entries.
