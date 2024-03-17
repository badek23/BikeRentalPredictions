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
    Now that we know the split between casual and registered users overall, we can see if there are any differences between these two groups. Let's see if there is
     a difference in which days they tend to bike. Use the dropdown menu below to take a look at the split by months and seasons as well.
    """
)



# Form data for the following charts
weekly_counts = data.groupby('weekday')[['casual','registered']].sum().reset_index()
monthly_counts = data.groupby('mnth')[['casual','registered']].sum().reset_index()
season_counts = data.groupby('season')[['casual','registered']].sum().reset_index()

chart_type = st.radio('Choose a time period:', ['Weeks', 'Months', 'Seasons'])

# Format the data properly so we can use it to show percentages in the stacked bar charts
week_reg = data.groupby('weekday')[['registered']].sum().reset_index()
week_reg['TYPE'] = 'Registered'
week_reg['user'] = week_reg['registered']
week_reg = week_reg.drop('registered',axis=1)

week_cas = data.groupby('weekday')[['casual']].sum().reset_index()
week_cas['TYPE'] = 'Casual'
week_cas['user'] = week_cas['casual']
week_cas = week_cas.drop('casual',axis=1)

# Combine above DFs vertically and add weight column
combine_week = (week_reg,week_cas)
total_week = pd.concat(combine_week)
total_week['weight'] = total_week['user'] / total_week.groupby(['weekday'])['user'].transform('sum')

# Format the data properly so we can use it to show percentages in the stacked bar charts
month_reg = data.groupby('mnth')[['registered']].sum().reset_index()
month_reg['TYPE'] = 'Registered'
month_reg['user'] = month_reg['registered']
month_reg = month_reg.drop('registered',axis=1)

month_cas = data.groupby('mnth')[['casual']].sum().reset_index()
month_cas['TYPE'] = 'Casual'
month_cas['user'] = month_cas['casual']
month_cas = month_cas.drop('casual',axis=1)

# Combine above DFs vertically and add weight column
combine_month = (month_reg,month_cas)
total_month = pd.concat(combine_month)
total_month['weight'] = total_month['user'] / total_month.groupby(['mnth'])['user'].transform('sum')

# Format the data properly so we can use it to show percentages in the stacked bar charts
season_reg = data.groupby('season')[['registered']].sum().reset_index()
season_reg['TYPE'] = 'Registered'
season_reg['user'] = season_reg['registered']
season_reg = season_reg.drop('registered',axis=1)

season_cas = data.groupby('season')[['casual']].sum().reset_index()
season_cas['TYPE'] = 'Casual'
season_cas['user'] = season_cas['casual']
season_cas = season_cas.drop('casual',axis=1)

# Combine above DFs vertically and add weight column
combine_season = (season_reg,season_cas)
total_season = pd.concat(combine_season)
total_season['weight'] = total_season['user'] / total_season.groupby(['season'])['user'].transform('sum')

# Plot share of type of users by time period

if chart_type == 'Weeks':
    fig2 = px.bar(total_week, x="weekday", y='weight', color='TYPE',  
              title="Share of Casual and Registered Users by Day of Week",
              labels={'weight': 'Share', 'TYPE': 'Type of User','weekday':'Day of Week'},
              color_discrete_sequence=['rebeccapurple','darkcyan'],
              width=800, height=500)
    fig2.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = [0,1,2,3,4,5,6],
                ticktext = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
                )
            )
    fig2.update_traces(texttemplate='%{value:.2f}')
elif chart_type == 'Months':
    fig2 = px.bar(total_month, x="mnth", y='weight', color='TYPE',  
              title="Share of Casual and Registered Users by Month",
              labels={'weight': 'Share', 'TYPE': 'Type of User','mnth':'Month'},
              color_discrete_sequence=['rebeccapurple','darkcyan'],
              width=800, height=500)
    fig2.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = [1,2,3,4,5,6,7,8,9,10,11,12],
                ticktext = ["January","February","March","April","May","June","July","August","September","October","November","December"]
            ))
    fig2.update_traces(texttemplate='%{value:.2f}')
elif chart_type == 'Seasons':
    fig2 = px.bar(total_season, x="season", y='weight', color='TYPE',  
              title="Share of Casual and Registered Users by Season",
              labels={'weight': 'Share', 'TYPE': 'Type of User','season':'Season'},
              color_discrete_sequence=['rebeccapurple','darkcyan'],
              width=800, height=500)
    fig2.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = [1,2,3,4],
                ticktext = ["Spring","Summer","Autumn","Winter"]
            ))
    fig2.update_traces(texttemplate='%{value:.2f}')
st.plotly_chart(fig2)

st.markdown(
    """
    We see that there is a clear pattern where during the weekdays, a higher proportion of users are registered, and on the weekends, a larger number of casual users
     rent bikes. This corroberates a previous theory we stated, where we hypothesized that a fair number of bikers are commuters who do not commute on the weekends. We
     also see that a lower proportion of casual users rent bicycles during the colder months/seasons. As registered users likely pay a subscription fee, we hypothesize 
     that this difference may be due to casual users having an easier "out" if the weather is cold: they haven't spent any money yet, so might as well transport themselves 
     another way. Alternatively, as we already know that a higher proportion of those renting bikes during weekdays are registered users, perhaps more registered users 
     must rent a bike in order to commute to work, no matter the weather, while casual riders simply have more choice in the matter.
    """
)