import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Main content

st.title('Predict Bike Usage')
st.header("Model Selection")

st.markdown(
    """
    Before training a model, we need to select features. We decided to remove several features through logic. We removed "yr" (year) because years are not cyclical: 
    we can never have a new data point in 2011 or 2012, so training a model on those numbers is useless. We dropped "registered" and "casual" as these are parts of
    the larger target variable, and therefore of course would be very highly correlated with the target variable. However, we cannot, of course, know these numbers in advance,
    which makes them useless for prediction. We also removed "instant" because it is only an identifier. Lastly, we also calculated "day" (day of the month) from "dteday" 
    and dropped "dteday" as we now had all of that information in other features.
    """
)
st.markdown(
    """
    We next took a look at a correlation matrix to understand if there is any multicollinearity between features.
    """
)
# CORRELATION MATRIX

# Exclude non-numeric columns from the correlation matrix
# we are excluding the dateday column
data = pd.read_csv("cleaned_data.csv")

numeric_data = data.select_dtypes(include=[np.number])
correlation = numeric_data.corr().abs()

# Reverse the order of rows and columns
correlation = correlation.iloc[::-1, ::-1]

# Create a heatmap with reversed diagonal values
fig = go.Figure(data=go.Heatmap(
    z=correlation.values,  # Use the corrected correlation matrix
    x=list(correlation.columns),
    y=list(correlation.index),
    text=correlation.values.round(2).astype(str),  # Use original values for annotations
    hoverinfo='text',
    colorscale='Blues'
))

# Update layout to make it more readable
fig.update_layout(
    title='Diagonal Correlation Matrix',  # Update title
    xaxis=dict(tickangle=45, side='top', automargin=True),  # Rotate x-axis labels and enable auto margin
    yaxis=dict(tickmode='array', automargin=True),
    autosize=False,  # Disable autosize to set custom width and height
    width=800,  # Increase width if needed
    height=800,  # Increase height if needed
    margin=dict(l=150, r=150, b=100, t=235)  # Adjust margins to fit labels, increase top margin
)

# Show the corrected diagonal figure
st.plotly_chart(fig)


st.markdown(
    """
    It is clear here that atemp (temperature feel) and temp (real temperature) are extremely correlated, which makes sense. We'll remove one of these features. We decided 
    to remove temp as people may act more on how warm it feels outside.
    """
)

st.markdown(
    """
    We then trained a Random Forest Regressor for our model. We knew we needed a regression model because we needed to predict a number, not a category. 
    Random Forest has many qualities that made it a good choice: it is more accurate than Decision Trees due to its ensemble technique, 
    it is easy to use (no scaling or encoding necessary), and, most importantly in this case, it is pretty easily interpretable. We can 
    look at which features are more or less important and get a general idea of what we should be paying attention to 
    in order to predict number of overall bicycle riders.
    """
)

st.markdown(
    """
    After an initial Random Forest, we tuned hyperparameters utilizing GridSearchCV.
    """
)

image = Image.open("photos/NRMSE.png")

st.image(image, caption='Negative RMSE through GridSearchCV.')

st.markdown(
    """
    We took a look at feature importance next.
    """
)

