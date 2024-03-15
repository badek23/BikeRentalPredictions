import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import joblib
from sklearn.ensemble import RandomForestClassifier

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
OG_data = pd.read_csv("bike-sharing_hourly.csv")


numeric_data = OG_data.select_dtypes(include=[np.number])
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
    colorscale='viridis'
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

means = joblib.load("means.joblib")
list = list(means)
depth = [20,21,22,23,24]
frame = [[depth[0], list[0]], [depth[1], list[1]], [depth[2], list[2]],[depth[3], list[3]],[depth[4], list[4]]]
r2_df = pd.DataFrame(frame, columns=['Max_Depth','R2'])

fig3 = px.line(r2_df, 
            x='Max_Depth', 
            y='R2', 
            labels={"Max_Depth": 'Max Depth', "R2": 'R^2'},
            title='R^2 by Different Max Depths')
fig3.update_layout(
            xaxis = dict(
            tickmode = 'array',
            tickvals = [20,21,22,23,24]
            ))
st.plotly_chart(fig3)


#image = Image.open("photos/NRMSE.png")

#st.image(image, caption='Negative RMSE through GridSearchCV.')

st.markdown(
    """
    We took a look at feature importance next.
    """
)


model = joblib.load("Model2.joblib")

model_feat = model.feature_importances_
columns = data.drop("cnt",axis=1).columns

fig2 = px.bar(model_feat, 
            x=columns, 
            y=model_feat,
            orientation='v',
            title='Model Feature Importance',
            barmode='group',
            color=model_feat,  # Color bars based on counts
            color_continuous_scale='viridis',  # Use the same color scale as matplotlib
            width=800, height=500)
fig2.update_layout(
            xaxis_title="Features", yaxis_title="Importance"
            )

st.plotly_chart(fig2)

st.markdown(
    """
    We see here that the hour of the day is the most important feature by far. This makes sense logically: no matter any other factor, more people will ride bikes during
    the daytime than they will during the night, when far more people are asleep. We see that the second most important feature is temperature feel. This also makes sense
    logically, as we saw in our EDA process.
    """
)
