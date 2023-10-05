import panel as pn
import pandas as pd

pn.extension("tabulator")

INPUT_FILE = "data/song_info.csv"

filters = {
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
    "danceability": {
        "type": "number",
        "func": ">=",
        "placeholder": "Enter minimum danceability",
    },
    "tempo": {
        "type": "number",
        "func": ">=",
        "placeholder": "Enter minimum tempo"
    },
    "year": {
        "type": "number",
        "func": "=",
        "placeholder": "Enter year"},
}

tab = pn.widgets.Tabulator(
    pd.read_csv(INPUT_FILE),
    pagination="remote",
    layout="fit_columns",
    page_size=10,
    sizing_mode="stretch_width",
    header_filters=filters,
    selectable="checkbox"
)

run_button = pn.widgets.Button(name='\u25b6', width=100, height=100)

@pn.depends(b=run_button)
def run(b):
    if len(tab.selection) == 0:
        return
    return tab.value.iloc[tab.selection]

template = pn.template.VanillaTemplate(title="Music Recommender", sidebar=[])
template.main.append(
    pn.Column(
        "# Songs",
        tab,
        run_button,
        run
    )
)
template.servable()
