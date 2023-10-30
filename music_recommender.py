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