import streamlit as st

# Sidebar

# Main content
st.title('Predict Bike Usage')
st.header("Overview")

st.markdown(
    """
    Welcome! In this app, you'll discover many different insights on bike rentals. You'll learn more about what factors affect people's likelihood to rent bikes, 
    and you'll learn about trends and patterns on bike usage. We'll discuss weather, seasons, and even the type of biker. You will utilize a new tool that 
    predicts how many people will rent bikes during any given hour, depending on a host of factors. And lastly, we will provide our thoughts on things you can do 
    based on our new knowledge to improve your business and optimize costs. We can't wait to dive in. So let's get started!
    """
)

st.markdown(
    """
    We began, of course, by ensuring the data was clean. Thankfully, there were no nulls or missing values at all - fantastic data quality! We took a look at the data 
    itself, checking that data types were correct and that we fully understood how all normalized variables had been standardized. Then we moved on to exploration. Look 
     through the tabs on the left to learn more!
    """
)