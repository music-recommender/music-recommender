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
# SONGS_FILE = "data/song_info_test.csv"
SONGS_FILE = "data/song_info_complete_rows.csv"

import sys
import pandas as pd
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def main():
    print(recommendSongs(0))

def loadSongs(file_path=SONGS_FILE):
    songs = pd.read_csv(file_path)
    for val in ["location"]:
        songs[val] = songs[val].astype("category")
    cat_columns = songs.select_dtypes(["category"]).columns
    songs[cat_columns] = songs[cat_columns].apply(lambda x: x.cat.codes)
    return songs

def recommendSongs(song_id, k=5, songs=loadSongs()):
    cols = ["lat", "lon", "tempo", "year", "artist_terms_label"]
    songs = pd.DataFrame(
        StandardScaler().fit_transform(songs[cols].values),
        columns=cols,
        index=songs.index,
    )
    nn = NearestNeighbors(n_neighbors=1)
    nn.fit(songs.values.tolist())
    return nn.kneighbors(
        [songs.iloc[song_id].tolist()], k + 1, return_distance=False)


# Verifying results with Thisismyjam
# dfJam_msd = pd.read_csv(JAM_MSD_FILE, sep="\t", names=["jam_id", "msd_id"])
# print(dfJam_msd)
# # jamToMsd = {row["jam_id"]: row["msd_id"] for row in df.iloc}

# df_likes = pd.read_csv(LIKES_FILE, sep="\t")
# print(df_likes)
# sorted_likes = df_likes.sort_values("jam_id")
# print(sorted_likes)
# likes_groups = df_likes.groupby("user_id")

if __name__ == "__main__":
    sys.exit(main())