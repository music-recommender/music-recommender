import panel as pn
import pandas as pd
from bokeh.models.widgets.tables import NumberFormatter
from music_recommender import recommendSongs
from tabulator_filters import filters

pn.extension("tabulator")

INPUT_FILE = "data/song_info_complete_rows.csv"

formatters = {
    "index": NumberFormatter(format="0"),
    "lat": NumberFormatter(format="0.00000"),
    "lon": NumberFormatter(format="0.00000"),
    "tempo": NumberFormatter(format="0.000"),
    "year": NumberFormatter(format="0"),
}

msd_df = pd.read_csv(
    INPUT_FILE,
    converters={
        "artist_terms": lambda x: x.split(",")
    }
)

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

@pn.depends(s=tab.param.selection, k=k_input, cbg=checkbox_group)
def output(s, k, cbg):
    if len(s) == 0:
        return "### Please select a song."
    elif not cbg:
        return "### Please select at least one column used for prediction."
    elif len(s) == 1:
        return pn.widgets.Tabulator(
            recommendSongs(s[0], k, cbg, msd_df),
            pagination="local",
            layout="fit_columns",
            page_size=10,
            sizing_mode="stretch_width",
            disabled=True,
            formatters=formatters,
        )
    else:
        return


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
