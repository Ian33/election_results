import pandas as pd

data = pd.read_csv(r"data/all_results.csv")
print(data)
boundary = gpd.read_file(r"data/gs_data/Edmonds_Boundary.geojson")
#boundary = boundary.to_crs(epsg = 32610)
boundary = boundary.to_crs(epsg=4326)
edm_precincts.to_file("data/gs_data/edmonds_precincts.geojson", driver='GeoJSON')