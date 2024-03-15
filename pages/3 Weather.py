import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Main content
st.title('Predict Bike Usage')
st.header("Exploratory Data Analysis: Weather")

st.markdown(
    """
    Next, we looked at weather. Anecdotally, people tend to bike more during nicer weather, so we hypothesized that we would see patterns here as well.
    """
)
st.markdown(
    """
    We first investigated how many bikes are rented by type of weather.
    """
)

# Load data
data = pd.read_csv("cleaned_data.csv")

# Plot count of rentals by type of weather

weather_counts = data.groupby('weathersit')['cnt'].sum().reset_index()

fig2 = px.bar(weather_counts, 
            x='cnt', 
            y='weathersit', 
            labels={"cnt": 'Count of Rentals',"weathersit": 'Weather Type'},
            title='Count of Rentals by Weather',
            orientation='h',
            barmode='group',
            color='cnt',  
            color_continuous_scale='viridis',
            width=800, height=500)
fig2.update_layout(
        yaxis = dict(
            tickmode = 'array',
            tickvals = [1,2,3,4],
            ticktext = ["Mostly Clear",
                    "Misty",
                    "Light Rain or Snow",
                    "Heavy Rain or Snow, and Thunderstorms"]
        ))
st.plotly_chart(fig2)

st.markdown(
    """
    We see here that, as is logical, more people rent bikes the nicer the weather. In the very worst of weather, very few people rent bikes.
    """
)

st.markdown(
    """
    We check next the bike rental counts by daily temperature. The red line is the line of best fit utilizing Locally Weighted Scatterplot Smoothing.
    Use the dropdown menu to change the colors in the chart to a third, optional, weather-related variable as well.
    """
)


# Upload data that still includes years
year_data = pd.read_csv("bike-sharing_hourly.csv")

# Edit dataset
year_data['day'] = year_data['dteday'].apply(lambda x: str(x)[-2:])
year_data['atemp'] = year_data['atemp'].apply(lambda x: x*50)
year_data['Humidity'] = year_data['hum'].apply(lambda x: x*100)
year_data['Windspeed'] = year_data['windspeed'].apply(lambda x: x*67)


# Group by years, months, day and get a daily average temperature feel + sum of daily counts

chart_type = st.selectbox('Choose a third variable:', ['None','Windspeed', 'Humidity'])

if chart_type == 'None':
    year_dataset = year_data.groupby(["yr","mnth","day"]).agg({
        'atemp': 'mean',
        'cnt': 'sum'
        })
    fig3 = px.scatter(year_dataset, 
                x='atemp', 
                y='cnt', 
                labels={"atemp": 'Temperature Feel (C)', "cnt": 'Sum of Rentals'},
                trendline='lowess',
                trendline_color_override='red',
                title='Daily Sum of Rentals by Temperature Feel',
                color='cnt',  # Color bars based on counts
                color_continuous_scale='viridis',  # Use the same color scale as matplotlib
                width=800, height=500)
elif chart_type == 'Windspeed':
    year_dataset = year_data.groupby(["yr","mnth","day"]).agg({
        'atemp': 'mean',
        'cnt': 'sum',
        'Windspeed':'mean'
        })
    fig3 = px.scatter(year_dataset, 
                x='atemp', 
                y='cnt', 
                labels={"atemp": 'Temperature Feel (C)', "cnt": 'Sum of Rentals'},
                trendline='lowess',
                trendline_color_override='red',
                title='Daily Sum of Rentals by Temperature Feel',
                color='Windspeed',  # Color bars based on counts
                color_continuous_scale='viridis',  # Use the same color scale as matplotlib
                width=800, height=500)
elif chart_type == 'Humidity':
    year_dataset = year_data.groupby(["yr","mnth","day"]).agg({
        'atemp': 'mean',
        'cnt': 'sum',
        'Humidity':'mean'
        })
    fig3 = px.scatter(year_dataset, 
                x='atemp', 
                y='cnt', 
                labels={"atemp": 'Temperature Feel (C)', "cnt": 'Sum of Rentals'},
                trendline='lowess',
                trendline_color_override='red',
                title='Daily Sum of Rentals by Temperature Feel',
                color='Humidity',  # Color bars based on counts
                color_continuous_scale='viridis',  # Use the same color scale as matplotlib
                width=800, height=500)
st.plotly_chart(fig3)

st.markdown(
    """
    We see here that there is a marked pattern to amounts of bikes rented: it increases steadily as the temperature gets warmer, until about 30 C, when it flattens and even goes down slightly.
    Logically, these takeaways make sense: people like riding bikes more as it gets warmer, but not when it gets too hot. We see as well, through the optional third
    variables, that high humidity or windspeed appears to be correlated with slightly fewer people renting bikes. 
    """
)