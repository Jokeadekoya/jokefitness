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
intensity = st
