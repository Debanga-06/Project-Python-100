import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from datetime import datetime

# Data file
DATA_FILE = "data/budget.csv"

# Ensure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

# Ensure CSV exists
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Type", "Amount", "Notes"])
    df.to_csv(DATA_FILE, index=False)

# Main window
root = tk.Tk()
root.title("Budget Planner")
root.geometry("800x600")

# Load data
def load_data():
    return pd.read_csv(DATA_FILE)

# Save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Add entry
def add_entry():
    date = date_entry.get()
    category = category_entry.get()
    type_ = type_var.get()
    amount = amount_entry.get()
    notes = notes_entry.get()
    
    if not date or not category or not amount:
        messagebox.showwarning("Input Error", "Date, Category, and Amount are required")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number")
        return
    
    df = load_data()
    df = pd.concat([df, pd.DataFrame({
        "Date": [date],
        "Category": [category],
        "Type": [type_],
        "Amount": [amount],
        "Notes": [notes]
    })], ignore_index=True)
    
    save_data(df)
    messagebox.showinfo("Success", "Entry added successfully")
    clear_entries()
    refresh_table()

# Clear entry fields
def clear_entries():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    notes_entry.delete(0, tk.END)

# Refresh table
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    df = load_data()
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

# Plot expenses by category
def plot_expenses():
    df = load_data()
    expenses = df[df["Type"]=="Expense"].groupby("Category")["Amount"].sum()
    if expenses.empty:
        messagebox.showinfo("No Data", "No expense data to plot")
        return
    fig, ax = plt.subplots(figsize=(6,4))
    expenses.plot(kind="pie", autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
    ax.set_title("Expense by Category")
    
    # Display in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(pady=10)
    canvas.draw()

# Export report
def export_report():
    df = load_data()
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Exported", f"Report exported to {file_path}")

# ----- GUI Elements -----
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=2)
date_entry = tk.Entry(input_frame)
date_entry.grid(row=0, column=1, padx=5, pady=2)

tk.Label(input_frame, text="Category:").grid(row=1, column=0, padx=5, pady=2)
category_entry = tk.Entry(input_frame)
category_entry.grid(row=1, column=1, padx=5, pady=2)

tk.Label(input_frame, text="Type:").grid(row=2, column=0, padx=5, pady=2)
type_var = tk.StringVar()
type_combo = ttk.Combobox(input_frame, textvariable=type_var, values=["Income", "Expense"])
type_combo.grid(row=2, column=1, padx=5, pady=2)
type_combo.current(1)

tk.Label(input_frame, text="Amount:").grid(row=3, column=0, padx=5, pady=2)
amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=3, column=1, padx=5, pady=2)

tk.Label(input_frame, text="Notes:").grid(row=4, column=0, padx=5, pady=2)
notes_entry = tk.Entry(input_frame)
notes_entry.grid(row=4, column=1, padx=5, pady=2)

add_btn = tk.Button(input_frame, text="Add Entry", command=add_entry)
add_btn.grid(row=5, column=0, columnspan=2, pady=5)

# Table
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)
columns = ["Date", "Category", "Type", "Amount", "Notes"]
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(side=tk.LEFT)

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)

# Plot & Export Buttons
action_frame = tk.Frame(root)
action_frame.pack(pady=10)

plot_btn = tk.Button(action_frame, text="Plot Expenses", command=plot_expenses)
plot_btn.grid(row=0, column=0, padx=10)

export_btn = tk.Button(action_frame, text="Export Report", command=export_report)
export_btn.grid(row=0, column=1, padx=10)

# Initial table load
refresh_table()

root.mainloop()