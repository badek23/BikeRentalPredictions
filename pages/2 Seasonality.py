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

season_counts = data.groupby('season')['cnt'].sum().reset_index()
month_counts = data.groupby('mnth')['cnt'].sum().reset_index()

if chart_type == 'Seasons':
    fig1 = px.bar(season_counts, 
                x='season', 
                y='cnt', 
                labels={"season": 'Season', "cnt": 'Count of Rentals'},
                title='Count of Rentals by Season',
                barmode='group',
                color='cnt',  # Color bars based on counts
                color_continuous_scale='viridis',  # Use the same color scale as matplotlib
                width=800, height=500)  # Adjust width and height for better appearance

# Add text annotations for each bar
    fig1.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = [1,2,3,4],
                ticktext = ["Spring","Summer","Autumn","Winter"]
            ))
elif chart_type == 'Months':
    fig1 = px.bar(month_counts, 
                x='mnth', 
                y='cnt', 
                labels={"mnth": 'Month', "cnt": 'Count of Rentals'},
                title='Count of Rentals by Month',
                barmode='group',
                color='cnt',  # Color bars based on counts
                color_continuous_scale='viridis',  # Use the same color scale as matplotlib
                width=800, height=500)  # Adjust width and height for better appearance) 
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
    Let's next look at when during the day more people use bikes, as split by workday and weekend day. We hypothesized that there would be a difference in pattern here.
    """
)



year_data['Working Day'] = year_data['workingday']

hour_data = year_data.groupby(["yr","workingday","hr"]).agg({
        'yr':'mean',
        'Working Day':'mean',
        'hr': 'mean',
        'cnt': 'mean'
        })

def change_legend(data):
    if data == 0:
        return 'No'
    else:
        return 'Yes'
    
hour_data['Working Day'] = hour_data['Working Day'].apply(change_legend)

chart_type = st.radio('Choose a year:', ['2011', '2012'])

if chart_type == '2011':
    hour_data = hour_data[hour_data["yr"] == 0]
    fig4 = px.line(hour_data, 
            x='hr', 
            y='cnt', 
            labels={"hr": 'Hour', "cnt": 'Mean Rentals'},
            color='Working Day',
            color_discrete_sequence=['darkcyan', 'rebeccapurple'],
            title='Mean Rentals by Hour')
    fig4.update_traces(mode="markers+lines", hovertemplate=None)
    fig4.update_layout(hovermode="x unified")

if chart_type == '2012':
    hour_data = hour_data[hour_data["yr"] == 1]
    fig4 = px.line(hour_data, 
            x='hr', 
            y='cnt', 
            labels={"hr": 'Hour', "cnt": 'Mean Rentals'},
            color='Working Day',
            title='Mean Rentals by Hour')
    fig4.update_traces(mode="markers+lines", hovertemplate=None)
    fig4.update_layout(hovermode="x unified")
st.plotly_chart(fig4)

st.markdown(
    """
    Our hypothesis was correct! We see here two large spikes at 8:00 and 17:00 during weekdays - these correlate to when people would commute to work.
    On the weekends, in contrast, we see that people tend to go biking later, most likely between 10:00 and 17:00. In this case, we understand that 
    people are less likely to commute to work on the weekends and can take advantage of weekend afternoons for biking for pleasure. We see as well that this pattern
    remains extremely stable from 2011 to 2012.
    """
)