import geopandas as gpd
import folium
import pandas as pd
import os

# Create output directory
os.makedirs('data/maps', exist_ok=True)

# Load data
data = pd.read_csv(r"data/all_results.csv")
data["precinct"] = pd.to_numeric(data["precinct"])

edm_precincts = gpd.read_file(r"data/gs_data/edmonds_precincts.geojson")
edm_precincts["precinct"] = pd.to_numeric(edm_precincts["precinct"])
edm_precincts = edm_precincts.to_crs(epsg=4326)

"""county_precincts = gpd.read_file(r"data/gs_data/county_precincts.geojson")
county_precincts["precinct"] = pd.to_numeric(county_precincts["precinct"])
county_precincts = county_precincts.to_crs(epsg=4326)
print(county_precincts)"""
# Merge data with geometry - KEEP AS GEODATAFRAME
edm_data = gpd.GeoDataFrame(
    edm_precincts.merge(data, on="precinct", how="inner"),
    geometry='geometry',
    crs=edm_precincts.crs
)
"""edm_data = gpd.GeoDataFrame(
    county_precincts.merge(data, on="precinct", how="inner"),
    geometry='geometry',
    crs=county_precincts.crs)"""

# Function to determine winner for each precinct/contest
def get_precinct_winners(df):
    # Group by precinct and contest, find candidate with most votes
    winners = df.loc[df.groupby(['precinct', 'contest'])['votes'].idxmax()]
    return winners

# Get winners for each precinct/contest
winners_df = get_precinct_winners(edm_data)

# Create a color map for candidates
unique_candidates = edm_data['candidate'].unique()
colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'pink', 'brown']
candidate_colors = {candidate: colors[i % len(colors)] for i, candidate in enumerate(unique_candidates)}

# Get unique contests
contests = edm_data['contest'].unique()

# Create a map for each contest
for contest in contests:
    # Filter data for this contest
    contest_data = edm_data[edm_data['contest'] == contest]
    contest_winners = winners_df[winners_df['contest'] == contest]
    
    # Merge winners back with geometry - KEEP AS GEODATAFRAME
    contest_geo = gpd.GeoDataFrame(
        contest_winners[['precinct', 'name', 'geometry', 'candidate']].copy(),
        geometry='geometry',
        crs=edm_data.crs
    )
    
    # Get bounds
    bounds = contest_geo.total_bounds
    center_lat = (bounds[1] + bounds[3]) / 2
    center_lon = (bounds[0] + bounds[2]) / 2
    
    # Create map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    
    # Add each precinct
    for idx, row in contest_geo.iterrows():
        precinct = row['precinct']
        winner = row['candidate']
        
        # Get all results for this precinct/contest
        precinct_results = contest_data[contest_data['precinct'] == precinct]
        total_votes = precinct_results['votes'].sum()
        
        # Build popup HTML
        popup_html = f"""
        <div style="font-family: Arial; font-size: 12px; width: 250px;">
            <h4 style="margin: 5px 0;">{row['name']}</h4>
            <p style="margin: 5px 0;"><b>Precinct:</b> {precinct}</p>
            <p style="margin: 5px 0;"><b>Contest:</b> {contest}</p>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;"><b>Results:</b></p>
        """
        
        # Add each candidate's results
        for _, result in precinct_results.iterrows():
            candidate = result['candidate']
            votes = result['votes']
            percentage = (votes / total_votes * 100) if total_votes > 0 else 0
            marker = "W" if candidate == winner else "  "
            popup_html += f"""
            <p style="margin: 2px 0; padding-left: 10px;">
                {marker} {candidate}: {votes} votes ({percentage:.1f}%)
            </p>
            """
        
        popup_html += f"""
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;"><b>Total Votes:</b> {total_votes}</p>
        </div>
        """
        
        # Add to map with color based on winner
        folium.GeoJson(
            row['geometry'],
            style_function=lambda x, color=candidate_colors.get(winner, 'gray'): {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.6
            },
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(m)
    
    # Add legend
    legend_html = f'''
    <div style="position: fixed; 
                top: 10px; right: 10px; width: 200px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
        <p style="margin: 5px 0;"><b>{contest}</b></p>
        <hr style="margin: 5px 0;">
    '''
    
    for candidate in unique_candidates:
        if candidate in contest_data['candidate'].values:
            color = candidate_colors.get(candidate, 'gray')
            legend_html += f'''
            <p style="margin: 5px 0;">
                <span style="background-color:{color}; 
                      width: 20px; height: 20px; 
                      display: inline-block; border: 1px solid black;">
                </span> {candidate}
            </p>
            '''
    
    legend_html += '</div>'
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save map
    safe_filename = contest.replace(' ', '_').replace('/', '_')
    m.save(f'data/maps/{safe_filename}_map.html')
    print(f"✓ Saved: {safe_filename}_map.html")

print("\n✓ All maps created!")