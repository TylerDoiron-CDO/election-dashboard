# pages/4_Party_Spectrum.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🧭 Canadian Political Spectrum (2000–2025)")
st.caption("Explore the ideological positioning and historical dispersion of Canadian political parties.")

# -------------------------------
# Define ideological coordinates manually (2000–2025)
# -------------------------------

years = [2000, 2004, 2006, 2008, 2011, 2015, 2019, 2021, 2025]

party_colors = {
    'Liberal Party': 'red',
    'Conservative Party': 'blue',
    'New Democratic Party': 'orange',
    'Green Party': 'green',
    'Bloc Québécois': 'darkgreen',
    'People\'s Party': 'purple'
}

party_history = []

# Liberal Party ideological drift
liberal_coords = [(0.3, 0.2), (0.25, 0.1), (0.2, 0.0), (0.15, -0.1), (0.2, -0.3), (0.15, -0.4), (0.2, -0.35), (0.25, -0.3), (0.2, -0.25)]
# Conservative Party
con_coords = [(0.5, 0.4), (0.55, 0.45), (0.6, 0.5), (0.65, 0.55), (0.65, 0.6), (0.6, 0.6), (0.7, 0.6), (0.65, 0.55), (0.6, 0.5)]
# NDP
ndp_coords = [(-0.6, -0.6)] * len(years)
# Green Party
green_coords = [(-0.4, -0.4)] * len(years)
# Bloc
bloc_coords = [(-0.3, -0.1)] * len(years)
# PPC (only from 2019)
ppc_years = [2019, 2021, 2025]
ppc_coords = [(0.85, 0.8), (0.85, 0.8), (0.85, 0.8)]

for i, year in enumerate(years):
    party_history.append({'Year': year, 'Party': 'Liberal Party', 'Economic': liberal_coords[i][0], 'Social': liberal_coords[i][1], 'Color': party_colors['Liberal Party']})
    party_history.append({'Year': year, 'Party': 'Conservative Party', 'Economic': con_coords[i][0], 'Social': con_coords[i][1], 'Color': party_colors['Conservative Party']})
    party_history.append({'Year': year, 'Party': 'New Democratic Party', 'Economic': ndp_coords[i][0], 'Social': ndp_coords[i][1], 'Color': party_colors['New Democratic Party']})
    party_history.append({'Year': year, 'Party': 'Green Party', 'Economic': green_coords[i][0], 'Social': green_coords[i][1], 'Color': party_colors['Green Party']})
    party_history.append({'Year': year, 'Party': 'Bloc Québécois', 'Economic': bloc_coords[i][0], 'Social': bloc_coords[i][1], 'Color': party_colors['Bloc Québécois']})
    if year in ppc_years:
        j = ppc_years.index(year)
        party_history.append({
            'Year': year,
            'Party': 'People\'s Party',
            'Economic': ppc_coords[j][0],
            'Social': ppc_coords[j][1],
            'Color': party_colors['People\'s Party']
        })

df = pd.DataFrame(party_history)

# -------------------------------
# Party Spectrum Scatter Plot (Year Selector)
# -------------------------------

st.subheader("🟢 Political Spectrum – Party Positions by Year")

selected_year = st.selectbox("Select Election Year", sorted(df['Year'].unique(), reverse=True))

df_year = df[df['Year'] == selected_year]

fig_scatter = px.scatter(
    df_year,
    x='Economic',
    y='Social',
    text='Party',
    color='Party',
    color_discrete_map=party_colors,
    title=f"Political Spectrum – {selected_year}",
    labels={
        'Economic': 'Economic Axis: Left ← → Right',
        'Social': 'Social Axis: Libertarian ↑  |  ↓ Authoritarian'
    },
    range_x=[-1, 1],
    range_y=[-1, 1],
    height=600
)

fig_scatter.update_traces(marker=dict(size=14), textposition='top center')
fig_scatter.update_layout(
    xaxis=dict(showgrid=True, zeroline=True, zerolinewidth=2),
    yaxis=dict(showgrid=True, zeroline=True, zerolinewidth=2),
    showlegend=False
)

st.plotly_chart(fig_scatter, use_container_width=True)

# -------------------------------
# Matrix-Style Heatmaps (Like JPMorgan Chart)
# -------------------------------
st.subheader("🧮 Tabular Ideological Heatmaps")

pivot_econ = df.pivot(index='Party', columns='Year', values='Economic')
pivot_soc = df.pivot(index='Party', columns='Year', values='Social')

st.markdown("#### 🟢 Economic Ideology (Left → Right)")

st.dataframe(
    pivot_econ.style.background_gradient(
        cmap='RdYlGn', axis=1, vmin=-1, vmax=1
    ).format("{:.2f}"),
    use_container_width=True
)

st.markdown("#### 🔵 Social Ideology (Libertarian → Authoritarian)")

st.dataframe(
    pivot_soc.style.background_gradient(
        cmap='RdYlGn', axis=1, vmin=-1, vmax=1
    ).format("{:.2f}"),
    use_container_width=True
)

# -------------------------------
# Optional Table
# -------------------------------
with st.expander("See Raw Party Data"):
    st.dataframe(df[['Year', 'Party', 'Economic', 'Social']], use_container_width=True)

# -------------------------------
# Footer
# -------------------------------
st.caption("Ideological positions are estimates based on public platforms and PoliticalCompass-style references. Visuals designed for exploration and analysis.")
