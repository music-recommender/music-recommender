import panel as pn
import pandas as pd
from bokeh.models.widgets.tables import NumberFormatter
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

pn.extension("tabulator")

all_columns = [
    "index", "ID", "Title", "Artist", "Genres", "Location", "Latitude", "Longitude", "Tempo", "Year", "Overlapping genres"
]
hidden_columns=["index", "ID", "Latitude", "Longitude"]
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
    song_id = selection[0]
    songs["Overlapping genres"] = songs.Genres.apply(
        lambda x: count_overlapping_genres(
            songs.iloc[song_id].Genres, x
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


@pn.depends(s=tab.param.selection, k=k_input, ir=included_recom_cbg, hc=hidden_columns_cbg)
def output(s, k, ir, hc):
    if len(s) == 0:
        return "### Please select a song."
    elif not ir:
        return "### Please select at least one column used for prediction."
    else:
        recommend_df = recommendSongs(s, k, ir, tab.value.copy())
        recommend_tab = create_tabulator(recommend_df, hc=hc, sel_opt=False)
        jam_results = None # Vector

        return pn.Column(recommend_tab, jam_results)

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
