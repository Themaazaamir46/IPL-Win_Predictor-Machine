import streamlit as st
import pandas as pd
import pickle

# Loading the model
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Adding image at the top
st.image("https://www.orissapost.com/wp-content/uploads/2019/04/ipl-2018_1515079024.jpeg", use_column_width=True)

# Title with color
st.markdown('<h1 style="text-align: center; color: #FFD700;">🏏 IPL Win Probability Predictor 🏏</h1>',
            unsafe_allow_html=True)

# Welcome message with a catchy line
st.markdown('<h3 style="text-align: center; color: #8B4513;">Where Cricket Meets Data Science! 📊🏏</h3>',
            unsafe_allow_html=True)

# List of teams
teams = sorted([
    'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
    'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
    'Rajasthan Royals', 'Delhi Capitals'])

col1, col2 = st.columns(2)

# Selecting boxes for teams
with col1:
    batting_team = st.selectbox('Select the batting team', teams)
with col2:
    bowling_team = st.selectbox('Select the bowling team', teams)

# Cities for selection
cities = [
    'Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
    'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
    'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
    'Sharjah', 'Mohali', 'Bengaluru']

selected_city = st.selectbox('Select the city', sorted(cities))

# Input fields for match data
target = st.number_input('Target', min_value=0)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Score', min_value=0)
with col4:
    wickets = st.number_input('Wickets', min_value=0, max_value=9)
with col5:
    overs = st.number_input('Overs completed', min_value=0, max_value=20)

# Addinging button to predict and display the result
if st.button('Predict Probability'):
    # Calculations for prediction
    runs_left = target - score
    balls_left = 120 - overs * 6
    wickets_left = 10 - wickets
    crr = score / overs
    rrr = runs_left * 6 / balls_left
    df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team],
                       'city': [selected_city], 'runs_left': [runs_left],
                       'balls_left': [balls_left], 'wickets': [wickets_left],
                       'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]})

    # Predicting using the loaded model
    result = pipe.predict_proba(df)
    r_1 = round(result[0][0] * 100)
    r_2 = round(result[0][1] * 100)

    # Stylized result with colors and emojis
    st.markdown(f"<h2 style='color: #FF5733;'>🎉 Winning Probability 🎉</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #28A745;'>🏏 {batting_team} : {r_2}% 🏏</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #DC3545;'>🏏 {bowling_team} : {r_1}% 🏏</h3>", unsafe_allow_html=True)

    # Fun commentary after the result
    if r_2 > r_1:
        st.markdown(f"<h4 style='color: #FFD700;'>🎯 {batting_team} is likely to win! 🎯</h4>", unsafe_allow_html=True)
        st.markdown(
            f"<h5 style='color: #FFFFE0;'>It's looking good for {batting_team}, but cricket is full of surprises! 😎</h5>",
            unsafe_allow_html=True)
    elif r_1 > r_2:
        st.markdown(f"<h4 style='color: #FFD700;'>🔥 {bowling_team} is likely to win! 🔥</h4>", unsafe_allow_html=True)
        st.markdown(
            f"<h5 style='color: #FFFFE0;'>Looks like {bowling_team} is dominating, but don't count out {batting_team} just yet! 😏</h5>",
            unsafe_allow_html=True)
    else:
        st.markdown(f"<h4 style='color: #FFC107;'>🤔 It's too close to call! 🤔</h4>", unsafe_allow_html=True)
        st.markdown(f"<h5 style='color: #FFC107;'>The match could go either way... Get ready for a nail-biter! 😲</h5>",
                    unsafe_allow_html=True)
