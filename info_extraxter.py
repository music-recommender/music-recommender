import os
import pandas as pd
import hdf5_getters as g
import numpy as np

MSD_ROOT = "/home/taleiko/Documents/Introduction to data science/Mini-project/MillionSongSubset"
OUTPUT_FILE = "data/song_info_all.csv"

files = []

def createFileList(dir=MSD_ROOT):
    for path in os.listdir(dir):
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
            g.get_track_id(h5).decode(),
            g.get_title(h5).decode(),
            g.get_artist_name(h5).decode(),
            np.array([term.decode() for term in g.get_artist_terms(h5)]),
            g.get_artist_location(h5).decode(),
            g.get_artist_latitude(h5),
            g.get_artist_longitude(h5),
            round(g.get_tempo(h5)),
            g.get_year(h5)
        ]
        h5.close()
        rows.append(row)
    df = pd.DataFrame(
        rows,
        columns=[
            "ID",
            "Track",
            "Title",
            "Artist",
            "Genres",
            "Location",
            "Latitude",
            "Longitude",
            "Tempo",
            "Year",
        ],
    )
    # df = df.dropna()
    df = processGenreColumn(df)
    df = removeYear0(df)
    df.to_csv(OUTPUT_FILE, index=False)


def removeYear0(df):
    return df[df.Year != 0]


def processGenreColumn(df):
    df.Genres = df.Genres.apply(lambda x: sorted(x.tolist()))
    return df


createFileList(MSD_ROOT)
createSongInfoCsv(files)
