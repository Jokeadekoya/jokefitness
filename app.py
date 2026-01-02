import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Fitness & Nutrition Tracker", layout="centered")

# -------------------- Load Data --------------------
try:
    df = pd.read_csv("data.csv", parse_dates=["date"])
except:
    df = pd.DataFrame(columns=[
        "date","workout_done","workout_type","workout_duration","intensity",
        "calories","protein","carbs","fats","water","sleep","stress","mood"
    ])

today = pd.to_datetime(date.today())

st.title("🏋️ Personal Fitness & Nutrition Tracker")
st.subheader(f"Date: {today.date()}")

# -------------------- DAILY INPUT --------------------
st.header("Workout / Exercise")
workout_done = st.checkbox("Workout completed today")
workout_type = st.selectbox("Workout type", ["Strength", "Cardio", "Flexibility", "HIIT"])
workout_duration = st.number_input("Duration (minutes)", min_value=0, step=5)
intensity = st.radio("Intensity", ["Easy", "Medium", "Hard"])

st.header("Nutrition")
calories = st.number_input("Calories eaten today", min_value=0, step=50)
protein = st.number_input("Protein (grams)", min_value=0, step=5)
carbs = st.number_input("Carbs (grams)", min_value=0, step=5)
fats = st.number_input("Fats (grams)", min_value=0, step=5)
water = st.number_input("Water intake (cups)", min_value=0, step=1)

st.header("Lifestyle")
sleep = st.number_input("Sleep (hours)", min_value=0, step=1)
stress = st.slider("Stress level (1 low - 5 high)", 1, 5)
mood = st.slider("Mood / Energy level (1 low - 5 high)", 1, 5)

# -------------------- SAVE DAILY DATA --------------------
if st.button("Save Today"):
    # Remove old entry for today
    df = df[df["date"] != today]
    
    new_row = pd.DataFrame([[
        today, workout_done, workout_type, workout_duration, intensity,
        calories, protein, carbs, fats, water, sleep, stress, mood
    ]], columns=df.columns)
    
    df = pd.concat([df, new_row])
    df.to_csv("data.csv", index=False)
    st.success("✅ Today's data saved!")

# -------------------- WEEKLY SUMMARY --------------------
st.header("📊 This Week Summary")

if not df.empty:
    df["week"] = df["date"].dt.isocalendar().week
    current_week = today.isocalendar().week
    week_df = df[df["week"] == current_week]

    # Weekly metrics
    workouts_done = week_df["workout_done"].sum()
    total_workout_minutes = week_df["workout_duration"].sum()
    avg_calories = week_df["calories"].mean()
    avg_protein = week_df["protein"].mean()
    avg_water = week_df["water"].mean()
    avg_sleep = week_df["sleep"].mean()
    avg_stress = 6 - week_df["stress"].mean()  # invert stress: lower stress = higher score
    avg_mood = week_df["mood"].mean()

    # Weekly goals (editable)
    target_workouts = st.number_input("Weekly workout goal (days)", value=4)
    max_calories = st.number_input("Weekly calorie goal (avg/day)", value=2000)
    target_protein = st.number_input("Daily protein goal (grams)", value=100)
    target_water = st.number_input("Daily water goal (cups)", value=8)
    target_sleep = st.number_input("Daily sleep goal (hours)", value=7)
    target_mood = 4  # scale 1-5

    # Scoring
    score_workout = min(workouts_done / target_workouts, 1) * 30 if target_workouts else 0
    score_calories = min(max_calories / avg_calories, 1) * 15 if avg_calories else 15
    score_protein = min(avg_protein / target_protein, 1) * 10
    score_water = min(avg_water / target_water, 1) * 10
    score_sleep = min(avg_sleep / target_sleep, 1) * 10
    score_lifestyle = ((avg_mood + avg_stress)/2)/5 * 25  # mood + stress weighted

    weekly_score = round(score_workout + score_calories + score_protein +
                         score_water + score_sleep + score_lifestyle)

    # Rating
    if weekly_score >= 85:
        rating = "Excellent 💪"
    elif weekly_score >= 70:
        rating = "Good 👍"
    elif weekly_score >= 50:
        rating = "Fair ⚠️"
    else:
        rating = "Poor 🚨"

    # Display
    st.metric("Workouts Done", workouts_done)
    st.metric("Total Workout Minutes", total_workout_minutes)
    st.metric("Average Calories", round(avg_calories) if avg_calories else 0)
    st.metric("Weekly Score", weekly_score)
    st.success(f"Rating: {rating}")

    # Optional: chart trends
    st.subheader("Weekly Trends")
    chart_data = week_df[["date","calories","workout_duration","water","sleep"]].set_index("date")
    st.line_chart(chart_data)
