# TODO
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
SONGS_FILE = "data/song_info_complete_rows.csv"

import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


def count_similar_artist_terms(song_ats, other_ats):
    c = 0
    for at in song_ats:
        if at in other_ats:
            c += 1
    return c


def recommendSongs(selection, k, cols, songs):
    song_id = selection[0]
    songs["artist_terms_matches"] = songs.artist_terms.apply(
        lambda x: count_similar_artist_terms(
            songs.iloc[song_id].artist_terms, x
        )
    )
    songs_copy = songs.copy()
    songs = pd.DataFrame(
        StandardScaler().fit_transform(songs[cols].values),
        columns=cols,
        index=songs.index,
    )
    song_samples = songs.values.tolist()
    nn = NearestNeighbors(n_neighbors=1)
    nn.fit(song_samples)
    v = nn.kneighbors(
        [songs.iloc[song_id].tolist()],
        k + 1,
        return_distance=False
    )

    return songs_copy.iloc[v[0][1:]]

# Can this be removed?
# Verifying results with Thisismyjam
# dfJam_msd = pd.read_csv(JAM_MSD_FILE, sep="\t", names=["jam_id", "msd_id"])
# print(dfJam_msd)
# # jamToMsd = {row["jam_id"]: row["msd_id"] for row in df.iloc}

# df_likes = pd.read_csv(LIKES_FILE, sep="\t")
# print(df_likes)
# sorted_likes = df_likes.sort_values("jam_id")
# print(sorted_likes)
# likes_groups = df_likes.groupby("user_id")
