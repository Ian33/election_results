import pandas as pd
import geopandas as gpd
data = pd.read_csv(r"data/all_results.csv")
data["precinct"] = pd.to_numeric(data["precinct"])

#print(data.loc[data["precinct"] == 23231564])
edm_precincts = gpd.read_file(r"data/gs_data/edmonds_precincts.geojson")
edm_precincts["precinct"] = pd.to_numeric(edm_precincts["precinct"])

#boundary = boundary.to_crs(epsg = 32610)
edm_precincts = edm_precincts.to_crs(epsg=4326)
print(edm_precincts)
#print(edm_precincts.loc[edm_precincts["name"] == "Edmonds 50"])
edm_data = edm_precincts.merge(data, on="precinct", how="inner")

"""
## reclip
boundary = gpd.read_file(r"data/gs_data/Edmonds_Boundary.geojson")
#boundary = boundary.to_crs(epsg = 32610)
boundary = boundary.to_crs(epsg=4326)

edm_data = gpd.clip(edm_data, boundary)"""
#edm_data = pd.merge(data, edm_precincts, on = "precinct", how = "right")
#edm_data = edm_data.dropna(subset=["geometry"])
edm_data.to_csv("data/edm_data.csv", index = False)
print(edm_data)