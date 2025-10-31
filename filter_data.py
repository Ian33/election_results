import pandas as pd

data = pd.read_csv("data/edm_data.csv")
contests = data["contest"].unique().tolist()

for contest in contests:
    contest_data = data[data["contest"] == contest].copy()
    canidates = contest_data["candidate"].unique().tolist()
    for candidate in canidates:
        print(candidate)
        canidate_data = contest_data[contest_data["candidate"] == candidate].copy()
        precincts = canidate_data["precinct"].unique().tolist()
        print(canidate_data)
        
#print(contests)
contest: 
