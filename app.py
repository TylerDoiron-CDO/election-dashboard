# app.py

import streamlit as st

# Set page config
st.set_page_config(page_title="Canadian Election Dashboard", layout="wide")

st.title("🇨🇦 Canadian Election Dashboard")

st.markdown("""
Welcome to the interactive Canadian Election Dashboard.

This platform provides a deep and dynamic exploration of Canadian federal election data, including:
- Historical election trends
- Provincial and constituency voting patterns
- Party performance over time
- Predictive models for future elections
- Advanced statistical and geospatial analyses

**Developed by Tyler Doiron, MSc, MQM, aCAP**  
Chief Data Officer of Astute Innovations

Tyler Doiron is a data scientist with expertise in machine learning, statistical modeling, and advanced analytics. 
This tool reflects a commitment to making data accessible, insightful, and actionable for political researchers, analysts, and citizens interested in Canada's electoral landscape.

Use the sidebar to navigate between sections and explore the data insights and forecasts.
""")

st.sidebar.success("Select a page to explore ⬆️")
