import streamlit as st

# Main content
#st.sidebar.title("Pages")

st.title('Predict Bike Usage')
st.header("Model")

st.markdown(
    """
    We used a Random Forest Regressor for our model. We knew we needed a regression model because we needed to predict a number, not a category. 
    Random Forest has many qualities that made it a good choice: it is more accurate than Decision Trees due to its ensemble technique, 
    it is easy to use (no scaling or encoding necessary), and, most importantly in this case, it is pretty easily interpretable. We can 
    look at which features are more or less important and get a general idea of what we should be paying attention to when it comes to 
    in order to predict number of overall bicycle riders.
    """
)

st.markdown(
    """
    After an initial Random Forest, we tuned hyperparameters utilizing GridSearchCV.
    """
)