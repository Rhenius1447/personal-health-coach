import tkinter as tk
from tkinter import messagebox
import json
import os
import random

DATA_FILE = "health_data.json"

def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_bmr(weight, height, age, gender):
    if gender.lower() == "male":
        return 10*weight + 6.25*height - 5*age + 5
    else:
        return 10*weight + 6.25*height - 5*age - 161

def health_score(bmi, water, exercise):
    score = 50
    if 18.5 <= bmi < 25:
        score += 20
    if water >= 2:
        score += 15
    if exercise >= 3:
        score += 15
    return min(score, 100)

def health_tip():
    tips = [
        "Drink at least 2-3 liters of water daily.",
        "Exercise 30 minutes every day.",
        "Sleep 7-8 hours.",
        "Eat more fruits and vegetables.",
        "Stay consistent!"
    ]
    return random.choice(tips)


def generate_report():
    try:
        name = name_entry.get()
        age = int(age_entry.get())
        gender = gender_var.get()
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())
        height = height_cm / 100
        water = float(water_entry.get())
        exercise = int(exercise_entry.get())

        bmi = calculate_bmi(weight, height)
        category = bmi_category(bmi)
        bmr = calculate_bmr(weight, height_cm, age, gender)
        calories = round(bmr * 1.55, 2)
        score = health_score(bmi, water, exercise)

        result_text.set(
            f"Name: {name}\n"
            f"BMI: {bmi} ({category})\n"
            f"Daily Calories: {calories} kcal\n"
            f"Health Score: {score}/100\n"
            f"Tip: {health_tip()}"
        )

        data = {
            "Name": name,
            "BMI": bmi,
            "Category": category,
            "Calories": calories,
            "Health Score": score
        }

        with open(DATA_FILE, "w") as f:
            json.dump(data, f)

    except:
        messagebox.showerror("Error", "Please enter valid details!")


root = tk.Tk()
root.title("Personal Health Coach")
root.geometry("400x600")
root.resizable(False, False)

title = tk.Label(root, text="Personal Health Coach", font=("Arial", 16, "bold"))
title.pack(pady=10)

# Inputs
name_entry = tk.Entry(root)
age_entry = tk.Entry(root)
weight_entry = tk.Entry(root)
height_entry = tk.Entry(root)
water_entry = tk.Entry(root)
exercise_entry = tk.Entry(root)

gender_var = tk.StringVar(value="male")

labels = [
    ("Name", name_entry),
    ("Age", age_entry),
    ("Weight (kg)", weight_entry),
    ("Height (cm)", height_entry),
    ("Water Intake (liters)", water_entry),
    ("Exercise Days/Week", exercise_entry)
]

for text, entry in labels:
    tk.Label(root, text=text).pack()
    entry.pack(pady=5)

tk.Label(root, text="Gender").pack()
tk.Radiobutton(root, text="Male", variable=gender_var, value="male").pack()
tk.Radiobutton(root, text="Female", variable=gender_var, value="female").pack()

tk.Button(root, text="Generate Health Report", command=generate_report, bg="green", fg="white").pack(pady=15)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left", wraplength=350)
result_label.pack(pady=10)

root.mainloop()
