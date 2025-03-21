# pyinstaller --onefile --windowed --hidden-import=sklearn --hidden-import=joblib --hidden-import=sklearn.ensemble._forest --add-data "../model/random_forest_model.pkl;." --icon=./icon/electricDemandPredictor_icon.ico electricDemandPredictor.py

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

import os
import sys
import joblib
import pandas as pd

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model"))

model_path = os.path.join(base_path, "random_forest_model.pkl")
model = joblib.load(model_path)

def get_quarter(date):
    minutes = date.minute
    if 0 <= minutes <= 14:
        return 0
    elif 15 <= minutes <= 29:
        return 2
    elif 30 <= minutes <= 44:
        return 3
    elif 45 <= minutes <= 59:
        return 4

def get_day_week(date):
    return date.weekday()

def get_season(date):
    month = date.month
    dia = date.day
    if (month == 3 and dia >= 20) or month in [4, 5] or (month == 6 and dia < 21):
        return 0  # Spring
    elif (month == 6 and dia >= 21) or month in [7, 8] or (month == 9 and dia < 23):
        return 1  # Summer
    elif (month == 9 and dia >= 23) or month in [10, 11] or (month == 12 and dia < 21):
        return 2  # Autumn
    else:
        return 3  # Winter

def predict():
    date = datetime.strptime(calendar.get_date(), "%m/%d/%y")
    date = datetime(
        date.year, date.month, date.day,
        int(hour.get()), int(minute.get())
    )

    features = pd.DataFrame([{
        "Day": date.day,
        "Month": date.month,
        "Year": date.year,
        "Hour": date.hour,
        "Quarter": get_quarter(date),
        "Day_week": get_day_week(date),
        "Season": get_season(date),
    }])

    predicted_values = model.predict(features)
    kW = predicted_values[0][0]
    kVAr = predicted_values[0][1]

    kW_value_label.config(text=f"{round(kW, 2)}")
    kVAr_value_label.config(text=f"{round(kVAr, 2)}")

def validate_hour_input(hour):
    if hour == "": return True
    return hour.isdigit() and 0 <= int(hour) < 24

def validate_minute_input(minute):
    if minute == "": return True
    return minute.isdigit() and 0 <= int(minute) < 60

def config_button():
    btn_select.config(state=tk.NORMAL if hour.get() and minute.get() else tk.DISABLED)

# Create main window
root = tk.Tk()
root.title("Electric Demand Predictor")
root.geometry("350x400")

# Date selection with calendar
current_time = datetime.now()
calendar = Calendar(root, selectmode='day', year=current_time.year, month=current_time.month, day=current_time.day)
calendar.pack(pady=20)

# Time selection section (hour and minute)
frame_time = tk.Frame(root)
frame_time.pack()

tk.Label(frame_time, text="Hour:").pack(side=tk.LEFT)

hour_validate = root.register(validate_hour_input)
hour = ttk.Combobox(frame_time, values=[str(i) for i in range(24)], width=3, validate="key",
                    validatecommand=(hour_validate, "%P"))
hour.pack(side=tk.LEFT)
hour.set(current_time.hour)
hour.bind("<<ComboboxSelected>>", lambda event: config_button())
hour.bind("<KeyRelease>", lambda event: config_button())

tk.Label(frame_time, text=":").pack(side=tk.LEFT)

minute_validate = root.register(validate_minute_input)
minute = ttk.Combobox(frame_time, values=[str(i) for i in range(60)], width=3, validate="key",
                      validatecommand=(minute_validate, "%P"))
minute.pack(side=tk.LEFT)
minute.set(current_time.minute)
minute.bind("<<ComboboxSelected>>", lambda event: config_button())
minute.bind("<KeyRelease>", lambda event: config_button())

# Prediction button
btn_select = tk.Button(root, text="Predict (kW) and (kVAr)", command=predict)
btn_select.pack(pady=10)

# Results section
frame_results = tk.Frame(root)
frame_results.pack(pady=10)

tk.Label(frame_results, text="(kW):", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)
kW_value_label = tk.Label(frame_results, text="---", font=("Arial", 10))
kW_value_label.grid(row=0, column=1, sticky="e", padx=5)

tk.Label(frame_results, text="(kVAr):", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5)
kVAr_value_label = tk.Label(frame_results, text="---", font=("Arial", 10))
kVAr_value_label.grid(row=1, column=1, sticky="e", padx=5)

# Run application
root.mainloop()