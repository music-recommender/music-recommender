import os
import pandas as pd
import hdf5_getters as g
import numpy as np

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
    df = removeYear0(df)
    df = processGenreColumn(df)
    df.to_csv(OUTPUT_FILE, index=False)

def removeYear0(df):
    return df[df.year != 0]

def processGenreColumn(df):
    df.artist_terms = df.artist_terms.apply(lambda x: sorted(x.tolist()))
    return df

createFileList(MSD_ROOT)
createSongInfoCsv(files)

# print(files)