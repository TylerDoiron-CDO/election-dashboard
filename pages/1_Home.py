# pages/1_Home.py

import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('data/Election_Data.csv', encoding='latin1')
    df.columns = df.columns.str.strip()

    # Parse numeric components of date
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
    df['Day'] = pd.to_numeric(df['Day'], errors='coerce')

    # Build ParsedDate from components
    df['ParsedDate'] = pd.to_datetime(dict(year=df['Year'], month=df['Month'], day=df['Day']), errors='coerce')
    df = df.dropna(subset=['ParsedDate'])
    df['Year'] = df['ParsedDate'].dt.year.astype(int)

    return df

# Load and prepare data
df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Overview")

selected_provinces = st.sidebar.multiselect("Province/Territory", sorted(df['Province_Territory'].dropna().unique()))
selected_parties = st.sidebar.multiselect("Political Affiliation", sorted(df['Political_Affiliation'].dropna().unique()))
selected_years = st.sidebar.multiselect("Election Year", sorted(df['Year'].dropna().unique()))

df_filtered = df.copy()
if selected_provinces:
    df_filtered = df_filtered[df_filtered['Province_Territory'].isin(selected_provinces)]
if selected_parties:
    df_filtered = df_filtered[df_filtered['Political_Affiliation'].isin(selected_parties)]
if selected_years:
    df_filtered = df_filtered[df_filtered['Year'].isin(selected_years)]

# ---------------------------------------
# Page Title & Intro
# ---------------------------------------
st.title("🇨🇦 Canadian Election Dashboard")
st.caption("A comprehensive look at Canada's federal election results — past, present, and predictive.")
st.markdown("""
Welcome to **Data Canada Votes**, an interactive dashboard exploring Canadian federal elections.  
Use the sidebar to filter by **Province**, **Party**, and **Election Year**.
""")
st.divider()

# ---------------------------------------
# KPIs
# ---------------------------------------
st.header("📊 Election Overview at a Glance")

total_votes = df_filtered['Votes'].sum()
total_parliaments = df_filtered['Parliament'].nunique()
top_party = df_filtered['Political_Affiliation'].value_counts().idxmax() if not df_filtered.empty else "N/A"
unique_parties = df_filtered['Political_Affiliation'].nunique()
avg_votes_per_constituency = int(df_filtered.groupby('Constituency')['Votes'].sum().mean()) if not df_filtered.empty else 0

col1, col2, col3 = st.columns(3)
col1.metric("🗳️ Total Votes", f"{total_votes:,}")
col2.metric("🏛️ Parliaments", total_parliaments)
col3.metric("🎖️ Top Party", top_party)

col4, col5 = st.columns(2)
col4.metric("🧾 Unique Parties", unique_parties)
col5.metric("📈 Avg Votes per Riding", f"{avg_votes_per_constituency:,}")

st.divider()

# ---------------------------------------
# Sample of the Data
# ---------------------------------------
st.header("📂 Sample of Election Data")
st.dataframe(df_filtered.head(10), use_container_width=True)
st.caption("Showing 10 rows. Use filters to explore more.")
st.divider()

# ---------------------------------------
# 🥇 Winning Party by Riding and Parliament
# ---------------------------------------
st.header("🥇 Winning Party by Riding and Parliament")

# Filter to elected candidates only
winners = df_filtered[df_filtered['Result'].str.contains("Elected", na=False)]

# Sum votes by Constituency within each Parliament & Province
summary = (
    winners.groupby(['Parliament', 'Province_Territory', 'Constituency', 'Political_Affiliation'])['Votes']
    .sum()
    .reset_index()
)

# Rank within each riding
summary['Rank'] = summary.groupby(['Parliament', 'Province_Territory', 'Constituency'])['Votes'] \
                         .rank(ascending=False, method='first')

# Keep only top-ranked (winning) party per riding
winners_only = summary[summary['Rank'] == 1].drop(columns='Rank')

# Total votes per riding (regardless of party)
total_votes = (
    df_filtered.groupby(['Parliament', 'Province_Territory', 'Constituency'])['Votes']
    .sum()
    .reset_index()
    .rename(columns={'Votes': 'TotalVotes'})
)

# Merge to calculate vote share
winners_only = winners_only.merge(total_votes, on=['Parliament', 'Province_Territory', 'Constituency'])
winners_only['Vote Share (%)'] = (winners_only['Votes'] / winners_only['TotalVotes']) * 100
winners_only['Vote Share (%)'] = winners_only['Vote Share (%)'].round(2)

