import panel as pn
import pandas as pd
from bokeh.models.widgets.tables import NumberFormatter
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import numpy as np
import json

pn.extension("tabulator")

all_columns = [
    "index", "ID", "Title", "Artist", "Genres", "Location", "Latitude", "Longitude", "Tempo", "Year", "Overlapping genres", "Distance"
]
hidden_columns=["index", "ID", "Latitude", "Longitude", "Distance"]
recom_cols = ["Year", "Tempo", "Latitude", "Longitude", "Overlapping genres"]

msd_df = pd.read_csv(
    "https://raw.githubusercontent.com/music-recommender/music-recommender/main/data/song_info_complete_rows.csv",
    converters={
        "Genres": lambda x: x.split(",")
    }
)

msd_df_all = pd.read_csv(
    "https://raw.githubusercontent.com/music-recommender/music-recommender/main/data/song_info_all.csv",
    converters={
        "Genres": lambda x: x.split(",")
    }
)

def create_tabulator(df, hc, sel_opt):
    return pn.widgets.Tabulator(
        df,
        selectable=sel_opt,
        hidden_columns=hc,
        pagination="local",
        layout="fit_columns",
        page_size=10,
        sizing_mode="stretch_width",
        disabled=True,
        formatters= {
            "Tempo": NumberFormatter(format="0"),
            "Year": NumberFormatter(format="0"),
        }
    )

tab = create_tabulator(
    msd_df, hc=hidden_columns, sel_opt="checkbox"
)
k_input = pn.widgets.IntInput(
    value=5, start=1, step=1, end=msd_df.shape[0], width=100
)
included_recom_cbg = pn.widgets.CheckBoxGroup(
    options=recom_cols, value=recom_cols
)
hidden_columns_cbg = pn.widgets.CheckBoxGroup(
    options=all_columns, value=hidden_columns
)
dataset_switch = pn.widgets.Switch(value=False)

def count_overlapping_genres(song_ats, other_ats):
    c = 0
    for at in song_ats:
        if at in other_ats:
            c += 1
    return c


def recommendSongs(selection, k, cols, songs):
    # If overlapping genres are used, we need to remove the column temporarily because it is not built yet
    use_genres = "Overlapping genres" in cols
    if use_genres:
        cols.remove("Overlapping genres")
    # ids = list(map(lambda i: songs.iloc[i]["ID"], selection)) # Maybe del
    genres = list(map(lambda song: songs.iloc[song]["Genres"], selection))
    # save song data 
    selection_songs = songs[cols].iloc[selection]
    # Remove all songs from the artists in the selection
    songs = songs[~ songs["Artist"].isin(list(songs.iloc[selection]["Artist"]))]
    # selection = list(map(lambda i: songs.index[songs["ID"] == test_id].tolist(), selection)) # Maybe del
    # We create a separate dataframe for each song (because the Overlapping genres are different for each song)
    songs_with_genres = list()
    for s in range(len(selection)):
        songs_with_genres.append(songs[cols].copy())
        if use_genres:
            songs_with_genres[s]["Overlapping genres"] = songs["Genres"].apply(
                lambda x: count_overlapping_genres(
                genres[s], x
            ))
    if use_genres:
        selection_songs["Overlapping genres"] = list(map(len, genres))
    # We normalize everything using the same scaler 
    scaler = StandardScaler().fit(songs_with_genres[0])
    songs_data = list()
    for song_list in songs_with_genres:
        songs_data.append(scaler.transform(song_list))
    selection_songs_scaled = scaler.transform(selection_songs)
    # Create list of nearest neighbours for each song
    neighbours = list()
    for song, matrix in zip(selection_songs_scaled, songs_data):
        # We make k*selection_size suggestions here, just in case there are better candidates since more input songs mean broader search space
        neighbours += NearestNeighbors(n_neighbors = k*len(selection)).fit(matrix).kneighbors([song], return_distance = False).tolist()[0]
    # Delete duplicates
    neighbours = list(set(neighbours))
    results = songs.iloc[neighbours].copy().reset_index()
    results["Distance"] = [0] * len(results)
    results["Distance"] = results["Distance"].astype(np.float64)
    # Calculate squared distances for each result song for each input song
    for song, matrix in zip(selection_songs_scaled, songs_data):
        for i, result in enumerate(neighbours):
            results.loc[i, "Distance"] += np.square(np.linalg.norm(song - matrix[result]))
    # Sort by least distance and only return the first k elements
    return results.sort_values(by=["Distance"]).iloc[:k].reset_index(drop=True)

def readEchoUserData():
    with open("data/echo_user_data.json", "r") as f:
        echo_user_data = json.load(f)
    for user in echo_user_data.keys():
        echo_user_data[user] = set(echo_user_data[user])
    return echo_user_data

def echoComparison(user_song_id, recommended_songs_df):
    song_ids = np.array([
        row["ID"] for row in recommended_songs_df.iloc
    ])
    echo_listens = readEchoUserData()
    users = list(echo_listens.keys())
    scores = np.zeros(len(song_ids))
    user_song_listeners = np.zeros(len(song_ids))

    for i in range(len(song_ids)):
        for user in users:
            if user_song_id in echo_listens[user]:
                if song_ids[i] in echo_listens[user]:
                    scores[i] += 1
                user_song_listeners[i] += 1

    for i in range(len(scores)):
        if user_song_listeners[i] > 0:
            scores[i] = scores[i] / user_song_listeners[i]
    return scores


@pn.depends(s=tab.param.selection, k=k_input, ir=included_recom_cbg, hc=hidden_columns_cbg)
def output(s, k, ir, hc):
    if len(s) == 0:
        return "### Please select a song."
    elif not ir:
        return "### Please select at least one column used for prediction."
    else:
        recommend_df = recommendSongs(s, k, ir, tab.value.copy())
        recommend_tab = create_tabulator(recommend_df, hc=hc, sel_opt=False)
        # Commented this out because it didn't work for me. Had the same issue as Matias
        # echo_results = echoComparison(s, recommend_df)
        # return pn.Column(recommend_tab, echo_results)
        return pn.Column(recommend_tab)

@pn.depends(hc=hidden_columns_cbg, watch=True)
def update_hidden_columns(hc):
    tab.hidden_columns = hc

@pn.depends(b=dataset_switch, watch=True)
def update_tab_df(b):
    if b:
        tab.value = msd_df_all
    else:
        tab.value = msd_df

template = pn.template.VanillaTemplate(
    title="Music Recommender",
    sidebar=[
        "## Settings",
        pn.layout.Divider(),
        "### Number of recommendations",
        k_input,
        "### Include in recommendation",
        included_recom_cbg,
        "### Hidden columns",
        hidden_columns_cbg,
        "### Allow missing values",
        dataset_switch
    ],
    sidebar_width = 240
)

template.main.append(
    pn.Column(
        "# Songs",
        tab,
        "# Recommendations",
        output)
)

template.servable()
