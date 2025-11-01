import geopandas as gpd
import folium
import pandas as pd
import os
import numpy as np
import math
import matplotlib.colors as mcolors

# to view a map https://ian33.github.io/election_results/data/maps/CITY_OF_EDMONDS_Council_Position_3_map.html

# Create output directory
os.makedirs('data/maps', exist_ok=True)

# Load data
data = pd.read_csv(r"data/all_results.csv")
data["precinct"] = pd.to_numeric(data["precinct"])

edm_precincts = gpd.read_file(r"data/gs_data/edmonds_precincts.geojson")
edm_precincts["precinct"] = pd.to_numeric(edm_precincts["precinct"])
edm_precincts = edm_precincts.to_crs(epsg=4326)

# Merge data with geometry - KEEP AS GEODATAFRAME
edm_data = gpd.GeoDataFrame(
    edm_precincts.merge(data, on="precinct", how="inner"),
    geometry='geometry',
    crs=edm_precincts.crs
)

# determin winner of precinct for contest
def get_precinct_winners(df):
    # Group by precinct and contest, find candidate with most votes
    winners = df.loc[df.groupby(['precinct', 'contest'])['votes'].idxmax()]
    return winners
def get_color_with_opacity(base_color, percentage):
    """
    Convert a color to have varying intensity based on percentage.
    Returns color with opacity scaled by percentage.
    """
    # Normalize percentage to 0-1 range
    normalized = percentage / 100.0
    
    # For fillOpacity approach (keeps color consistent, varies transparency)
    return base_color, normalized

def get_gradient_color(base_color, percentage):
    # Map percentage to index (0-10)
    if percentage < 20:
        idx = 0
    elif percentage < 25:
        idx = 1
    elif percentage < 30:
        idx = 2
    elif percentage < 35:
        idx = 3
    elif percentage < 40:
        idx = 4
    elif percentage < 45:
        idx = 5
    elif percentage < 50:
        idx = 6
    elif percentage < 55:
        idx = 7
    elif percentage < 60:
        idx = 8
    elif percentage < 65:
        idx = 9    
    else:
        idx = 10

    color_gradients = {
        'red': ['#FEEBE7','#FCC6BB','#FAA18F','#F87C63','#F54927','#F4320B','#C82909','#9C2007','#701705','#440E03','#180501'],
        'green': ['#EFF6F0','#D2E5D4','#B5D4B9','#97C39D','#7AB382','#5DA266','#467A4D','#3C6841','#2B4A2F','#1A2D1D','#09100A'],
        'blue': ['#E7E7FE','#BBBDFC','#8F93FA','#6368F8','#272EF5','#0B13F4','#0910C8','#070C9C','#050970','#030544','#010218'],
        'orange': ['#FEF5E6','#FDE2BA','#FBCF8E','#F9BD62','#F7A328','#F69709','#CA7C07','#9D6106','#714604','#452A02','#190F01'],
        'purple': ['#F7E6FE','#E9BAFD','#DA8EFB','#CC62F9','#B928F7','#AF09F6','#8F07CA','#70069D','#500471','#310245','#110119'],
        'pink': ['#FDE8F9','#F9BEEE','#F594E3','#F16AD8','#ED37CC','#E916C3','#BF12A0','#950E7C','#6B0A59','#410636','#170213'],
        'teal': ['#E8FDF9','#BEF9EF','#94F5E5','#6AF1DB','#37EDCF','#16E9C6','#12BFA2','#0E957F','#0A6B5B','#064137','#021714']
    }
 
    return color_gradients.get(base_color, color_gradients['red'])[idx]
    

# winners of each precinct
winners_df = get_precinct_winners(edm_data)

# create a color map for candidates
unique_candidates = edm_data['candidate'].unique()
colors = ['red', 'blue', 'green', 'orange', 'purple', 'pink', 'teal']
candidate_colors = {candidate: colors[i % len(colors)] for i, candidate in enumerate(unique_candidates)}


#gradient={'0':'Navy', '0.25':'Blue','0.5':'Green', '0.75':'Yellow','1': 'Red'}
# get unique contests
contests = edm_data['contest'].unique()

# Create a map for each contest
for contest in contests:
    # Filter data for this contest
    contest_data = edm_data[edm_data['contest'] == contest]
    contest_winners = winners_df[winners_df['contest'] == contest]
    
    # Calculate total votes per candidate for this contest
    candidate_totals = contest_data.groupby('candidate')['votes'].sum().to_dict()
    total_contest_votes = sum(candidate_totals.values())
    
    # Find overall winner
    overall_winner = max(candidate_totals, key=candidate_totals.get)
    
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
        base_color = candidate_colors.get(winner, 'gray')
        # Method 1: Use gradient color (blends with white)
        gradient_color = get_gradient_color(base_color, percentage)
        # Add to map with color based on winner
        # Method 2: Use variable opacity (simpler, often better looking)
        folium.GeoJson(
            row['geometry'],
            style_function=lambda x, color=gradient_color, pct=percentage: {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.3 + (pct / 100.0 * 0.7)  # 0.3 to 1.0 range
            },
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(m)
    
    # Add legend with vote totals
    legend_html = f'''
            <div style="position: fixed; 
                        top: 10px; right: 10px; width: 320px; 
                        background-color: white; border:2px solid grey; z-index:9999; 
                        font-size:14px; padding: 10px">
                <p style="margin: 5px 0;"><b>{contest}</b></p>
                <hr style="margin: 5px 0;">
            '''
                
    # Sort candidates by votes (winner first)
    sorted_candidates = sorted(candidate_totals.items(), key=lambda x: x[1], reverse=True)
    
    for candidate, votes in sorted_candidates:
        if candidate in contest_data['candidate'].values:
            color = candidate_colors.get(candidate, 'gray')
            percentage = (votes / total_contest_votes * 100) if total_contest_votes > 0 else 0
            is_winner = candidate == overall_winner
            
            # Bold the winner
            font_weight = 'bold' if is_winner else 'normal'
            
            legend_html += f'''
            <p style="margin: 5px 0; font-weight: {font_weight};">
                <span style="background-color:{color}; 
                      width: 20px; height: 20px; 
                      display: inline-block; border: 1px solid black;">
                </span> {candidate}<br>
                <span style="margin-left: 30px; font-size: 12px;">
                    {votes:,} votes ({percentage:.1f}%)
                </span>
            </p>
            '''
    
    legend_html += f'''
        <hr style="margin: 5px 0;">
        <p style="margin: 5px 0; font-size: 12px;">
            <b>Total:</b> {total_contest_votes:,} votes
        </p>
    </div>
    '''
    
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save map
    safe_filename = contest.replace(' ', '_').replace('/', '_')
    m.save(f'data/maps/{safe_filename}_map.html')
    print(f"✓ Saved: {safe_filename}_map.html")

print("\n✓ All maps created!")