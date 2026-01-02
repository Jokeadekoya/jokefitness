import streamlit as st
import pandas as pd
from datetime import date

# -------------------- Page Settings --------------------
st.set_page_config(page_title="Fitness Tracker", layout="centered")

# -------------------- Load Data --------------------
try:
    df = pd.read_csv("data.csv", parse_dates=["date"])
except:
    df = pd.DataFrame(columns=[
        "date","workout_done","workout_type","workout_duration","intensity",
        "protein","food_quality","food_portion","water","sleep","stress","mood"
    ])

today = pd.to_datetime(date.today())

st.title("🏋️ Fitness Tracker")
st.subheader(f"Date: {today.date()}")

# -------------------- DAILY INPUT --------------------
st.header("Daily Input")

workout_done = st.checkbox("Workout done today")
workout_type = st.selectbox("Workout type", ["Lower body", "Upper body", "Abdominals"])
workout_duration = st.number_input("Duration (minutes)", min_value=0, step=5)
intensity = st.radio("Intensity", ["Easy", "Medium", "Hard"])

protein = st.number_input("Protein (g)", min_value=0, step=5, value=100)
food_quality = st.slider("Food quality (1=poor, 5=excellent)", 1, 5, value=4)
food_portion = st.selectbox("Food portion", ["Under-eat", "Normal", "Over-eat"], index=1)
water = st.number_input("Water (liters)", min_value=0.0, step=0.1, value=2.0)

sleep = st.number_input("Sleep (hrs)", min_value=0, step=1, value=7)
stress = st.slider("Stress level (1 low - 5 high)", 1, 5, value=3)
mood = st.slider("Mood / Energy level (1 low - 5 high)", 1, 5, value=4)

if st.button("Save Today"):
    df = df[df["date"] != today]
    new_row = pd.DataFrame([[
        today, workout_done, workout_type, workout_duration, intensity,
        protein, food_quality, food_portion, water, sleep, stress, mood
    ]], columns=df.columns)
    df = pd.concat([df, new_row])
    df.to_csv("data.csv", index=False)
    st.success("✅ Saved!")

# -------------------- WEEKLY SCORE --------------------
st.header("Weekly Score")

if not df.empty:
    df["week"] = df["date"].dt.isocalendar().week
    current_week = today.isocalendar().week
    week_df = df[df["week"] == current_week]

    workouts_done = week_df["workout_done"].sum()
    avg_protein = week_df["protein"].mean() if not week_df.empty else 0
    avg_food_quality = week_df["food_quality"].mean() if not week_df.empty else 0
    avg_water = week_df["water"].mean() if not week_df.empty else 0
    avg_sleep = week_df["sleep"].mean() if not week_df.empty else 0
    avg_stress = 6 - week_df["stress"].mean()
    avg_mood = week_df["mood"].mean() if not week_df.empty else 0

    # Pre-filled goals
    target_workouts = 4
    target_protein = 100
    target_food_quality = 4
    target_water = 2.0
    target_sleep = 7
    target_mood = 4

    # Scoring
    score_workout = min(workouts_done / target_workouts, 1) * 30
    score_protein = min(avg_protein / target_protein, 1) * 15
    score_food_quality = min(avg_food_quality / target_food_quality, 1) * 20
    portion_score_map = {"Under-eat": 5, "Normal": 10, "Over-eat": 5}
    score_food_portion = week_df["food_portion"].map(portion_score_map).mean() if not week_df.empty else 0
    score_food_portion = min(score_food_portion, 10)
    score_water = min(avg_water / target_water, 1) * 10
    score_sleep = min(avg_sleep / target_sleep, 1) * 7.5
    score_lifestyle = ((avg_mood + avg_stress)/2)/5 * 7.5

    weekly_score = round(score_workout + score_protein + score_food_quality +
                         score_food_portion + score_water + score_sleep + score_lifestyle)

    if weekly_score >= 85:
        rating = "Excellent 💪"
        color = "green"
    elif weekly_score >= 70:
        rating = "Good 👍"
        color = "yellow"
    elif weekly_score >= 50:
        rating = "Fair ⚠️"
        color = "orange"
    else:
        rating = "Poor 🚨"
        color = "red"

    st.markdown(f"<h2 style='color:{color}'>{rating} - {weekly_score}/100</h2>", unsafe_allow_html=True)

# -------------------- Expandable Detailed Dashboard --------------------
with st.expander("Show Weekly Dashboard & Trends"):
    if not df.empty:
        st.subheader("Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Workouts Done", f"{workouts_done}/{target_workouts}")
        col2.metric("Avg Protein (g)", round(avg_protein))
        col3.metric("Avg Food Quality", round(avg_food_quality,1))

        col4, col5, col6 = st.columns(3)
        col4.metric("Avg Water (L)", round(avg_water,1))
        col5.metric("Avg Sleep (hrs)", round(avg_sleep,1))
        col6.metric("Avg Mood", round(avg_mood,1))

        st.subheader("Weekly Trends")
        trend_data = week_df[["date","workout_duration","protein","food_quality","water","sleep"]].set_index("date")
        st.line_chart(trend_data)

        st.subheader("Detailed Weekly Data")
        st.dataframe(week_df.style.format({
            "protein":"{:.0f}",
            "food_quality":"{:.0f}",
            "water":"{:.1f}",
            "sleep":"{:.1f}",
            "mood":"{:.0f}",
            "stress":"{:.0f}"
        }).background_gradient(subset=["workout_duration","protein","food_quality","water","sleep"], cmap="RdYlGn"))
