# pages/4_Party_Spectrum.py

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page Title
# -------------------------------
st.title("🧭 Political Spectrum")
st.caption("Visualizing the ideological positioning of Canadian political parties across time.")

# -------------------------------
# Define political positions over time
# -------------------------------

# This is a manually curated mapping — you can expand as needed
party_positions = {
    2011: [
        {'Party': 'Conservative Party', 'Economic': 0.6, 'Social': 0.5, 'Color': 'blue'},
        {'Party': 'Liberal Party',       'Economic': 0.2, 'Social': -0.3, 'Color': 'red'},
        {'Party': 'New Democratic Party','Economic': -0.6,'Social': -0.6, 'Color': 'orange'},
        {'Party': 'Green Party',         'Economic': -0.4,'Social': -0.4, 'Color': 'green'},
        {'Party': 'Bloc Québécois',      'Economic': -0.3,'Social': -0.1, 'Color': 'darkgreen'},
        {'Party': 'People\'s Party',     'Economic': 0.8, 'Social': 0.7, 'Color': 'purple'}
    ],
    # You can expand this with other years
    2006: [
        {'Party': 'Conservative Party', 'Economic': 0.5, 'Social': 0.4, 'Color': 'blue'},
        {'Party': 'Liberal Party',       'Economic': 0.1, 'Social': -0.2, 'Color': 'red'},
        {'Party': 'New Democratic Party','Economic': -0.5,'Social': -0.5, 'Color': 'orange'},
        {'Party': 'Bloc Québécois',      'Economic': -0.3,'Social': -0.2, 'Color': 'darkgreen'}
    ],
}

# Available years
available_years = sorted(party_positions.keys(), reverse=True)

# -------------------------------
# Select Year
# -------------------------------
selected_year = st.selectbox("Select Election Year", available_years)

# Extract data for selected year
data = pd.DataFrame(party_positions[selected_year])

# -------------------------------
# Plot
# -------------------------------
fig = px.scatter(
    data, x='Economic', y='Social', text='Party',
    title=f"Political Spectrum – {selected_year}",
    labels={'Economic': 'Economic: Left ↔ Right', 'Social': 'Social: Libertarian ↔ Authoritarian'},
    color='Party', color_discrete_map={p['Party']: p['Color'] for p in data.to_dict('records')},
    width=700, height=600
)

fig.update_traces(marker=dict(size=12), textposition='top center')
fig.update_layout(
    xaxis=dict(range=[-1, 1], zeroline=True, zerolinewidth=2),
    yaxis=dict(range=[-1, 1], zeroline=True, zerolinewidth=2),
    showlegend=False
)

# Display plot
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Party Position Table
# -------------------------------
st.subheader("Party Positions in 2D Space")
st.dataframe(data[['Party', 'Economic', 'Social']], use_container_width=True)

# -------------------------------
# Footer
# -------------------------------
st.caption("Ideological positions are approximated based on public platforms and politicalcompass.org references. Subject to refinement.")
