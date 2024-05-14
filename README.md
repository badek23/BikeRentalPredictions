# Bike Rental Predictions
### About this project
This project was in collaboration with a classmate. Provided data on a bike rental company, we created an app that provides (1) important insights into the data found through EDA, (2) a model that predicts number of bike rentals by hour, (3) insights on how the model performs, (4) recommendations for the business based on our insights, and finally (5) a simulator that takes user input and predicts the number of bike rentals. The deployed app can be found here: https://bikerentalpredictor.streamlit.app/

### Technologies 
This project is coded in Python. Libraries used include: 🎨streamlit | 🧠scikit-learn | 📉plotly | 🌊seaborn | 🐼pandas | 🧮numpy | 🔧joblib

### Files
- Overview: This file contains the script for the landing page of the app.
- pages: This folder contains all of the scripts for the other pages of the app.
- EDA_and_prep: This file contains all script for creation of the project, including EDA, model creation, etc.
- Model2: This joblib file contains the model for upload into the app.
- Model3: This joblib file contains the updated model after removing features deemed unimportant through feature importance analysis.
- bike_sharing_hourly: This csv is the original, provided data.
- cleaned_data: This csv is the cleaned data.
- means: This joblib file contains data about the model, which is used in creating some visuals in the app.
- means3: This joblib file contains some data about model3.
- real_pred: This csv contains predictions on a test dataset.
- .streamlit: This file contains theme code for the app.
