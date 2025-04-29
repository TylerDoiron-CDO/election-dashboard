# pages/4_Party_Spectrum.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🧭 Canadian Political Spectrum")
st.caption("Visualizing ideological shifts of Canadian political parties from 2000 to present.")

# -------------------------------
# Manual ideological mapping (2000–2021)
# Economic: -1 (socialist) to +1 (capitalist)
# Social: -1 (libertarian) to +1 (authoritarian)
# -------------------------------

party_history = []

party_colors = {
    'Liberal Party': 'red',
    'Conservative Party': 'blue',
    'New Democratic Party': 'orange',
    'Green Party': 'green',
    'Bloc Québécois': 'darkgreen',
    'People\'s Party': 'purple'
}

years = [2000, 2004, 2006, 2008, 2011, 2015, 2019, 2021]

# Liberal Party
liberal_coords = [(0.3, 0.2), (0.25, 0.1), (0.2, 0.0), (0.15, -0.1), (0.2, -0.3), (0.15, -0.4), (0.2, -0.35), (0.25, -0.3)]
# Conservative Party
con_coords = [(0.5, 0.4), (0.55, 0.45), (0.6, 0.5), (0.65, 0.55), (0.65, 0.6), (0.6, 0.6), (0.7, 0.6), (0.65, 0.55)]
# NDP
ndp_coords = [(-0.6, -0.6)] * len(years)
# Green Party
green_coords = [(-0.4, -0.4)] * len(years)
# Bloc
bloc_coords = [(-0.3, -0.1)] * len(years)
# PPC (only from 2019)
ppc_coords = [(0.85, 0.8), (0.85, 0.8)]

for i, year in enumerate(years):
    party_history.append({'Year': year, 'Party': 'Liberal Party', 'Economic': liberal_coords[i][0], 'Social': liberal_coords[i][1], 'Color': party_colors['Liberal Party']})
    party_history.append({'Year': year, 'Party': 'Conservative Party', 'Economic': con_coords[i][0], 'Social': con_coords[i][1], 'Color': party_colors['Conservative Party']})
    party_history.append({'Year': year, 'Party': 'New Democratic Party', 'Economic': ndp_coords[i][0], 'Social': ndp_coords[i][1], 'Color': party_colors['New Democratic Party']})
    party_history.append({'Year': year, 'Party': 'Green Party', 'Economic': green_coords[i][0], 'Social': green_coords[i][1], 'Color': party_colors['Green Party']})
    party_history.append({'Year': year, 'Party': 'Bloc Québécois', 'Economic': bloc_coords[i][0], 'Social': bloc_coords[i][1], 'Color': party_colors['Bloc Québécois']})
    if year >= 2019:
        party_history.append({'Year': year, 'Party': 'People\'s Party', 'Economic': ppc_coords[year - 2019][0], 'Social': ppc_coords[year - 2019][1], 'Color': party_colors['People\'s Party']})

df = pd.DataFrame(party_history)

# -------------------------------
# Year Selection
# -------------------------------
selected_year = st.selectbox("Select Election Year", sorted(df['Year'].unique(), reverse=True))

df_year = df[df['Year'] == selected_year]

# -------------------------------
# Spectrum Plot
# -------------------------------
fig = px.scatter(
    df_year,
    x='Economic',
    y='Social',
    text='Party',
    color='Party',
    color_discrete_map=party_colors,
    title=f"Canadian Political Spectrum – {selected_year}",
    labels={'Economic': 'Left ← Economic → Right', 'Social': 'Libertarian ↑  |  ↓ Authoritarian'},
    range_x=[-1, 1],
    range_y=[-1, 1],
    height=600
)

fig.update_traces(marker=dict(size=14), textposition='top center')
fig.update_layout(
    xaxis=dict(showgrid=True, zeroline=True, zerolinewidth=2),
    yaxis=dict(showgrid=True, zeroline=True, zerolinewidth=2),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Table of Positions
# -------------------------------
st.subheader("Party Coordinates (for selected year)")
st.dataframe(df_year[['Party', 'Economic', 'Social']], use_container_width=True)

# -------------------------------
# Footer
# -------------------------------
st.caption("Party positions estimated using public platforms, historical policy analysis, and PoliticalCompass references. This model simplifies ideology and is meant for educational purposes.")
