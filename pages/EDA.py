import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Main content
st.title('Predict Bike Usage')
st.header("Exploratory Data Analysis")

st.markdown(
    """
    In our exploration, we needed to ensure there were no nulls or otherwise wonky data, and we also needed to take a look under the hood to inspect trends and patterns. 
    """
)
st.markdown(
    """
    We began by seeing if there is any seasonality in regards to how many bikes are rented.
    """
)

data = pd.read_csv("cleaned_data.csv")

# Plot rentals by season

chart_type = st.radio('Choose a time period:', ['Seasons', 'Months'])

if chart_type == 'Seasons':
    fig1 = px.bar(data, 
                x='season', 
                y='cnt', 
                labels={"season": 'Season', "cnt": 'Count of Rentals'},
                title='Count of Rentals by Season',
                barmode='group')
    fig1.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = [1,2,3,4],
                ticktext = ["Spring","Summer","Autumn","Winter"]
            ))
elif chart_type == 'Months':
    fig1 = px.bar(data, 
                x='mnth', 
                y='cnt', 
                labels={"mnth": 'Month', "cnt": 'Count of Rentals'},
                title='Count of Rentals by Month',
                barmode='group') 
    fig1.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = [1,2,3,4,5,6,7,8,9,10,11,12],
                ticktext = ["January","February","March","April","May","June","July","August","September","October","November","December"]
            ))
st.plotly_chart(fig1)

st.markdown(
    """
    We see here that there is a very clear seasonal change in bike demand. During the Winter and Spring, demand drops, while during the Summer and Autumn, more people rent bikes.
    This trend is true when we split the data into monthly points as well.
    """
)

st.markdown(
    """
    We investigate bike rentals by weather as well.
    """
)

fig2 = px.bar(data, 
            x='weathersit', 
            y='cnt', 
            labels={"weathersit": 'Weather Type', "cnt": 'Count of Rentals'},
            title='Count of Rentals by Weather',
            barmode='group')
fig2.update_layout(
        xaxis = dict(
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
    """
)

# Upload data that still includes years
year_data = pd.read_csv("bike-sharing_hourly.csv")
# Calculate day field
year_data['day'] = year_data['dteday'].apply(lambda x: str(x)[-2:])
year_data['atemp'] = year_data['atemp'].apply(lambda x: x*50)
# Group by years, months, day and get a daily average temperature feel + sum of daily counts
year_data = year_data.groupby(["yr","mnth","day"]).agg({
    'atemp': 'mean',
    'cnt': 'sum'
    })

fig3 = px.scatter(year_data, 
            x='atemp', 
            y='cnt', 
            labels={"atemp": 'Temperature Feel (C)', "cnt": 'Count of Rentals'},
            trendline='lowess',
            trendline_color_override='red',
            title='Count of Rentals by Temperature Feel')
st.plotly_chart(fig3)

st.markdown(
    """
    We see here that there is a marked pattern to amounts of bikes rented: it increases steadily as the temperature gets warmer, until about 30 C, when it flattens and even goes down slightly.
    Logically, these takeaways make sense: people like riding bikes more as it gets warmer, but not when it gets too hot.
    """
)