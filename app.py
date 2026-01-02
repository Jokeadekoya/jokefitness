import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Fitness Tracker", layout="centered")

# Load data
try:
    df = pd.read_csv("data.csv", parse_dates=["date"])
except:
    df = pd.DataFrame(columns=["date", "workout_done", "calories"])

today = pd.to_datetime(date.today())

st.title("🏋️ Personal Fitness Tracker")

# ---------------- DAILY INPUT ----------------
st.header("Today")

workout_done = st.checkbox("Workout completed today")
calories = st.number_input("Calories eaten today", min_value=0, step=50)

if st.button("Save today"):
    df = df[df["date"] != today]
    new_row = pd.DataFrame(
        [[today, workout_done, calories]],
        columns=["date", "workout_done", "calories"]
    )
    df = pd.concat([df, new_row])
    df.to_csv("data.csv", index=False)
    st.success("Saved ✔")

# ---------------- WEEKLY SUMMARY ----------------
st.header("This Week")

df["week"] = df["date"].dt.isocalendar().week
current_week = today.isocalendar().week

week_df = df[df["week"] == current_week]

workouts_done = week_df["workout_done"].sum()
total_calories = week_df["calories"].sum()

# Weekly goals (editable)
target_workouts = st.number_input("Weekly workout goal", value=4)
max_calories = st.number_input("Weekly calorie limit", value=12000)

# Score calculation
workout_score = min(workouts_done / target_workouts, 1) * 40 if target_workouts else 0
calorie_score = min(max_calories / total_calories, 1) * 40 if total_calories else 40
score = round(workout_score + calorie_score + 20)

# Rating
if score >= 85:
    rating = "Excellent 💪"
elif score >= 70:
    rating = "Good 👍"
elif score >= 50:
    rating = "Fair ⚠️"
else:
    rating = "Poor 🚨"

# Display
st.metric("Workouts Done", workouts_done)
st.metric("Calories This Week", int(total_calories))
st.metric("Weekly Score", score)
st.success(f"Rating: {rating}")
