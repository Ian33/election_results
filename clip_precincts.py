import geopandas as gpd
import folium

# Read the GeoJSON file
precincts = gpd.read_file(r"data\gs_data\SnoCo_Precinct_Districts.geojson")
precincts = precincts.rename(columns = {"Name" : "name"})
precincts = precincts.rename(columns = {"Precinct" : "precinct"})
precincts = precincts[["precinct", "name", "geometry"]]
# precincts = precincts.to_crs(epsg=4326) existing crs
#precincts = precincts.to_crs(epsg = 32610)
precincts = precincts.to_crs(epsg=4326)

precincts["precinct"] = precincts["precinct"].str[4:]#.astype(int)
precincts.to_file("data/gs_data/county_precincts.geojson", driver='GeoJSON')
print(precincts)
boundary = gpd.read_file(r"data/gs_data/Edmonds_Boundary.geojson")
#boundary = boundary.to_crs(epsg = 32610)
boundary = boundary.to_crs(epsg=4326)

edm_precincts = gpd.clip(precincts, boundary)
edm_precincts.to_file("data/gs_data/edmonds_precincts.geojson", driver='GeoJSON')
#print(edm_precincts)