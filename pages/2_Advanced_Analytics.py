# pages/2_Advanced_Analytics.py

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import calendar

# -------------------------------
# Load data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('data/Election_Data.csv', encoding='latin1')
    df.columns = df.columns.str.strip()

    # Parse dates
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
    df['Day'] = pd.to_numeric(df['Day'], errors='coerce')
    df['Date'] = pd.to_datetime(dict(year=df['Year'], month=df['Month'], day=df['Day']), errors='coerce')
    df['Weekday'] = df['Date'].dt.day_name()

    # Filter out rows with missing key fields
    df = df.dropna(subset=['Year', 'Province_Territory', 'Election_Type', 'Parliament', 'Constituency', 'Votes'])
    df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce').fillna(0).astype(int)
    return df

df = load_data()

# -------------------------------
# Page Configuration
# -------------------------------
st.title("📊 Advanced Electoral Analytics")
st.caption("Deep-dive into Canada's federal election trends, party dynamics, and historical outcomes.")

# Filters
available_types = sorted(df['Election_Type'].dropna().unique())
default_type = 'General' if 'General' in available_types else available_types[0]
selected_type = st.selectbox("Filter by Election Type:", available_types, index=available_types.index(default_type))

available_parties = sorted(df['Political_Affiliation'].dropna().unique())
selected_parties = st.multiselect("Filter by Political Party:", available_parties, default=available_parties)

available_constituencies = sorted(df['Constituency'].dropna().unique())
selected_constituencies = st.multiselect("Filter by Constituency:", available_constituencies, default=available_constituencies)

# Apply filters
df = df[df['Election_Type'] == selected_type]
df = df[df['Political_Affiliation'].isin(selected_parties)]
df = df[df['Constituency'].isin(selected_constituencies)]

# -------------------------------
# Turnout and Participation Over Time
# -------------------------------
st.header("📈 Turnout and Participation Over Time")
turnout = df.groupby('Year').agg({
    'Votes': 'sum',
    'Constituency': 'nunique',
    'Province_Territory': 'nunique'
}).rename(columns={
    'Votes': 'Total Votes',
    'Constituency': 'Total Ridings',
    'Province_Territory': 'Provinces Participating'
}).reset_index()

fig_turnout = px.line(turnout, x='Year', y='Total Votes', markers=True, title='Total Votes Cast Over Time')
st.plotly_chart(fig_turnout, use_container_width=True)

# -------------------------------
# Votes by Province Over Time
# -------------------------------
st.header("🗺️ Vote Totals by Province")
prov_vote = df.groupby(['Year', 'Province_Territory'])['Votes'].sum().reset_index()
fig_prov = px.line(prov_vote, x='Year', y='Votes', color='Province_Territory', title="Votes by Province")
st.plotly_chart(fig_prov, use_container_width=True)

# -------------------------------
# Vote Share by Party
# -------------------------------
st.header("🧮 Party Vote Share Over Time")
party_share = df.groupby(['Year', 'Political_Affiliation'])['Votes'].sum().reset_index()
total_by_year = party_share.groupby('Year')['Votes'].sum().reset_index().rename(columns={'Votes': 'YearTotal'})
party_share = party_share.merge(total_by_year, on='Year')
party_share['Vote Share %'] = (party_share['Votes'] / party_share['YearTotal']) * 100

fig_share = px.area(party_share, x='Year', y='Vote Share %', color='Political_Affiliation', title="Party Vote Share Over Time")
st.plotly_chart(fig_share, use_container_width=True)

# -------------------------------
# Winning Margins
# -------------------------------
st.header("📏 Average Winning Margins")

margins = df.groupby(['Year', 'Province_Territory', 'Constituency']).apply(
    lambda x: x.sort_values('Votes', ascending=False).head(2)
).reset_index(drop=True)

margin_calc = margins.groupby(['Year', 'Province_Territory', 'Constituency'])['Votes'].apply(lambda x: x.iloc[0] - x.iloc[1] if len(x) > 1 else 0).reset_index(name='Winning Margin')
fig_margin = px.box(margin_calc, x='Year', y='Winning Margin', title="Distribution of Winning Margins")
st.plotly_chart(fig_margin, use_container_width=True)

# -------------------------------
# Close Races
# -------------------------------
st.header("📌 Close Races (<5% Margin)")

close_races = df.groupby(['Year', 'Constituency']).apply(lambda x: x.sort_values('Votes', ascending=False).head(2)).reset_index(drop=True)
close_races['Vote Diff'] = close_races.groupby(['Year', 'Constituency'])['Votes'].diff().abs()
close_races['Total Votes'] = close_races.groupby(['Year', 'Constituency'])['Votes'].transform('sum')
close_races['Margin %'] = (close_races['Vote Diff'] / close_races['Total Votes']) * 100

