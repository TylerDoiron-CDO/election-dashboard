# generate_election_map.py

import geopandas as gpd
import pandas as pd
import folium
from folium.plugins import TimeSliderChoropleth
import json

# -------------------------------
# Load GeoSpatial Riding Boundaries
# -------------------------------
# Downloaded or fetched Canadian riding boundaries (simplified for example)
riding_geojson_path = "data/canada_ridings_latest.geojson"  # Replace this with your full ridings file
riding_gdf = gpd.read_file(riding_geojson_path)

# -------------------------------
# Load Historical Election Data
# -------------------------------
election_df = pd.read_csv("data/Election_Data.csv", encoding='latin1')

# Clean up
election_df.columns = election_df.columns.str.strip()
election_df['Year'] = pd.to_numeric(election_df['Year'], errors='coerce')
election_df = election_df.dropna(subset=['Year', 'Province_Territory', 'Political_Affiliation', 'Constituency', 'Votes'])
election_df['Votes'] = pd.to_numeric(election_df['Votes'], errors='coerce').fillna(0).astype(int)
election_df['Result'] = election_df['Result'].str.strip()

# Only keep Elected candidates
election_winners = election_df[election_df['Result'].str.contains("Elected", na=False)]

# -------------------------------
# Prepare Data for Geo Join
# -------------------------------
# Normalize riding names
riding_gdf['Constituency'] = riding_gdf['ENGLISH_NAME'].str.strip().str.lower()
election_winners['Constituency'] = election_winners['Constituency'].str.strip().str.lower()

# Join election results to ridings
riding_gdf = riding_gdf.merge(
    election_winners[['Year', 'Constituency', 'Political_Affiliation', 'Candidate', 'Gender', 'Occupation', 'Votes']],
    how='left',
    on='Constituency'
)

# -------------------------------
# Assign Party Colors
# -------------------------------
party_colors = {
    'Liberal Party': '#E41A1C',
    'Conservative Party': '#377EB8',
    'New Democratic Party': '#FF7F00',
    'Bloc Québécois': '#4DAF4A',
    'Green Party': '#984EA3',
    'People\'s Party': '#984EA3',
    'Independent': '#999999',
    'Unknown': '#CCCCCC'
}

def get_party_color(party):
    return party_colors.get(party, "#BBBBBB")

riding_gdf['color'] = riding_gdf['Political_Affiliation'].apply(get_party_color)

# -------------------------------
# Create Folium Map
# -------------------------------
canada_center = [56.1304, -106.3468]
m = folium.Map(location=canada_center, zoom_start=4, tiles='CartoDB positron')

# -------------------------------
# TimeSlider Choropleth Setup
# -------------------------------
styledict = {}

for idx, row in riding_gdf.iterrows():
    if pd.isna(row['Year']):
        continue
    
    feature_id = str(idx)
    year = int(row['Year'])
    
    if feature_id not in styledict:
        styledict[feature_id] = {}
    
    styledict[feature_id][str(year)] = {
        'color': row['color'],
        'opacity': 0.7,
        'fillColor': row['color'],
        'fillOpacity': 0.6
    }

# Create Popup Content
def create_popup(row):
    return f"""
    <b>Riding:</b> {row['Constituency'].title()}<br>
    <b>Year:</b> {int(row['Year'])}<br>
    <b>Winning Party:</b> {row['Political_Affiliation']}<br>
    <b>Candidate:</b> {row['Candidate']}<br>
    <b>Votes:</b> {row['Votes']}<br>
    <b>Gender:</b> {row['Gender']}<br>
    <b>Occupation:</b> {row['Occupation']}<br>
    """

# Add the riding GeoJson
riding_geojson = folium.GeoJson(
    data=json.loads(riding_gdf.to_json()),
    style_function=lambda x: {
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.1
    },
    highlight_function=lambda x: {
        'weight': 3,
        'color': 'yellow'
    },
    tooltip=folium.features.GeoJsonTooltip(
        fields=['Constituency'],
        aliases=['Constituency:']
    ),
    popup=folium.GeoJsonPopup(
        fields=['Constituency', 'Political_Affiliation', 'Candidate', 'Votes', 'Gender', 'Occupation'],
        aliases=["Riding", "Party", "Candidate", "Votes", "Gender", "Occupation"],
        labels=True,
        style="background-color: white;"
    )
).add_to(m)

# TimeSlider
TimeSliderChoropleth(
    data=json.loads(riding_gdf.to_json()),
    styledict=styledict
).add_to(m)

# -------------------------------
# Save Map
# -------------------------------
m.save("outputs/canadian_election_historical_map.html")
print("✅ Map created successfully: outputs/canadian_election_historical_map.html")

