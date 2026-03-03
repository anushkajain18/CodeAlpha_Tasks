# ==========================================================
# MODERN STOCK PORTFOLIO MANAGEMENT SYSTEM
# Professional GUI + SQLite + Charts + CSV
# ==========================================================

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import csv
import matplotlib.pyplot as plt

# -------------------------
# Database Setup
# -------------------------
conn = sqlite3.connect("portfolio.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    quantity INTEGER,
    price REAL
)
""")
conn.commit()

# -------------------------
# Stock Prices
# -------------------------
stock_prices = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOG": 2800,
    "MSFT": 320,
    "AMZN": 3400
}

# -------------------------
# Functions
# -------------------------

def add_stock():
    symbol = symbol_entry.get().upper()
    qty = quantity_entry.get()

    if symbol not in stock_prices:
        messagebox.showerror("Error", "Stock not available!")
        return

    try:
        qty = int(qty)
        price = stock_prices[symbol]

        cursor.execute(
            "INSERT INTO portfolio (symbol, quantity, price) VALUES (?, ?, ?)",
            (symbol, qty, price)
        )
        conn.commit()

        symbol_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)

        refresh_data()

    except:
        messagebox.showerror("Error", "Enter valid quantity!")

def refresh_data():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM portfolio")
    rows = cursor.fetchall()

    total = 0

    for row in rows:
        id, symbol, qty, price = row
        investment = qty * price
        total += investment
        tree.insert("", "end", values=(id, symbol, qty, price, investment))

    total_label.config(text=f"Total Investment: ${total}")

def delete_stock():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select record to delete!")
        return

    values = tree.item(selected, "values")
    record_id = values[0]

    cursor.execute("DELETE FROM portfolio WHERE id=?", (record_id,))
    conn.commit()
    refresh_data()

def export_csv():
    cursor.execute("SELECT * FROM portfolio")
    rows = cursor.fetchall()

    with open("portfolio_export.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Symbol", "Quantity", "Price"])
        writer.writerows(rows)

    messagebox.showinfo("Success", "Exported Successfully!")

def show_chart():
    cursor.execute("SELECT symbol, quantity, price FROM portfolio")
    data = cursor.fetchall()

    labels = []
    values = []

    for sym, qty, price in data:
        labels.append(sym)
        values.append(qty * price)

    if not values:
        messagebox.showinfo("Info", "No data available!")
        return

    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Investment Distribution")
    plt.show()

# -------------------------
# GUI Setup
# -------------------------

root = tk.Tk()
root.title("📊 Modern Stock Portfolio System")
root.geometry("1000x650")
root.configure(bg="#1e1e2f")

style = ttk.Style()
style.theme_use("clam")

# Treeview Style
style.configure("Treeview",
                background="#2e2e3e",
                foreground="white",
                rowheight=25,
                fieldbackground="#2e2e3e")
style.map('Treeview', background=[('selected', '#4a90e2')])

# Title
title = tk.Label(root,
                 text="📈 Stock Portfolio Dashboard",
                 font=("Segoe UI", 24, "bold"),
                 bg="#1e1e2f",
                 fg="#4a90e2")
title.pack(pady=15)

# Input Frame
input_frame = tk.Frame(root, bg="#2a2a40", bd=2, relief="ridge")
input_frame.pack(pady=10, padx=20, fill="x")

tk.Label(input_frame, text="Stock Symbol:", bg="#2a2a40", fg="white").grid(row=0, column=0, padx=10, pady=10)
symbol_entry = tk.Entry(input_frame, font=("Segoe UI", 11))
symbol_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Quantity:", bg="#2a2a40", fg="white").grid(row=0, column=2, padx=10)
quantity_entry = tk.Entry(input_frame, font=("Segoe UI", 11))
quantity_entry.grid(row=0, column=3)

tk.Button(input_frame, text="Add Stock", bg="#4a90e2", fg="white",
          command=add_stock, width=12).grid(row=0, column=4, padx=10)

# Table Frame
table_frame = tk.Frame(root, bg="#1e1e2f")
table_frame.pack(pady=10)

columns = ("ID", "Symbol", "Quantity", "Price", "Total")

tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")

tree.pack()

# Bottom Buttons
button_frame = tk.Frame(root, bg="#1e1e2f")
button_frame.pack(pady=15)

tk.Button(button_frame, text="Delete Selected", bg="#e74c3c", fg="white",
          command=delete_stock, width=15).grid(row=0, column=0, padx=10)

tk.Button(button_frame, text="Export CSV", bg="#27ae60", fg="white",
          command=export_csv, width=15).grid(row=0, column=1, padx=10)

tk.Button(button_frame, text="Show Chart", bg="#f39c12", fg="white",
          command=show_chart, width=15).grid(row=0, column=2, padx=10)

tk.Button(button_frame, text="Refresh", bg="#9b59b6", fg="white",
          command=refresh_data, width=15).grid(row=0, column=3, padx=10)

# Total Label
total_label = tk.Label(root,
                       text="Total Investment: $0",
                       font=("Segoe UI", 16, "bold"),
                       bg="#1e1e2f",
                       fg="#ffffff")
total_label.pack(pady=10)

refresh_data()

root.mainloop()
conn.close()
