import h5py
import hdf5_getters as g
import os

filename = "file.hdf5"


# print(type(g.open_h5_file_read))
h5 = g.open_h5_file_read("/home/taleiko/Documents/Introduction to data science/Mini-project/MillionSongSubset/A/A/A/TRAAAAW128F429D538.h5")
# h5 = g.open_h5_file_read("/home/taleiko/Documents/Introduction to data science/Mini-project/MillionSongSubset/A/K/I/TRAKIIY128F9312465.h5")

# print(g.get_release(h5))
# print(g.get_num_songs(h5))

# print(g.get_artist_name(h5))
# print(g.get_artist_terms(h5))
# print(g.get_year(h5))
# print(g.get_artist_location(h5))
#print(g.get_song_id(h5))

def printSongInfo(path):
    # SONG NAME?
    h5 = g.open_h5_file_read(path)
    print(g.get_artist_name(h5))
    print(g.get_artist_terms(h5))
    # print(g.get_release(h5))
    print(g.get_year(h5))
    print(g.get_artist_location(h5))

#printSongInfo("/home/taleiko/Documents/Introduction to data science/Mini-project/MillionSongSubset/A/A/A/TRAAAAW128F429D538.h5")

print(h5.root.metadata.songs.cols[0])

# print(h5.root.musicbrainz.songs.cols.year[0])



# for path in os.listdir("/home/taleiko/Documents/Introduction to data science/Mini-project/MillionSongSubset/A/K/I"):
#     printSongInfo("/home/taleiko/Documents/Introduction to data science/Mini-project/MillionSongSubset/A/K/I/" + path)
