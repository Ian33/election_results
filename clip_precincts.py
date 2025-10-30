import geopandas as gpd
import folium

# Read the GeoJSON file
precincts = gpd.read_file(r"data\gs_data\SnoCo_Precinct_Districts.geojson")

# precincts = precincts.to_crs(epsg=4326) existing crs
#precincts = precincts.to_crs(epsg = 32610)
precincts = precincts.to_crs(epsg=4326)

boundary = gpd.read_file(r"data/gs_data/Edmonds_Boundary.geojson")
#boundary = boundary.to_crs(epsg = 32610)
boundary = boundary.to_crs(epsg=4326)

edm_precincts = gpd.clip(precincts, boundary)
edm_precincts.to_file("data/gs_data/edmonds_precincts.geojson", driver='GeoJSON')
print(edm_precincts)