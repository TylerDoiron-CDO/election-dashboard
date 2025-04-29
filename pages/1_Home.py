# pages/1_Home.py

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Load the election data
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv('data/Election_Data.csv', encoding='latin1')

df = load_data()
df['Year'] = pd.to_datetime(df['Date']).dt.year

# -------------------------------
# Header
# -------------------------------
st.title("🇨🇦 Canadian Election Dashboard")
st.caption("A comprehensive look at Canada's federal election results — past, present, and predictive.")

st.markdown("""
Welcome to **Data Canada Votes**, a dynamic dashboard designed to explore Canada's electoral history.  
Use the sidebar to filter elections by Province, Party, and Year, and navigate across different sections for deeper insights and predictions.
""")

st.divider()

# -------------------------------
# Key Metrics
# -------------------------------
st.header("📊 Election Overview at a Glance")

# Sidebar filters
province = st.sidebar.multiselect("Filter by Province/Territory:", options=df['Province_Territory'].unique())
party = st.sidebar.multiselect("Filter by Political Party:", options=df['Political_Affiliation'].unique())
year = st.sidebar.multiselect("Filter by Election Year:", options=sorted(df['Year'].unique()))

# Apply filters
df_filtered = df.copy()

if province:
    df_filtered = df_filtered[df_filtered['Province_Territory'].isin(province)]
if party:
    df_filtered = df_filtered[df_filtered['Political_Affiliation'].isin(party)]
if year:
    df_filtered = df_filtered[df_filtered['Year'].isin(year)]

# Metrics calculations
total_votes = df_filtered['Votes'].sum()
total_elections = df_filtered['Parliament'].nunique()
top_party = df_filtered['Political_Affiliation'].value_counts().idxmax()

# Metrics layout
col1, col2, col3 = st.columns(3)
col1.metric("🗳️ Total Votes Recorded", f"{total_votes:,}")
col2.metric("🏛️ Parliaments Covered", total_elections)
col3.metric("🎖️ Most Represented Party", top_party)

st.divider()

# -------------------------------
# Data Sample
# -------------------------------
st.header("📂 Sample of Election Data")

st.markdown("Here's a quick look at the dataset behind the dashboard:")

# Show small sample of the data
st.dataframe(df_filtered.head(10), use_container_width=True)

st.caption("Showing 10 rows. Full dataset available through dashboard filters.")

st.divider()

# -------------------------------
# How to Use This Dashboard
# -------------------------------
st.header("🧭 How to Explore the Dashboard")

st.markdown("""
- **Advanced Analytics**: Discover historical voting trends, gender dynamics, and party evolutions.
- **Predictive Models**: Forecast future election outcomes using real historical data.
- **Geospatial Mapping (Coming Soon!)**: Visualize voting patterns by electoral districts.

Use the sidebar to **filter by Province, Year, and Party** anytime.
""")

st.divider()

# -------------------------------
# Footer
# -------------------------------
st.caption("Built with ❤️ by Data Canada Votes | Powered by Streamlit")
