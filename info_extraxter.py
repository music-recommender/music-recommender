import os
import pandas as pd
import hdf5_getters as g
import numpy as np
import math

# Real
MSD_ROOT = "/home/taleiko/Documents/Introduction to data science/Mini-project/MillionSongSubset"
# Subfolder for testing
# MSD_ROOT = "/home/taleiko/Documents/Introduction to data science/Mini-project/MillionSongSubset/B/I"
# OUTPUT_FILE = "data/song_info.csv"
# OUTPUT_FILE = "data/song_info_test.csv"
OUTPUT_FILE = "data/song_info_complete_rows.csv"

files = []

def createFileList(dir=MSD_ROOT):
    for path in os.listdir(dir):
        # print(path)
        dir_path = "/".join([dir, path])
        if os.path.isdir(dir_path):
            createFileList(dir_path)
        else:
            global files
            files.append(dir_path)

def createSongInfoCsv(file_paths):
    rows = []
    for file_path in file_paths:
        h5 = g.open_h5_file_read(file_path)
        row = [
            g.get_song_id(h5).decode(),
            g.get_title(h5).decode(),
            g.get_artist_name(h5).decode(),
            # How do we use the terms as a feature?
            # Are they consistent or improvised for each song?
            # If improvised, then they are just useless noise.
            np.array([term.decode() for term in g.get_artist_terms(h5)]),
            g.get_artist_location(h5).decode(),
            g.get_artist_latitude(h5),
            g.get_artist_longitude(h5),
            # Meaning unclear
            # g.get_danceability(h5),
            g.get_tempo(h5),
            # Does not always exist, 0 in that case.
            # Can we get around this?
            g.get_year(h5)
        ]   
        h5.close()
        rows.append(row)
    df = pd.DataFrame(rows, columns=["song_id",
                                     "title",
                                     "artist_name",
                                     "artist_terms",
                                     "location",
                                     "lat",
                                     "lon",
                                    #  "danceability",
                                     "tempo",
                                     "year"
                                    ])
    # print(df)
    df = df.dropna()
    df = processGenreColumn(df)
    df = removeYear0(df)
    # print(df)
    df.to_csv(OUTPUT_FILE, index=False)

def removeYear0(df):
    return df[df.year != 0]

def processGenreColumn(df):
    genre_labels = createGenreLabels()
    col = df["artist_terms"]
    scores = np.zeros(len(col), dtype=int)
    for i in range(len(col)):
        score = 0
        n_scores = 0
        for term in col[i]:
            for keyword in genre_labels.keys():
                if keyword in term:
                    score += genre_labels[keyword]
                    n_scores += 1
        if n_scores == 0:
            scores[i] = -1
        else:
            scores[i] = math.floor(score / n_scores)
    df["artist_terms_label"] = scores
    return df

def createGenreLabels():
    genres = ["classic", "soul", "blues", "country", "jazz", "pop", "hip hop", "disco", "techno", "rock", "metal"]
    # tango?
    genre_scores = {}
    score = 0
    for genre in genres:
        genre_scores[genre] = score
        score += 1
    return genre_scores


createFileList(MSD_ROOT)
createSongInfoCsv(files)

# print(files)