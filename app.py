import panel as pn
import pandas as pd
from bokeh.models.widgets.tables import NumberFormatter
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

pn.extension("tabulator")

formatters = {
    "index": NumberFormatter(format="0"),
    "lat": NumberFormatter(format="0.00000"),
    "lon": NumberFormatter(format="0.00000"),
    "tempo": NumberFormatter(format="0.000"),
    "year": NumberFormatter(format="0"),
}

msd_df = pd.read_csv(
    "https://raw.githubusercontent.com/music-recommender/music-recommender/main/data/song_info_complete_rows.csv",
    converters={
        "artist_terms": lambda x: x.split(",")
    }
)

filters = {
    "index": {
        "type": "number",
        "func": ">=",
        "placeholder": "Enter index (min)"
    },
    "song_id": {
        "type": "input",
        "func": "like",
        "placeholder": "Enter song id"},
    "title": {
        "type": "input",
        "func": "like",
        "placeholder": "Enter title"
    },
    "artist_name": {
        "type": "input",
        "func": "like",
        "placeholder": "Enter artist"
    },
    "artist_terms": {
        "type": "input",
        "func": "like",
        "placeholder": "Enter terms"
    },
    "location": {
        "type": "input",
        "func": "like",
        "placeholder": "Enter location"
    },
    "lat": {
        "type": "number",
        "func": ">=",
        "placeholder": "Enter latitude (min)"
    },
    "lon": {
        "type": "number",
        "func": ">=",
        "placeholder": "Enter longitude (min)"
    },
    "tempo": {
        "type": "number",
        "func": ">=",
        "placeholder": "Enter tempo (min)"
    },
    "year": {
        "type": "number",
        "func": ">=",
        "placeholder": "Enter year (min)"
    },
}


tab = pn.widgets.Tabulator(
    msd_df,
    pagination="local",
    layout="fit_columns",
    page_size=10,
    sizing_mode="stretch_width",
    header_filters=filters,
    disabled=True,
    selectable="checkbox",
    formatters=formatters,
)

k_input = pn.widgets.IntInput(
    value=5, start=1, step=1, end=msd_df.shape[0], width=100
)
cols = ["year", "tempo", "lat", "lon", "artist_terms_matches"]
checkbox_group = pn.widgets.CheckBoxGroup(options=cols, value=cols)

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


@pn.depends(s=tab.param.selection, k=k_input, cbg=checkbox_group)
def output(s, k, cbg):
    if len(s) == 0:
        return "### Please select a song."
    elif not cbg:
        return "### Please select at least one column used for prediction."
    else:
        recommend_df = recommendSongs(s, k, cbg, msd_df)
        recommend_tab = pn.widgets.Tabulator(
            recommend_df,
            pagination="local",
            layout="fit_columns",
            page_size=10,
            sizing_mode="stretch_width",
            disabled=True,
            formatters=formatters,
        )
        
        jam_results = None # Vector

        return pn.Column(recommend_tab, jam_results)


template = pn.template.VanillaTemplate(
    title="Music Recommender",
    sidebar=[
        "## Settings",
        pn.layout.Divider(),
        "### Number of recommendations",
        k_input,
        "### Include in recommendation",
        checkbox_group
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
