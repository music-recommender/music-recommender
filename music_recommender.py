# TODO
# Load the training data
# Turn string values in to numerical values

# VERIFICATION DATA
# Take jam_to_msd.tsv and
#   create maps for the needed conversions
# Take likes.tsv and
#   group the dataset by user IDs
#   pick a user and check if the recommended songs are in the set of liked songs
#   PROBLEM: How do we choose what user to pick?
#     If the user is picked randomly, then the correct answer is not consistent
#     every time the model is trained.
#     sort the user IDs and pick the first one? Then it is always the same for
#     each set of data.

LIKES_FILE = "data/likes.tsv"
JAM_MSD_FILE = "data/jam_to_msd.tsv"
# SONGS_FILE = "data/song_info.csv"
SONGS_FILE = "data/song_info_test.csv"

import pandas as pd

# dfJamMsd = pd.read_csv(JAM_MSD_FILE, sep="\t", names=["jam_id", "msd_id"])
# print(dfJamMsd)
# # jamToMsd = {row["jam_id"]: row["msd_id"] for row in df.iloc}

# dfLikes = pd.read_csv(LIKES_FILE, sep="\t")
# print(dfLikes)
# sortedLikes = dfLikes.sort_values("jam_id")
# print(sortedLikes)
# likesGroups = dfLikes.groupby("user_id")

# Loading songs
songs = pd.read_csv(SONGS_FILE)
print(songs)

# Convert string values into categorical values
for val in ["location"]:
    songs[val] = songs[val].astype("category")

cat_columns = songs.select_dtypes(["category"]).columns
songs[cat_columns] = songs[cat_columns].apply(lambda x: x.cat.codes)
print(songs)

# Machine learning

# from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

songSamples = [[song["lat"], song["lon"], song["tempo"], song["year"]] for song in songs.iloc]
print(songSamples)

# samples = [[0, 0, 2], [1, 0, 0], [0, 0, 1]]
# neigh = NearestNeighbors(n_neighbors=2, radius=0.4)
# neigh.fit(samples)

# print(neigh.kneighbors([[0, 0, 1.3]], 2, return_distance=False))
# nbrs = neigh.radius_neighbors(
#     [[0, 0, 1.3]], 0.4, return_distance=False
# )

