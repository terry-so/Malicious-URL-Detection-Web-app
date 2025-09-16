import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Malicious URL Detector",
    page_icon="🛡️",
    layout="centered"
)

st.title("Malicious URL Detector")
st.write("Enter a URL to check if it's benign or malicious. This app uses a machine learning model to predict the result.")

user_url = st.text_input("Enter URL here:", placeholder="e.g., http://google.com")

if st.button("Check URL"):
    if user_url: 
        api_url = "https://malicious-url-detection-web-app.onrender.com"
        payload = {"domain": user_url}
        st.write("Sending URL to the model for prediction...")
        response = requests.post(api_url, json=payload)
        result = response.json()
        prediction = result.get("prediction")

        st.write("")
        if prediction == "Malicious":
            st.error(f"**Prediction:** This URL is likely **{prediction}**!")
        else:
            st.success(f"**Prediction:** This URL appears to be **{prediction}**.")
    
    else:
        st.warning("Please enter a URL to check.")