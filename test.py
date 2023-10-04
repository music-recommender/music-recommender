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

# Irrelevant
# print(g.get_num_songs(h5))
# print(g.get_end_of_fade_in(h5))
# print(g.get_start_of_fade_out(h5))

# Need to be converted into something else (e.g. IDs)
# print(g.get_artist_id(h5))
# print(g.get_artist_mbid(h5))
# print(g.get_artist_playmeid(h5))
# print(g.get_artist_7digitalid(h5))
# print(g.get_release_7digitalid(h5))
# print(g.get_song_id(h5))
# print(g.get_track_7digitalid(h5))
# print(g.get_audio_md5(h5))
# print(g.get_key(h5))
# print(g.get_track_id(h5))

# Meaning unclear (vectors and values)
# print(g.get_artist_familiarity(h5))
# print(g.get_artist_hotttnesss(h5))
# print(g.get_song_hotttnesss(h5))
# print(g.get_key_confidence(h5))
# print(g.get_time_signature_confidence(h5))
# print(g.get_segments_start(h5))
# print(g.get_segments_confidence(h5))
# print(g.get_segments_pitches(h5))
# print(g.get_segments_timbre(h5))
# print(g.get_segments_loudness_max(h5))
# print(g.get_segments_loudness_max_time(h5))
# print(g.get_segments_loudness_start(h5))
# print(g.get_sections_start(h5))
# print(g.get_sections_confidence(h5))
# print(g.get_beats_start(h5))
# print(g.get_beats_confidence(h5))
# print(g.get_bars_start(h5))
# print(g.get_bars_confidence(h5))
# print(g.get_tatums_start(h5))
# print(g.get_tatums_confidence(h5))
# print(g.get_artist_mbtags(h5))
# print(g.get_artist_mbtags_count(h5))

# Exact meaning unclear
# print(g.get_artist_latitude(h5))
# print(g.get_artist_longitude(h5))
# print(g.get_analysis_sample_rate(h5))
# print(g.get_artist_terms_freq(h5))
# print(g.get_artist_terms_weight(h5))
# print(g.get_loudness(h5))
# print(g.get_mode(h5))
# print(g.get_mode_confidence(h5))
# print(g.get_time_signature(h5))

# Somewhat useful
# print(g.get_release(h5))
# print(g.get_duration(h5))
# print(g.get_energy(h5))

# Useful
print(g.get_artist_location(h5))
print(g.get_artist_name(h5))
print(g.get_title(h5))
print(g.get_artist_terms(h5))
print(g.get_danceability(h5))
print(g.get_tempo(h5))
print(g.get_year(h5))

# NOTE: Kind of what we do, should leave out
# print(g.get_similar_artists(h5))

# print(g.get_song_id(h5))
# print(g.get_title(h5))

def printSongInfo(path):
    # SONG NAME?
    h5 = g.open_h5_file_read(path)
    print(g.get_title(h5))
    print(g.get_artist_name(h5))
    print(g.get_artist_terms(h5))
    # print(g.get_release(h5))
    print(g.get_year(h5))
    print(g.get_artist_location(h5))

#printSongInfo("/home/taleiko/Documents/Introduction to data science/Mini-project/MillionSongSubset/A/A/A/TRAAAAW128F429D538.h5")

# print(h5.root.metadata.songs.cols[0])

# print(h5.root.musicbrainz.songs.cols.year[0])



# for path in os.listdir("/home/taleiko/Documents/Introduction to data science/Mini-project/MillionSongSubset/A/K/I"):
#     printSongInfo("/home/taleiko/Documents/Introduction to data science/Mini-project/MillionSongSubset/A/K/I/" + path)

h5.close()