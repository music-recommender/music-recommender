import panel as pn
import pandas as pd
from bokeh.models.widgets.tables import NumberFormatter
from music_recommender import recommendSongs

pn.extension("tabulator")

INPUT_FILE = "data/song_info_complete_rows.csv"

filters = {
    "index": {"type": "number", "func": ">=", "placeholder": "Enter index (min)"},
    "song_id": {"type": "input", "func": "like", "placeholder": "Enter song id"},
    "title": {"type": "input", "func": "like", "placeholder": "Enter title"},
    "artist_name": {"type": "input", "func": "like", "placeholder": "Enter artist"},
    "artist_terms": {"type": "input", "func": "like", "placeholder": "Enter terms"},
    "location": {"type": "input", "func": "like", "placeholder": "Enter location"},
    "lat": {"type": "number", "func": ">=", "placeholder": "Enter latitude (min)"},
    "lon": {"type": "number", "func": ">=", "placeholder": "Enter longitude (min)"},
    "tempo": {"type": "number", "func": ">=", "placeholder": "Enter tempo (min)"},
    "year": {"type": "number", "func": ">=", "placeholder": "Enter year (min)"},
}
formatters = {
    "index": NumberFormatter(format="0"),
    "lat": NumberFormatter(format="0.00000"),
    "lon": NumberFormatter(format="0.00000"),
    "tempo": NumberFormatter(format="0.000"),
    "year": NumberFormatter(format="0"),
}

msd_df = pd.read_csv(INPUT_FILE, converters={"artist_terms": lambda x: x.split(",")})
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

k_input = pn.widgets.IntInput(value=5, start=1, step=1, end=msd_df.shape[0], width=100)
toggle_group = pn.widgets.ToggleGroup(options=["year", "tempo", "lat", "lon", "artist_terms_matches"], value=["year", "tempo", "lat", "lon", "artist_terms_matches"])

@pn.depends(s=tab.param.selection, k=k_input, tg=toggle_group)
def output(s, k, tg):
    print(tg)
    if len(s) == 0:
        return "### Please select a song."
    elif not tg:
        return "### Please select at least one column used for prediction."
    elif len(s) == 1:
        return pn.widgets.Tabulator(
            recommendSongs(s[0], k, tg, msd_df),
            pagination="local",
            layout="fit_columns",
            page_size=10,
            sizing_mode="stretch_width",
            disabled=True,
            formatters=formatters,
        )
    else:
        return


template = pn.template.VanillaTemplate(title="Music Recommender", sidebar=[])
template.main.append(
    pn.Column(
        "# Songs",
        tab,
        "# Recommendations",
        pn.Row(k_input, toggle_group),
        output)
)
template.servable()
