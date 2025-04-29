# pages/1_Home.py

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('data/Election_Data.csv', encoding='latin1')
    df.columns = df.columns.str.strip()

    # Ensure Year, Month, Day are numeric
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
    df['Day'] = pd.to_numeric(df['Day'], errors='coerce')

    # Build ParsedDate from Y/M/D
    df['ParsedDate'] = pd.to_datetime(
        dict(year=df['Year'], month=df['Month'], day=df['Day']),
        errors='coerce'
    )

    df = df.dropna(subset=['ParsedDate'])
    df['Year'] = df['ParsedDate'].dt.year.astype(int)
    return df

df = load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔍 Filter Overview")

selected_provinces = st.sidebar.multiselect(
    "Province/Territory",
    options=sorted(df['Province_Territory'].dropna().unique())
)

selected_parties = st.sidebar.multiselect(
    "Political Affiliation",
    options=sorted(df['Political_Affiliation'].dropna().unique())
)

selected_years = st.sidebar.multiselect(
    "Election Year",
    options=sorted(df['Year'].dropna().unique())
)

# -------------------------------
# Apply Filters
# -------------------------------
df_filtered = df.copy()
if selected_provinces:
    df_filtered = df_filtered[df_filtered['Province_Territory'].isin(selected_provinces)]
if selected_parties:
    df_filtered = df_filtered[df_filtered['Political_Affiliation'].isin(selected_parties)]
if selected_years:
    df_filtered = df_filtered[df_filtered['Year'].isin(selected_years)]

# -------------------------------
# Page Title & Description
# -------------------------------
st.title("🇨🇦 Canadian Election Dashboard")
st.caption("A comprehensive look at Canada's federal election results — past, present, and predictive.")
st.markdown("""
Welcome to **Data Canada Votes**, a dynamic dashboard designed to explore Canada's electoral history.  
Use the sidebar to filter elections by Province, Party, and Year.
""")

st.divider()

# -------------------------------
# Key Metrics
# -------------------------------
st.header("📊 Election Overview at a Glance")

total_votes = df_filtered['Votes'].sum()
total_elections = df_filtered['Parliament'].nunique()
top_party = df_filtered['Political_Affiliation'].value_counts().idxmax() if not df_filtered.empty else "N/A"

col1, col2, col3 = st.columns(3)
col1.metric("🗳️ Total Votes Recorded", f"{total_votes:,}")
col2.metric("🏛️ Parliaments Covered", total_elections)
col3.metric("🎖️ Most Represented Party", top_party)

st.divider()

# -------------------------------
# Data Sample
# -------------------------------
st.header("📂 Sample of Election Data")
st.dataframe(df_filtered.head(10), use_container_width=True)
st.caption("Showing 10 rows. Use filters to explore more.")

st.divider()

# -------------------------------
# Party Votes Chart
# -------------------------------
st.subheader("Votes by Political Party")

if not df_filtered.empty:
    party_votes = df_filtered.groupby('Political_Affiliation')['Votes'].sum().reset_index()
    fig_party = px.bar(party_votes, x='Political_Affiliation', y='Votes',
                       title="Votes by Party", color='Political_Affiliation')
    st.plotly_chart(fig_party, use_container_width=True)
else:
    st.info("No data available for the selected filters.")

st.divider()

# -------------------------------
# Footer
# -------------------------------
st.caption("Built with ❤️ by Data Canada Votes | Powered by Streamlit")