# Rename and reorder columns
winners_only = winners_only.rename(columns={
    'Province_Territory': 'Province',
    'Constituency': 'Constituency',
    'Political_Affiliation': 'Winning Party',
    'Votes': 'Votes Won'
})

winners_only = winners_only[['Parliament', 'Province', 'Constituency', 'Winning Party', 'Votes Won', 'Vote Share (%)']]

# Display
st.dataframe(winners_only.sort_values(['Parliament', 'Province', 'Constituency']), use_container_width=True)

# ---------------------------------------
# Political Party Spectrum
# ---------------------------------------
st.header("🧭 Political Spectrum of Canadian Parties")

# Manual mapping: political orientation (subject to refinement)
party_positions = pd.DataFrame({
    'Party': [
        'Liberal', 'Conservative', 'NDP', 'Bloc Québécois', 'Green Party', 
        'People\'s Party', 'Progressive Conservative', 'Reform', 'Social Credit'
    ],
    'Economic': [-0.2, 0.8, -0.7, -0.3, -0.6, 0.9, 0.6, 0.7, 0.4],  # -1 = socialist, +1 = capitalist
    'Social': [-0.3, 0.5, -0.8, -0.2, -0.7, 0.8, 0.4, 0.6, 0.2]     # -1 = libertarian, +1 = authoritarian
})

fig_spectrum = px.scatter(
    party_positions, x='Economic', y='Social', text='Party',
    title="Canadian Political Spectrum (2D)", labels={'Economic': 'Left ↔ Right', 'Social': 'Libertarian ↔ Authoritarian'},
    range_x=[-1, 1], range_y=[-1, 1], width=700, height=500
)

fig_spectrum.update_traces(marker=dict(size=12, color='blue'), textposition='top center')
fig_spectrum.update_layout(xaxis_title="Economic (Left to Right)", yaxis_title="Social (Libertarian to Authoritarian)")

st.plotly_chart(fig_spectrum, use_container_width=True)

st.caption("Note: Positioning based on general policy trends and public perception. Subject to refinement.")

st.divider()

# -------------------------------
# 🧑‍💼 Most Common Occupations (Elected vs Not Elected)
# -------------------------------
st.header("💼 Top 10 Candidate Occupations")

# Clean and categorize
df_filtered['Result_Clean'] = df_filtered['Result'].fillna("Unknown").str.contains("Elected", case=False)

# Group and count
occ_counts = (
    df_filtered.groupby(['Result_Clean', 'Occupation'])
    .size()
    .reset_index(name='Count')
)

# Get top 10 for each group
top_occ = (
    occ_counts.groupby('Result_Clean')
    .apply(lambda x: x.sort_values('Count', ascending=False).head(10))
    .reset_index(drop=True)
)

fig_occ = px.bar(
    top_occ,
    x='Count',
    y='Occupation',
    color='Result_Clean',
    barmode='group',
    orientation='h',
    title="Top 10 Occupations: Elected vs Non-Elected Candidates",
    labels={'Result_Clean': 'Elected?', 'Count': 'Number of Candidates'}
)

fig_occ.update_layout(yaxis=dict(categoryorder='total ascending'))
st.plotly_chart(fig_occ, use_container_width=True)

st.divider()

# -------------------------------
# 🔤 Most Common Candidate Names (First and Last)
# -------------------------------
st.header("🔤 Most Common Candidate Names")

# First Names
first_names = (
    df_filtered['First_Name']
    .dropna()
    .str.title()
    .value_counts()
    .head(10)
    .reset_index()
)
first_names.columns = ['First Name', 'Count']

fig_first = px.bar(
    first_names,
    x='Count',
    y='First Name',
    orientation='h',
    title="Top 10 First Names Among Candidates"
)
fig_first.update_layout(yaxis=dict(categoryorder='total ascending'))

# Last Names
last_names = (
    df_filtered['Last_Name']
    .dropna()
    .str.title()
    .value_counts()
    .head(10)
    .reset_index()
)
last_names.columns = ['Last Name', 'Count']

fig_last = px.bar(
    last_names,
    x='Count',
    y='Last Name',
    orientation='h',
    title="Top 10 Last Names Among Candidates"
)
fig_last.update_layout(yaxis=dict(categoryorder='total ascending'))

# Display side-by-side
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_first, use_container_width=True)
with col2:
    st.plotly_chart(fig_last, use_container_width=True)

st.divider()


st.caption("Built with ❤️ by Data Canada Votes | Powered by Streamlit")
