import pandas as pd
import json

# Our song data from MSD
songs = pd.read_csv("data/song_info_all.csv")
# Echo user data
echo_data = pd.read_csv("data/train_triplets.txt",
                sep="\t",
                names=["user_id", "msd_id", "listen_times"])

# Filter to the songs that we have
song_set = set(songs["song_id"])
echo_data = echo_data[echo_data["msd_id"].isin(song_set)]

# Create a JSON file with every user's likes gathered as a list
echo_listens = {}
for row in echo_data.iloc:
    try:
        echo_listens[row["user_id"]].append(row["msd_id"])
    except:
        echo_listens[row["user_id"]] = [row["msd_id"]]

with open("data/echo_user_data.json", "w") as f:
    f.write(json.dumps(echo_listens, indent=2))