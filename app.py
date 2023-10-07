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

msd_df = pd.read_csv(INPUT_FILE)
tab = pn.widgets.Tabulator(
    msd_df,
    pagination="local",
    layout="fit_columns",
    page_size=10,
    sizing_mode="stretch_width",
    header_filters=filters,
    disabled=True,
    selectable='checkbox',
    frozen_rows=[]
)

output_column = pn.Column()
run_button = pn.widgets.Button(icon='run', button_type='primary', name='Run', width=100)
reset_button = pn.widgets.Button(icon='trash', button_type='danger', name='Reset', width=100)

@pn.depends(s=tab.param.selection, watch=True)
def selection_callback(s):
    tab.frozen_rows = s

@pn.depends(r=reset_button, watch=True)
def reset(r):
    output_column.clear()
    tab.selection = []
    tab.value = msd_df


@pn.depends(b=run_button, watch=True)
def run(b):
    return output_column

template = pn.template.VanillaTemplate(title="Music Recommender", sidebar=[])
template.main.append(
    pn.Column(
        "# Songs",
        tab,
        pn.Row(run_button, reset_button),
        output_column
    )
)
template.servable()
