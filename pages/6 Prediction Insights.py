import streamlit as st
import pandas as pd
import plotly.express as px


# Main text
st.title('Bike Rental Explorations')
st.header('Insights on Predictions')

st.markdown(
    """
    It is important as well for us to double tap into our model by looking at the predictions themselves. To do so, we need to compare the actual and the predicted values of our
     test dataset. We also built in the capability to add a third variable into the below scatterplot to take a look at potential patterns.
    """
)

# Load comparison data between real and predicted values
comparison = pd.read_csv("real_pred.csv")

def change_legend(data):
    if data == 0:
        return 'No'
    else:
        return 'Yes'
    
comparison['workingday'] = comparison['workingday'].apply(change_legend)


chart_type = st.selectbox('Choose a third variable:', ['None','Seasons','Temperature Feel', 'Humidity'])
if chart_type == 'None':
    fig = px.scatter(comparison, 
                x='real', 
                y='prediction', 
                labels={"real": 'Real', "prediction": 'Prediction'},
                trendline='lowess',
                trendline_color_override='red',
                title='Comparison between Real and Predicted Values',
                width=800, height=800)
elif chart_type == 'Temperature Feel':
    fig = px.scatter(comparison, 
                x='real', 
                y='prediction', 
                labels={"real": 'Real', "prediction": 'Prediction','atemp':'Temperature Feel'},
                trendline='lowess',
                trendline_color_override='red',
                title='Comparison between Real and Predicted Values, by Temperature Feel',
                color='atemp',  
                color_continuous_scale='viridis', 
                width=800, height=800)
elif chart_type == 'Humidity':
    fig = px.scatter(comparison, 
                x='real', 
                y='prediction', 
                labels={"real": 'Real', "prediction": 'Prediction','hum':'Humidity'},
                trendline='lowess',
                trendline_color_override='red',
                title='Comparison between Real and Predicted Values, by Humidity',
                color='hum',  
                color_continuous_scale='viridis', 
                width=800, height=800)
elif chart_type == 'Seasons':
    fig = px.scatter(comparison, 
                x='real', 
                y='prediction', 
                labels={"real": 'Real', "prediction": 'Prediction','season':'Seasons'},
                trendline='lowess',
                trendline_color_override='red',
                title='Comparison between Real and Predicted Values, by Seasons',
                color='season',  
                color_continuous_scale='viridis', 
                width=800, height=800)
    

st.plotly_chart(fig)

st.markdown(
    """
    We can see that the LOWESS trendline is generally even - however, we can note a sparser and more variable smattering of data points as the graph moves up and to 
     the right. From this we deduct that variability in this model appears to increase as the value increases. There is also a slight angle at about 150. This slight flattening 
     of the line after this value indicates that the Real value is relatively higher than the Predicted value, as compared to the Real-Predicted comparison before 
     the angle.
    """
)