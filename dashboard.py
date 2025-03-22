import streamlit as st
import requests
import pandas as pd

st.title("WasteWise Dashboard")

# Fetch bin data from Flask API
response = requests.get("http://127.0.0.1:5000/bins")
bins = response.json()

# Display bin data in a table
df = pd.DataFrame(bins)
st.write(df)
