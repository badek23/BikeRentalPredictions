import streamlit as st
import pandas as pd
import numpy as np
import joblib


st.title('Predict Bike Usage')
st.header("Prediction Simulator")

st.markdown(
    """
    Use this simulator to predict the number of bicycle users. Input the necessary information below and we'll tell you our estimate!
    """
)

season = st.selectbox(label="What season is it?",
             options=["Winter","Spring","Summer","Autumn"],
             index=None, 
             placeholder="Choose an option.")

def change_season(data):
    if data == "Winter":
        return 1
    elif data == "Spring":
        return 2
    elif data == "Summer":
        return 3
    else:
        return 4
    
season = change_season(season)

month = st.selectbox(label="What month is it?",
             options=["January","February","March","April","May","June","July","August","September","October","November","December"],
             index=None, 
             placeholder="Choose an option.")

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

month = change_month(month)

hour = st.slider(label="What hour of the day is it?",
             min_value=0,
             max_value=23,
             step=1)

holiday = st.radio(label="Is the day a holiday?", 
                   options=["Yes","No"])

def change_holiday(data):
    if data == "Yes":
        return 1
    else:
        return 0
    
holiday = change_holiday(holiday)

def change_workingday(data):
    if data == 1:
        return 0
    else:
        return 1

workingday = change_workingday(holiday)

day_of_week = st.selectbox(label="What day of the week is it?",
             options=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
             index=None, 
             placeholder="Choose an option.")

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

day_of_week = change_day_of_week(day_of_week)

def change_weekday(data):
    if data in [0,6]:
        return 0
    else:
        return 1

weekday = change_weekday(day_of_week)

temperature_real = st.slider(label="What is the real temperature (in Celsius)?",
             min_value=-20,
             max_value=41,
             step=1)

# Create normalization calculation

temperature_feel = st.slider(label="What is the temperature feel (in Celsius)?",
             min_value=-20,
             max_value=50,
             step=1)

# Create normalization calculation

humidity = st.slider(label="What is the humidity?",
             min_value=0,
             max_value=100,
             step=1)

def change_humidity(data):
    data = data/100
    return data

humidity = change_humidity(humidity)

wind = st.slider(label="What is the wind speed (in knots)?",
             min_value=0,
             max_value=67,
             step=1)

# Create normalization calculation

weather = st.selectbox(label="What will the weather be like?",
             options=["Clear; or Partly Cloudy",
					  "Misty and Cloudy; or Misty",
					  "Light Snow; or Light Rain and Scattered Clouds with or without Thunderstorm",
					  "Snow and Fog; or Heavy Rain, Ice, and Thunderstorms"],
             index=None, 
             placeholder="Choose an option.")

def change_weather(data):
    if data == "Clear; or Partly Cloudy":
        return 1
    elif data == "Misty and Cloudy; or Misty":
        return 2
    elif data == "Light Snow; or Light Rain and Scattered Clouds with or without Thunderstorm":
        return 3
    else:
        return 4

weather = change_weather(weather)

model = joblib.load("Model.pkl")

if st.button('Click here to predict!'):
    frame = [[season, '0', month, hour, holiday, weekday, workingday, weather, temperature_real, temperature_feel, humidity, wind,'01']]
 
    df = pd.DataFrame(frame, columns=['season','year','mnth','hr','holiday','weekday','workingday','weathersit','temp','atemp','hum','windspeed','day'])
    df = df.values

    pred = model.predict(df)
    st.write('We predict ', round(pred[0]), ' bikers that day.')