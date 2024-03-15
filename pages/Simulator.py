# Import libraries

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier

# Page text

st.title('Predict Bike Usage')
st.header("Prediction Simulator")

st.markdown(
    """
    Use this simulator to predict the number of bicycle users. Input the necessary information below and we'll tell you our estimate!
    """
)

# Create two columns
col1,col2 = st.columns(2)

# Data gathering

season = col1.selectbox(label="What season is it?",
             options=["Winter","Spring","Summer","Autumn"],
             index=None, 
             placeholder="Choose an option.")

if season == "Winter":
    month = col1.selectbox(label="What month is it?",
                options=["December","January","February","March"],
                index=None, 
                placeholder="Choose an option.")
elif season == "Spring":
    month = col1.selectbox(label="What month is it?",
                options=["March","April","May","June"],
                index=None, 
                placeholder="Choose an option.")
elif season == "Summer":
    month = col1.selectbox(label="What month is it?",
                options=["June","July","August","September"],
                index=None, 
                placeholder="Choose an option.")
else:  
    month = col1.selectbox(label="What month is it?",
             options=["September","October","November","December"],
             index=None, 
             placeholder="Choose an option.")

day = col1.slider(label="What day of the month is it?",
             min_value=1,
             max_value=31,
             step=1)

hour = col1.slider(label="What hour of the day is it?",
             min_value=0,
             max_value=23,
             step=1)

day_of_week = col1.selectbox(label="What day of the week is it?",
             options=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
             index=None, 
             placeholder="Choose an option.")

if day_of_week in ["Monday","Tuesday","Wednesday","Thursday","Friday"]:
    holiday = col1.radio(label="Is the day a holiday?", 
                    options=["Yes","No"])

temperature_feel = col2.slider(label="What is the temperature feel (in Celsius)?",
             min_value=0,
             max_value=50,
             step=1)

humidity = col2.slider(label="What is the humidity?",
             min_value=0,
             max_value=100,
             step=1)

wind = col2.slider(label="What is the wind speed (in knots)?",
             min_value=0,
             max_value=67,
             step=1)

weather = col2.selectbox(label="What will the weather be like?",
             options=["Clear; or Partly Cloudy",
					  "Misty and Cloudy; or Misty",
					  "Light Snow; or Light Rain and Scattered Clouds with or without Thunderstorm",
					  "Snow and Fog; or Heavy Rain, Ice, and Thunderstorms"],
             index=None, 
             placeholder="Choose an option.")



# Create functions to translate input data into numbers that the model will process

def change_season(data):
    if data == "Winter":
        return 1
    elif data == "Spring":
        return 2
    elif data == "Summer":
        return 3
    else:
        return 4
    
def change_month(data):
    if data == "January":
        return 1
    elif data == "February":
        return 2
    elif data == "March":
        return 3
    elif data == "April":
        return 4
    elif data == "May":
        return 5
    elif data == "June":
        return 6
    elif data == "July":
        return 7
    elif data == "August":
        return 8
    elif data == "September":
        return 9
    elif data == "October":
        return 10
    elif data == "November":
        return 11
    elif data == "December":
        return 12

def change_holiday(data):
    if data == "Yes":
        return 1
    else:
        return 0
    
def change_day_of_week(data):
    if data == "Monday":
        return 1
    elif data == "Tuesday":
        return 2
    elif data == "Wednesday":
        return 3
    elif data == "Thursday":
        return 4
    elif data == "Friday":
        return 5
    elif data == "Saturday":
        return 6
    else:
        return 0

def change_weekday(data):
    if data in [1,5]:
        return 0
    else:
        return 1

temperature_feel = temperature_feel/50

humidity = humidity/100

wind = wind/67

def change_weather(data):
    if data == "Clear; or Partly Cloudy":
        return 1
    elif data == "Misty and Cloudy; or Misty":
        return 2
    elif data == "Light Snow; or Light Rain and Scattered Clouds with or without Thunderstorm":
        return 3
    else:
        return 4

def change_workingday(data1, data2):
    if data1 == 0 and data2 == 0:
        return 0
    else:
        return 1


# Run functions 
    
season = change_season(season)
month = change_month(month)
day_of_week = change_day_of_week(day_of_week)
weekday = change_weekday(day_of_week)
weather = change_weather(weather)


if weekday == 0:
    holiday = change_holiday(holiday)
else:
    holiday = 0

workingday = change_workingday(holiday, weekday)



# Upload model
model = joblib.load("Model.joblib")

# Make prediction and display answer
if st.button('Click here to predict!'):
    frame = [[season, month, hour, holiday, weekday, workingday, weather, temperature_feel, humidity, wind, day]]
 
    df = pd.DataFrame(frame, columns=['season','mnth','hr','holiday','weekday','workingday','weathersit','atemp','hum','windspeed','day'])

    pred = model.predict(df)
    st.write('We predict ', round(pred[0]), ' bike users that day.')