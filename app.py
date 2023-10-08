import panel as pn
import pandas as pd
from music_recommender import recommendSongs

pn.extension("tabulator")

INPUT_FILE = "data/song_info_complete_rows.csv"

filters = {
    "title": {"type": "input", "func": "like", "placeholder": "Enter title"},
    "artist_name": {"type": "input", "func": "like", "placeholder": "Enter artist"},
    "artist_terms": {"type": "input", "func": "like", "placeholder": "Enter terms"},
    "location": {"type": "input", "func": "like", "placeholder": "Enter location"},
    "danceability": {
        "type": "number",
        "func": ">=",
        "placeholder": "Enter minimum danceability",
    },
    "tempo": {"type": "number", "func": ">=", "placeholder": "Enter minimum tempo"},
    "year": {"type": "number", "func": "=", "placeholder": "Enter year"},
}

msd_df = pd.read_csv(INPUT_FILE)
tab = pn.widgets.Tabulator(
    msd_df,
    pagination="local",
    layout="fit_columns",
    page_size=10,
    sizing_mode="stretch_width",
    header_filters=filters,
    disabled=True,
    selectable="toggle",
)


@pn.depends(s=tab.param.selection)
def output(s):
    if len(s) == 1:
        return pn.Column(
            "# Recommendations",
            pn.widgets.Tabulator(
                tab.value.iloc[recommendSongs(s[0])[0]],
                sizing_mode="stretch_width",
                layout="fit_columns",
                disabled=True,
            ),
        )
    else:
        return


template = pn.template.VanillaTemplate(title="Music Recommender", sidebar=[])
template.main.append(pn.Column("# Songs", tab, output))
template.servable()
