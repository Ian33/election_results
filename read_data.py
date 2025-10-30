## data source  ##
# https://www.sos.wa.gov/elections/data-research/election-results-and-voters-pamphlets/2025-primary-election
# https://results.vote.wa.gov/results/20250805/snohomish/

import pandas as pd

file_path = "data/20250805_snohomishprecincts.csv"

data = pd.read_csv(file_path, header = None)
# rename columns
data.columns = ["contest", "candidate", "name", "precinct", "votes"]
data = data[data['precinct'] != -1]
data = data[data["candidate"] != "WRITE-IN"]
data = data.drop(columns = ["precinct"])
data.to_csv(r"data/all_results.csv", index = False)
print(data)
# list unique contests
#print(data["contest"].unique())
# list unique municipalities
#print(data["municipality"].unique())