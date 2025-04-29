# pages/2_Advanced_Analytics.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Advanced Analytics")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('data/Election_Data.csv', encoding='latin1')

df = load_data()
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Trend over time
st.subheader("Historic Vote Trends")
trend = df.groupby('Year')['Votes'].sum().reset_index()
fig_trend = px.line(trend, x='Year', y='Votes', title="Votes Over Time")
st.plotly_chart(fig_trend, use_container_width=True)

# Gender Analysis
st.subheader("Gender Representation Over Time")
gender_trend = df.groupby(['Year', 'Gender']).size().reset_index(name='Count')
fig_gender = px.area(gender_trend, x='Year', y='Count', color='Gender', title="Candidates by Gender Over Time")
st.plotly_chart(fig_gender, use_container_width=True)
