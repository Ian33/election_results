import geopandas as gpd
import folium

# Read the GeoJSON file
gdf = gpd.read_file(r"data/gs_data/edmonds_precincts.geojson")
# Convert from UTM (EPSG:32610) to lat/lon (EPSG:4326)
gdf = gdf.to_crs(epsg=4326)

# Now get bounds in lat/lon
bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
center_lat = (bounds[1] + bounds[3]) / 2
center_lon = (bounds[0] + bounds[2]) / 2

print(f"Center (lat/lon): {center_lat}, {center_lon}")
print(f"Bounds: {bounds}")

print(f"\nCenter: {center_lat}, {center_lon}")

# Create map
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

#m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

# Add the GeoJSON to the map
folium.GeoJson(
    gdf,
    name='Precinct Districts',
    style_function=lambda x: {
        'fillColor': 'blue',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.3
    }
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save the map
m.save('precinct_map.html')
print("✓ Map saved to precinct_map.html")

# Display in Jupyter (if using Jupyter)
# m