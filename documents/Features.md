After looking through the available data in the Million Songs (MSD) dataset it seemed like the information that can be retrieved with the following getters is useful:
```
# Useful
g.get_title(h5)
g.get_artist_name(h5)
g.get_artist_terms(h5)
g.get_artist_location(h5)
g.get_danceability(h5)
g.get_tempo(h5)
g.get_year(h5)
```
Below is an example of the output:
```
b'California - LA'
b'Casual'
b"I Didn't Mean To"
[b'hip hop' b'underground rap' b'g funk' b'alternative rap' b'gothic rock'
 b'west coast rap' b'rap' b'club dance' b'singer-songwriter' b'chill-out'
 b'underground hip hop' b'rock' b'gothic' b'san francisco bay area'
 b'indie' b'american' b'punk' b'california' b'industrial' b'new york'
 b'90s' b'latin' b'spanish' b'dark' b'ebm' b'underground' b'deathrock'
 b'west coast' b'san francisco' b'producer' b'oakland' b'catalan'
 b'barcelona' b'doomsdope' b'norcal' b'west coast hip hop'
 b'alternative rock']
0.0
92.198
0
```

The other getters were sorted into other categories.
```
# Irrelevant
get_num_songs(h5)
get_end_of_fade_in(h5)
get_start_of_fade_out(h5)

# Need to be converted into something else (e.g. IDs)
get_artist_id(h5)
get_artist_mbid(h5)
get_artist_playmeid(h5)
get_artist_7digitalid(h5)
get_release_7digitalid(h5)
get_song_id(h5)
get_track_7digitalid(h5)
get_audio_md5(h5)
get_key(h5)
get_track_id(h5)

# Meaning unclear (vectors and values)
get_artist_familiarity(h5)
get_artist_hotttnesss(h5)
get_song_hotttnesss(h5)
get_key_confidence(h5)
get_time_signature_confidence(h5)
get_segments_start(h5)
get_segments_confidence(h5)
get_segments_pitches(h5)
get_segments_timbre(h5)
get_segments_loudness_max(h5)
get_segments_loudness_max_time(h5)
get_segments_loudness_start(h5)
get_sections_start(h5)
get_sections_confidence(h5)
get_beats_start(h5)
get_beats_confidence(h5)
get_bars_start(h5)
get_bars_confidence(h5)
get_tatums_start(h5)
get_tatums_confidence(h5)
get_artist_mbtags(h5)
get_artist_mbtags_count(h5)

# Exact meaning unclear
get_artist_latitude(h5)
get_artist_longitude(h5)
get_analysis_sample_rate(h5)
get_artist_terms_freq(h5)
get_artist_terms_weight(h5)
get_loudness(h5)
get_mode(h5)
get_mode_confidence(h5)
get_time_signature(h5)

# Somewhat useful
get_release(h5)
get_duration(h5)
get_energy(h5)
```