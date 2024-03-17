import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Set page title and header
st.title("Bike Rental Explorations")
st.header('Recommendations for Optimization')
st.markdown("Coupons; special events; cost optimizing.. and more!")

# Load bikesharing dataset (assuming 'data' is your bikesharing dataset)
data = pd.read_csv("bike-sharing_hourly.csv")

# Title: COUPONS & OTHER GIFTS:
st.subheader("**Coupons & Other Gifts:**")

# Group by 'weekday' and sum the counts
weekday_counts = data.groupby('weekday')['cnt'].sum().reset_index()

# Create the bar chart using Plotly Express
fig1 = px.bar(weekday_counts, x='weekday', y='cnt', 
            title='Count of Rentals by Day of Week',
            labels={'cnt': 'Count of Rentals', 'weekday': 'Day of Week'},
            color='cnt', 
            color_continuous_scale='viridis',  
            width=800, height=500)
fig1.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [0,1,2,3,4,5,6],
            ticktext = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        ))
st.plotly_chart(fig1)

# Bold and italicized text: Insights
st.markdown("*Insights:*")
# Text below the chart
st.write("""
    It's interesting to note that the total count gradually increases as the week continues, 
    and then, strangely, goes back down on Saturday (which is a day where we would expect more people to rent). 
    From this, we can deduce that a large majority of the customer base uses the bikes to go to work 
    (so during the week). There could potentially be some interesting promotional campaigns made around this insight. 
""")

# Bold and italicized text: Recommendations
st.markdown("*Recommendations:*")
# Text below the chart
st.write("""
    For example, we could recommend to create a promotional campaign to encourage people to rent more during the week-end, 
    e.g: "*First 3 minutes are free on Sundays*" (Sundays because it is the least popular day).
""")

# Title: Bonuses and other offers:
st.subheader("**Bonuses and Other Offers:**")

# Define labels and sizes for the pie chart
labels = ['Casual', 'Registered']
sizes = [data['casual'].sum(), data['registered'].sum()]
colors = ['darkcyan', 'rebeccapurple']

# Create the pie chart using Plotly Express
fig5 = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=0.5, textinfo='percent', marker=dict(colors=colors))])

# Set layout options
fig5.update_layout(title='Share of Casual and Registered Users')

# Show the chart
st.plotly_chart(fig5)

# Bold and italicized text: Insights
st.markdown("*Insights:*")
# Text below the chart
st.write("""
    We can see from this donut chart that there is a large unbalance on how total usage/count is shared between casual bike riders and ones registered with the service. Registered users take the bikes around 4 times more as casuals!
""")

# Bold and italicized text: Recommendations
st.markdown("*Recommendation:*")
# Text below the chart
st.write("""
    This large unbalance between the types of users could be a good indication to perhaps change the bike sharing app to a 'Freemium' type of service.. giving more options and bonuses to registered users, and so inciting more people to pay for a subscription. Like for example, free unlocks (taking inspiration from how services like Uber Lime work).
""")

# Title: Cost optimizing; fleet management; and technical improvements:
st.subheader("**Cost Optimizing; Fleet Management; and Technical Improvements:**")

# Group by 'season' and sum the counts
season_counts = data.groupby('season')['cnt'].sum().reset_index()

# Create the bar chart using Plotly Express
fig2 = px.bar(season_counts, 
            x='season', 
            y='cnt', 
            labels={"season": 'Season', "cnt": 'Count of Rentals'},
            title='Count of Rentals by Season',
            barmode='group',
            color='cnt',
            color_continuous_scale='viridis', 
            width=800, height=500)  
fig2.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [1,2,3,4],
            ticktext = ["Spring","Summer","Autumn","Winter"]
        ))
st.plotly_chart(fig2)

# Bold and italicized text: Insights
st.markdown("*Insights:*")
# Text below the chart
st.write("""
    This is also an interesting insight for seasonal campaigns or cost optimization decisions.
    There is an evident variation in the quantity of bike rentals between the different seasons, 
    giving easy indications to the customer on how to manage the bike fleet according to this. 
""")

# Bold and italicized text: Recommendations
st.markdown("*Recommendations:*")
# Text below the chart
st.write("""
    For example, the customer could deploy fewer bikes during Spring and Winter seasons, as that is when there have been the least rentals. 
    And, on the contrary, the customer could then increase the number of available bikes in Summer and Fall. 
    This would help reduce the costs of maintaining the bikes during the least popular seasons and would increase profits when bikes are very popular, so during Summer and Fall.
""")

# Group by 'weathersit' and sum the counts
weather_counts = data.groupby('weathersit')['cnt'].sum().reset_index()

fig4 = px.bar(weather_counts, 
            x='cnt', 
            y='weathersit', 
            labels={"cnt": 'Count of Rentals',"weathersit": 'Weather Type'},
            title='Count of Rentals by Weather',
            orientation='h',
            barmode='group',
            color='cnt',  
            color_continuous_scale='viridis',
            width=800, height=500)
fig4.update_layout(
        yaxis = dict(
            tickmode = 'array',
            tickvals = [1,2,3,4],
            ticktext = ["Mostly Clear",
                    "Misty",
                    "Light Rain or Snow",
                    "Heavy Rain or Snow, and Thunderstorms"]
        ))
st.plotly_chart(fig4)

# Bold and italicized text: Insights
st.markdown("*Insights:*")
# Text below the chart
st.write("""
    Although this is a rather logical insight and not particularly technical, we cannot overlook basic stats like these ones. As we can see, the total count of rentals is quite low in certain weather conditions..
""")

# Bold and italicized text: Recommendations
st.markdown("*Recommendations:*")
# Text below the chart
st.write("""
    The amount of bikes rented is so low for weather conditions 3 & 4 that it might be wise to limit the capacity and availability of these bikes during those times in order to increase cost optimization 
    and avoid spending money while leaving these bikes idle and paying employees managing them when not many people rent them.
""")

# Create the heatmap with Plotly Express
correlation_matrix = data[['temp', 'hum', 'windspeed', 'cnt']].corr()

# Convert correlation matrix to DataFrame
correlation_df = correlation_matrix.reset_index().melt(id_vars='index')

# Create the heatmap with Plotly Express
fig_heatmap = px.imshow(correlation_df.pivot(index='index', columns='variable', values='value'),
                        labels=dict(index="Variables", variable="Variables", color="Correlation"),
                        x=correlation_matrix.columns,
                        y=correlation_matrix.index,
                        color_continuous_scale='Viridis',  # Use a valid colorscale
                        zmin=-1, zmax=1)

# Update layout
fig_heatmap.update_layout(title='Correlation Matrix: Temperature, Humidity, Windspeed, Bike Counts')

# Show the chart
st.plotly_chart(fig_heatmap)

# Bold and italicized text: Insights
st.markdown("*Insights:*")
# Text below the chart
st.write("""
    Here we are plotting a heatmap combining these metrics to see how all these different meteorological conditions affect each other and the total count. We can observe some logical correlations, like for example the negative correlation between temperature and humidity, or the positive correlation between temperature and total count. However, there are some interesting ones, like for example the fact that windspeed is very weakly correlated with count.. showing that is the least important factor in deciding whether or not to ride a bike.
""")

# Bold and italicized text: Recommendations
st.markdown("*Recommendations:*")
# Text below the chart
st.write("""
    In that case, we could recommend the customer to implement/build something on the bikes to resist more against other meteorological factors (like humidity for example), rather than wind.
""")