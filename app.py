# app.py
import streamlit as st

# Set page config
st.set_page_config(page_title="Canadian Election Dashboard", layout="wide")

st.title("🇨🇦 Canadian Election Dashboard")
st.markdown("""
Welcome to the interactive Canadian Election dashboard.
Use the sidebar to navigate between sections and explore election results, historical trends, and predictive analytics.
""")

st.sidebar.success("Select a page above ⬆️")
