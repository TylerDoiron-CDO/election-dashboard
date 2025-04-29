# pages/1_Home.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏠 Home - Overview")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('data/Election_Data.csv', encoding='latin1')

df = load_data()

# Sidebar filters
province = st.sidebar.multiselect("Select Province/Territory:", options=df['Province_Territory'].unique())
party = st.sidebar.multiselect("Select Political Party:", options=df['Political_Affiliation'].unique())
year = st.sidebar.multiselect("Select Election Year:", options=pd.to_datetime(df['Date']).dt.year.unique())

# Apply filters
df_filtered = df.copy()

if province:
    df_filtered = df_filtered[df_filtered['Province_Territory'].isin(province)]

if party:
    df_filtered = df_filtered[df_filtered['Political_Affiliation'].isin(party)]

if year:
    df_filtered['Year'] = pd.to_datetime(df_filtered['Date']).dt.year
    df_filtered = df_filtered[df_filtered['Year'].isin(year)]

# KPIs
total_votes = df_filtered['Votes'].sum()
total_elections = df_filtered['Parliament'].nunique()
top_party = df_filtered['Political_Affiliation'].value_counts().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("🗳️ Total Votes", f"{total_votes:,}")
col2.metric("🏛️ Total Elections", total_elections)
col3.metric("🎖️ Top Party", top_party)

# Simple Chart
st.subheader("Votes by Political Party")
party_votes = df_filtered.groupby('Political_Affiliation')['Votes'].sum().reset_index()
fig = px.bar(party_votes, x='Political_Affiliation', y='Votes', title="Votes by Party", color='Political_Affiliation')
st.plotly_chart(fig, use_container_width=True)
