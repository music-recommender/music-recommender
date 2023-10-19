importScripts("https://cdn.jsdelivr.net/pyodide/v0.23.4/pyc/pyodide.js");

function sendPatch(patch, buffers, msg_id) {
  self.postMessage({
    type: 'patch',
    patch: patch,
    buffers: buffers
  })
}

async function startApplication() {
  console.log("Loading pyodide!");
  self.postMessage({type: 'status', msg: 'Loading pyodide'})
  self.pyodide = await loadPyodide();
  self.pyodide.globals.set("sendPatch", sendPatch);
  console.log("Loaded!");
  await self.pyodide.loadPackage("micropip");
  const env_spec = ['https://cdn.holoviz.org/panel/1.2.3/dist/wheels/bokeh-3.2.1-py3-none-any.whl', 'https://cdn.holoviz.org/panel/1.2.3/dist/wheels/panel-1.2.3-py3-none-any.whl', 'pyodide-http==0.2.1', 'bleach==6.1.0', 'bokeh==3.2.2', 'certifi==2023.7.22', 'charset-normalizer==3.3.0', 'contourpy==1.1.1', 'idna==3.4', 'Jinja2==3.1.2', 'joblib==1.3.2', 'linkify-it-py==2.0.2', 'Markdown==3.5', 'markdown-it-py==3.0.0', 'MarkupSafe==2.1.3', 'mdit-py-plugins==0.4.0', 'mdurl==0.1.2', 'numpy==1.26.1', 'packaging==23.2', 'pandas==2.1.1', 'panel==1.2.3', 'param==1.13.0', 'Pillow==10.1.0', 'python-dateutil==2.8.2', 'pytz==2023.3.post1', 'pyviz_comms==3.0.0', 'PyYAML==6.0.1', 'requests==2.31.0', 'scikit-learn==1.3.1', 'scipy==1.11.3', 'six==1.16.0', 'threadpoolctl==3.2.0', 'tornado==6.3.3', 'tqdm==4.66.1', 'typing_extensions==4.8.0', 'tzdata==2023.3', 'uc-micro-py==1.0.2', 'urllib3==2.0.7', 'webencodings==0.5.1', 'xyzservices==2023.10.0']
  for (const pkg of env_spec) {
    let pkg_name;
    if (pkg.endsWith('.whl')) {
      pkg_name = pkg.split('/').slice(-1)[0].split('-')[0]
    } else {
      pkg_name = pkg
    }
    self.postMessage({type: 'status', msg: `Installing ${pkg_name}`})
    try {
      await self.pyodide.runPythonAsync(`
        import micropip
        await micropip.install('${pkg}');
      `);
    } catch(e) {
      console.log(e)
      self.postMessage({
	type: 'status',
	msg: `Error while installing ${pkg_name}`
      });
    }
  }
  console.log("Packages loaded!");
  self.postMessage({type: 'status', msg: 'Executing code'})
  const code = `
  
import asyncio

from panel.io.pyodide import init_doc, write_doc

init_doc()

import panel as pn
import pandas as pd
from bokeh.models.widgets.tables import NumberFormatter
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

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
        return pn.widgets.Tabulator(
            recommendSongs(s, k, cbg, msd_df),
            pagination="local",
            layout="fit_columns",
            page_size=10,
            sizing_mode="stretch_width",
            disabled=True,
            formatters=formatters,
        )


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


await write_doc()
  `

  try {
    const [docs_json, render_items, root_ids] = await self.pyodide.runPythonAsync(code)
    self.postMessage({
      type: 'render',
      docs_json: docs_json,
      render_items: render_items,
      root_ids: root_ids
    })
  } catch(e) {
    const traceback = `${e}`
    const tblines = traceback.split('\n')
    self.postMessage({
      type: 'status',
      msg: tblines[tblines.length-2]
    });
    throw e
  }
}

self.onmessage = async (event) => {
  const msg = event.data
  if (msg.type === 'rendered') {
    self.pyodide.runPythonAsync(`
    from panel.io.state import state
    from panel.io.pyodide import _link_docs_worker

    _link_docs_worker(state.curdoc, sendPatch, setter='js')
    `)
  } else if (msg.type === 'patch') {
    self.pyodide.globals.set('patch', msg.patch)
    self.pyodide.runPythonAsync(`
    state.curdoc.apply_json_patch(patch.to_py(), setter='js')
    `)
    self.postMessage({type: 'idle'})
  } else if (msg.type === 'location') {
    self.pyodide.globals.set('location', msg.location)
    self.pyodide.runPythonAsync(`
    import json
    from panel.io.state import state
    from panel.util import edit_readonly
    if state.location:
        loc_data = json.loads(location)
        with edit_readonly(state.location):
            state.location.param.update({
                k: v for k, v in loc_data.items() if k in state.location.param
            })
    `)
  }
}

startApplication()