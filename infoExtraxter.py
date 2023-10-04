import os
import pandas as pd
import hdf5_getters as g

# Real
MSD_ROOT = "/home/taleiko/Documents/Introduction to data science/Mini-project/MillionSongSubset"
# Subfolder for testing
# MSD_ROOT = "/home/taleiko/Documents/Introduction to data science/Mini-project/MillionSongSubset/B/I"
OUTPUT_FILE = "data/song_info.csv"

files = []

def createFileList(dir=MSD_ROOT):
    for path in os.listdir(dir):
        # print(path)
        dirPath = "/".join([dir, path])
        if os.path.isdir(dirPath):
            createFileList(dirPath)
        else:
            global files
            files.append(dirPath)

def createSongInfoCsv(filePaths):
    rows = []
    for filePath in filePaths:
        h5 = g.open_h5_file_read(filePath)
        row = [
            g.get_title(h5),
            g.get_artist_name(h5),
            # How do we use the terms as a feature?
            g.get_artist_terms(h5),
            g.get_artist_location(h5),
            g.get_danceability(h5),
            g.get_tempo(h5),
            g.get_year(h5)
        ]
        h5.close()
        rows.append(row)
    df = pd.DataFrame(rows, columns=["title",
                                     "artist_name",
                                     "artist_terms",
                                     "location",
                                     "danceability",
                                     "tempo",
                                     "year"])
    # print(df)
    df.to_csv(OUTPUT_FILE, index=False)




createFileList(MSD_ROOT)
createSongInfoCsv(files)

# print(files)