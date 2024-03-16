import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Main content

st.title('Bike Rental Explorations')
st.header("Exploratory Data Analysis: Type of User")


st.markdown(
    """
    It is also important to better understand the users themselves. While we don't have demographic information, we do have some data on casual vs. registered users.
    """
)

st.markdown(
    """
    First, let's take a look at the share of each in the total user base.
    """
)

# Load data
data = pd.read_csv("bike-sharing_hourly.csv")

# Define labels and sizes for the pie chart
labels = ['Casual', 'Registered']
sizes = [data['casual'].sum(), data['registered'].sum()]
colors = ['darkcyan', 'rebeccapurple']

# Create the pie chart using Plotly Express
fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=0.5, textinfo='percent', marker=dict(colors=colors))])

# Set layout options
fig.update_layout(title='Share of Casual and Registered Users')

# Show the chart
st.plotly_chart(fig)

st.markdown(
    """
    Now that we know the split between casual and registered users overall, we can see if there are any differences between these two groups. First, let's see if there is
     a difference in which days they tend to bike.
    """
)

weekly_counts = data.groupby('weekday')[['casual','registered']].sum().reset_index()


fig2 = px.bar(weekly_counts, x="weekday", y=["registered","casual"], 
              title="Share of Casual and Registered Users by Day of Week",
              labels={'registered': 'Registered', 'casual': 'Casual','weekday':'Day of Week'},
              color_discrete_sequence=['rebeccapurple','darkcyan'],
              #color_continuous_scale='viridis',  
              width=800, height=500)
fig2.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [0,1,2,3,4,5,6],
            ticktext = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
            ),
        legend_title_text='Type of User',
        
        )
st.plotly_chart(fig2)

st.markdown(
    """
    We see that there is a clear pattern where during the weekdays, a higher proportion of users are registered, and on the weekends, a larger number of casual users
     rent bikes. This corroberates a previous theory we stated, where we hypothesized that a fair number of bikers are commuters who do not work on the weekends.
    """
)