import tkinter as tk
from tkinter import messagebox
import csv
import datetime
import matplotlib.pyplot as plt
import os

FILE = "bmi_data.csv"


# ---------- BMI LOGIC ----------
def calculate_bmi(weight, height):
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    return "Obese"


# ---------- DATA STORAGE ----------
def save_record(name, weight, height, bmi):
    file_exists = os.path.isfile(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Date", "Name", "Weight", "Height", "BMI"])

        writer.writerow([
            datetime.date.today(),
            name,
            weight,
            height,
            bmi
        ])


def get_history(name):
    dates = []
    bmis = []

    if not os.path.exists(FILE):
        return dates, bmis

    with open(FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Name"] == name:
                dates.append(row["Date"])
                bmis.append(float(row["BMI"]))

    return dates, bmis


# ---------- GUI ACTIONS ----------
def calculate_clicked():
    try:
        name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        # validation
        if name == "":
            raise ValueError("Name required")

        if not (20 <= weight <= 300):
            raise ValueError("Weight out of range")

        if not (50 <= height <= 250):
            raise ValueError("Height out of range")

        bmi = calculate_bmi(weight, height)
        cat = bmi_category(bmi)

        result_label.config(text=f"BMI: {bmi} ({cat})")

        save_record(name, weight, height, bmi)

    except Exception as e:
        messagebox.showerror("Input Error", str(e))


def show_history():
    name = name_entry.get().strip()
    dates, bmis = get_history(name)

    if not bmis:
        messagebox.showinfo("Info", "No records found.")
        return

    plt.plot(dates, bmis)
    plt.title(f"BMI Trend for {name}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# ---------- GUI LAYOUT ----------
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("300x300")

tk.Label(root, text="Name").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Weight (kg)").pack(pady=5)
weight_entry = tk.Entry(root)
weight_entry.pack()

tk.Label(root, text="Height (cm)").pack(pady=5)
height_entry = tk.Entry(root)
height_entry.pack()

tk.Button(root, text="Calculate & Save",
          command=calculate_clicked).pack(pady=10)

tk.Button(root, text="Show BMI Trend",
          command=show_history).pack()

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()