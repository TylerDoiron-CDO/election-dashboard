# pages/2_Advanced_Analytics.py

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Load and prepare data
# -------------------------------
@st.cache_data
def load_data():
    import pandas as pd

    df = pd.read_csv('data/Election_Data.csv', encoding='latin1')
    df.columns = df.columns.str.strip()

    # Ensure Year, Month, Day are numeric
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
    df['Day'] = pd.to_numeric(df['Day'], errors='coerce')

    # Create ParsedDate from components
    df['ParsedDate'] = pd.to_datetime(
        dict(year=df['Year'], month=df['Month'], day=df['Day']),
        errors='coerce'
    )

    # Drop rows with invalid or missing dates
    df = df.dropna(subset=['ParsedDate'])
    df['Year'] = df['ParsedDate'].dt.year.astype(int)

    return df

    
df = load_data()

# -------------------------------
# Page title & description
# -------------------------------
st.title("📈 Advanced Analytics")
st.caption("Explore trends, patterns, and key insights from Canada's federal election history.")

st.divider()

# -------------------------------
# Optional Filter Panel
# -------------------------------
with st.expander("🔍 Filter Data"):
    col1, col2, col3 = st.columns(3)

    selected_provinces = col1.multiselect(
        "Province/Territory",
        options=sorted(df['Province_Territory'].dropna().unique()),
        default=None
    )

    selected_parties = col2.multiselect(
        "Political Affiliation",
        options=sorted(df['Political_Affiliation'].dropna().unique()),
        default=None
    )

    selected_genders = col3.multiselect(
        "Candidate Gender",
        options=sorted(df['Gender'].dropna().unique()),
        default=None
    )

# Apply filters
filtered_df = df.copy()
if selected_provinces:
    filtered_df = filtered_df[filtered_df['Province_Territory'].isin(selected_provinces)]
if selected_parties:
    filtered_df = filtered_df[filtered_df['Political_Affiliation'].isin(selected_parties)]
if selected_genders:
    filtered_df = filtered_df[filtered_df['Gender'].isin(selected_genders)]

# -------------------------------
# 🕰️ Voting Trends Over Time
# -------------------------------
st.header("🕰️ Voting Trends Over Time")

trend = filtered_df[filtered_df['Votes'] > 0].groupby('Year')['Votes'].sum().reset_index()
if not trend.empty:
    fig_trend = px.line(trend, x='Year', y='Votes', markers=True,
                        title="Total Votes Recorded in Election Years")
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.info("No data available for the selected filters.")

st.divider()

# -------------------------------
# 🏛️ Party Dominance Over Time
# -------------------------------
st.header("🏛️ Party Dominance Across Elections")

party_wins = filtered_df[filtered_df['Result'].str.contains("Elected", na=False)]
party_trend = party_wins.groupby(['Year', 'Political_Affiliation']).size().reset_index(name='Seats')

if not party_trend.empty:
    fig_party = px.area(party_trend, x='Year', y='Seats', color='Political_Affiliation',
                        title="Seats Won by Political Party Over Time", groupnorm="percent")
    st.plotly_chart(fig_party, use_container_width=True)
else:
    st.info("No elected candidate data available for selected filters.")

st.divider()

# -------------------------------
# 👤 Gender Representation
# -------------------------------
st.header("👤 Gender Representation Over Time")

gender_trend = filtered_df.groupby(['Year', 'Gender']).size().reset_index(name='Count')
if not gender_trend.empty:
    fig_gender = px.area(gender_trend, x='Year', y='Count', color='Gender',
                         title="Candidate Gender Distribution by Year")
    st.plotly_chart(fig_gender, use_container_width=True)
else:
    st.info("No gender data available for selected filters.")

st.divider()

# -------------------------------
# 💼 Candidate Occupations
# -------------------------------
st.header("💼 Most Common Candidate Occupations")

occupation_counts = filtered_df['Occupation'].dropna().value_counts().reset_index()
occupation_counts.columns = ['Occupation', 'Count']
top_occupations = occupation_counts.head(10)

if not top_occupations.empty:
    fig_occ = px.bar(top_occupations, x='Count', y='Occupation', orientation='h',
                     title="Top 10 Candidate Occupations", color='Occupation')
    st.plotly_chart(fig_occ, use_container_width=True)
else:
    st.info("No occupation data available for selected filters.")

st.divider()

# -------------------------------
# 🗺️ Provincial Vote Totals
# -------------------------------
st.header("🗺️ Total Votes by Province")

province_votes = filtered_df.groupby('Province_Territory')['Votes'].sum().reset_index()
province_votes = province_votes[province_votes['Votes'] > 0]

if not province_votes.empty:
    fig_province = px.bar(province_votes, x='Votes', y='Province_Territory', orientation='h',
                          title="Total Votes by Province", color='Province_Territory')
    st.plotly_chart(fig_province, use_container_width=True)
else:
    st.info("No provincial vote data available for selected filters.")

st.divider()

# -------------------------------
# 🎯 Outcome Distribution
# -------------------------------
st.header("🎯 Election Outcomes")

outcomes = filtered_df['Result'].value_counts().reset_index()
outcomes.columns = ['Outcome', 'Count']

if not outcomes.empty:
    fig_outcome = px.pie(outcomes, names='Outcome', values='Count', hole=0.4,
                         title="Distribution of Election Outcomes")
    st.plotly_chart(fig_outcome, use_container_width=True)
else:
    st.info("No result data available for selected filters.")

st.divider()

# -------------------------------
# Footer
# -------------------------------
st.caption("Advanced analytics powered by Plotly and Streamlit • Data Canada Votes © 2025")
