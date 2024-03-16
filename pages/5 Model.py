import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import joblib
from sklearn.ensemble import RandomForestClassifier

# Main content

st.title('Bike Rental Explorations')
st.header("Model Selection")


st.markdown(
    """
    After exploring the data for a while, we needed to choose a predictive model.
    """
)
st.markdown(
    """
    Before we train a model, we need to select features. We decided to remove several features through logic. We removed "yr" (year) because years are not cyclical: 
    we can never have a new data point in 2011 or 2012, so training a model on those numbers is useless. We dropped "registered" and "casual" as we cannot, of course, know these numbers in advance,
    which makes them useless for prediction - they are, after all, simply portions of the target variable. We also removed "instant" because it is only an identifier. Lastly, we calculated "day" (day of the month) from "dteday" 
    and dropped "dteday" as we now had all of that information contained in other features.
    """
)
st.markdown(
    """
    After these initial feature choices, we next took a look at a correlation matrix to understand if there is any further multicollinearity between features.
    """
)

# CORRELATION MATRIX

data = pd.read_csv("cleaned_data.csv")

# Exclude non-numeric columns from the correlation matrix
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

st.plotly_chart(fig)


st.markdown(
    """
    It is clear here that "atemp" (temperature feel) and "temp" (real temperature) are extremely correlated, which makes sense. We'll remove one of these features. We decided 
    to remove "temp" as people may act more on how warm it feels outside.
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
    After an initial Random Forest, we tuned hyperparameters utilizing GridSearchCV. We used R^2 as the evaluation metric because it is an easy-to-understand way of
    explaining how much variance is explained by the model. We focused specifically on max depth when it came to tuning hyperparameters because it is one of the 
    hyperparameters with the largest singular affect on results.
    """
)


# Plot R^2 by depths during cross-validation

# Load means data and manipulate it into a DataFrame along with the Max_Depths
means = joblib.load("means.joblib")
list = list(means)
depth = [20,21,22,23,24]
frame = [[depth[0], list[0]], [depth[1], list[1]], [depth[2], list[2]],[depth[3], list[3]],[depth[4], list[4]]]
r2_df = pd.DataFrame(frame, columns=['Max_Depth','R2'])

fig3 = px.line(r2_df, 
            x='Max_Depth', 
            y='R2', 
            labels={"Max_Depth": 'Max Depth', "R2": 'R^2'},
            title='R^2 by Different Max Depths'
            )
fig3.update_layout(
            xaxis = dict(
            tickmode = 'array',
            tickvals = [20,21,22,23,24]
            ),
            showlegend=False,
            )
fig3.update_traces(mode="markers+lines", line_color='rebeccapurple')
st.plotly_chart(fig3)


st.markdown(
    """
    After several cycles of testing various ranges of max depths, we tested 20-24 and found that the highest R^2 is at a max depth of 22. We therefore chose to use a Random Forest Regression
    with a max depth of 22 as our final model.
    """
)


st.markdown(
    """
    We took a look at feature importance next.
    """
)


# Plot Feature Importance

# Load model
model = joblib.load("Model2.joblib")

model_feat = model.feature_importances_
columns = data.drop("cnt",axis=1).columns

fig2 = px.bar(model_feat, 
            x=columns, 
            y=model_feat,
            orientation='v',
            title='Model Feature Importance',
            barmode='group',
            color=model_feat,  
            color_continuous_scale='viridis',  
            width=800, height=500)
fig2.update_layout(
            xaxis_title="Feature", yaxis_title="Importance"
            )

st.plotly_chart(fig2)

st.markdown(
    """
    We see here that the hour of the day is the most important feature by far. This makes sense logically: no matter any other factor, more people will ride bikes during
    the daytime than they will during the night, when far more people are asleep. We see that the second most important feature is temperature feel. This also makes sense
    logically, as we saw in our EDA process.
    """
)

st.markdown(
    """
    We of course, lastly, validated our model on the test set. Compared to the train dataset's 0.845 R^2, the test dataset had an R^2 of 0.789. This is a decrease, but in this 
    case is sufficient for approximating number of bike rentals.
    """
)