close_summary = close_races[(close_races['Margin %'] < 5) & (close_races['Margin %'].notna())]
st.dataframe(close_summary[['Year', 'Constituency', 'Political_Affiliation', 'Votes', 'Margin %']].sort_values('Margin %'), use_container_width=True)

# -------------------------------
# Spoiler Candidates
# -------------------------------
st.header("🔻 Spoiler Effect: Strong 3rd Place Candidates")

spoilers = df.groupby(['Year', 'Constituency']).apply(lambda x: x.sort_values('Votes', ascending=False).head(3)).reset_index(drop=True)
spoilers['Rank'] = spoilers.groupby(['Year', 'Constituency'])['Votes'].rank(ascending=False, method='first')
thirds = spoilers[spoilers['Rank'] == 3]
thirds = thirds[thirds['Votes'] > 0]

fig_third = px.histogram(thirds, x='Votes', nbins=30, title="Votes Received by 3rd Place Candidates")
st.plotly_chart(fig_third, use_container_width=True)

# -------------------------------
# Statistical Summary
# -------------------------------
st.header("📋 Statistical Summary Table")

summary = df.groupby('Year').agg(
    Total_Votes=('Votes', 'sum'),
    Unique_Ridings=('Constituency', 'nunique'),
    Parties=('Political_Affiliation', 'nunique'),
    Avg_Candidates_Per_Riding=('Candidate', lambda x: round(len(x) / x.nunique(), 2))
).reset_index()
st.dataframe(summary, use_container_width=True)

# -------------------------------
# 🗓️ Temporal Election Patterns
# -------------------------------
st.header("🗓️ Temporal Election Patterns")

month_party = df[df['Result'].str.contains("Elected", na=False)].groupby(['Month', 'Political_Affiliation']).size().reset_index(name='Wins')
fig_month = px.bar(month_party, x='Month', y='Wins', color='Political_Affiliation', title="Wins by Party and Month")
st.plotly_chart(fig_month, use_container_width=True)

day_party = df[df['Result'].str.contains("Elected", na=False)].groupby(['Day', 'Political_Affiliation']).size().reset_index(name='Wins')
fig_day = px.bar(day_party, x='Day', y='Wins', color='Political_Affiliation', title="Wins by Party and Day")
st.plotly_chart(fig_day, use_container_width=True)

weekday_party = df[df['Result'].str.contains("Elected", na=False)].groupby(['Weekday', 'Political_Affiliation']).size().reset_index(name='Wins')
weekday_order = list(calendar.day_name)
fig_weekday = px.bar(weekday_party, x='Weekday', y='Wins', color='Political_Affiliation', category_orders={'Weekday': weekday_order}, title="Wins by Party and Weekday")
st.plotly_chart(fig_weekday, use_container_width=True)

# -------------------------------
# 🔁 Ridings with Consistent Party Wins
# -------------------------------
st.header("🔁 Ridings with Consistent Party Wins")
winner_df = df[df['Result'].str.contains("Elected", na=False)]
riding_dominance = winner_df.groupby(['Constituency', 'Political_Affiliation'])['Year'].nunique().reset_index(name='Win_Years')
top_ridings = riding_dominance.sort_values(['Constituency', 'Win_Years'], ascending=[True, False])
top_ridings = top_ridings.groupby('Constituency').head(1).sort_values('Win_Years', ascending=False).head(20)
st.dataframe(top_ridings, use_container_width=True)

# -------------------------------
# 🗺️ Riding Lifespan
# -------------------------------
st.header("🗺️ Riding Lifespan Map")
riding_years = df.groupby('Constituency')['Year'].agg(['min', 'max']).reset_index().rename(columns={'min': 'First Appearance', 'max': 'Last Appearance'})
st.dataframe(riding_years.sort_values('First Appearance'), use_container_width=True)

# -------------------------------
# 👔 Occupation vs Vote Share
# -------------------------------
st.header("👔 Occupation Influence on Vote Share")

# Calculate relative performance within each riding/year
df['Total_Riding_Votes'] = df.groupby(['Year', 'Constituency'])['Votes'].transform('sum')
df['Vote_Share'] = (df['Votes'] / df['Total_Riding_Votes']) * 100

occ_vote_share = df.groupby('Occupation')['Vote_Share'].mean().reset_index().dropna().sort_values('Vote_Share', ascending=False).head(15)
fig_occ_perf = px.bar(occ_vote_share, x='Vote_Share', y='Occupation', orientation='h', title="Avg Vote Share by Occupation")
st.plotly_chart(fig_occ_perf, use_container_width=True)

st.caption("All analyses above are filtered to the selected election type. Default is 'General'.")

# -------------------------------
# Footer
# -------------------------------
st.caption("Advanced analytics powered by Plotly and Streamlit • Data Canada Votes © 2025")

