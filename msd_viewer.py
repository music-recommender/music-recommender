"""
Run server via terminal with command:

panel serve msd_viewer.py

"""

import os
import h5py
import panel as pn
from dotenv import load_dotenv

pn.extension()


def initialize_MSD_file_selector():
    """
    Read Million Song Dataset's folder location from an env-file ("MSD_PATH").

    If "MSD_PATH" is not set or env-file is missing, the FileSelector interprets None value as "~".

    Hint: For debugging purposes, setting the path makes navigation much
    quicker and easier.
    """
    load_dotenv()
    MSD_PATH = os.environ.get("MSD_PATH")
    return pn.widgets.FileSelector(MSD_PATH)


file_selector = initialize_MSD_file_selector()


def read_MSD_file_data(path):
    data = {}
    with h5py.File(path, "r") as f:
        for group_key in f.keys():
            data[group_key] = {}
            for key, value in f[group_key].items():
                data[group_key][key] = {
                    "shape": value.shape,
                    "dtype": value.dtype,
                    "data": value[:],
                }

    return data


def create_MSD_tabs(data):
    tabs = pn.Tabs()
    for group_key, group in data.items():
        group_column = pn.Column()
        for key, value in group.items():
            group_column.append(
                pn.Column(
                    f"## {key}",
                    pn.layout.Divider(),
                    f"### shape:\n{value['shape']}",
                    f"### dtype:\n{value['dtype']}",
                    f"### data:",
                    pn.widgets.TextAreaInput(
                        value=str(value["data"]), disabled=True, width=1000, height=250
                    ),
                )
            )
        tabs.append((group_key, group_column))

    return tabs


@pn.depends(file_selector)
def handle_file_selection(file_selector):
    if len(file_selector) == 1:
        file_data = read_MSD_file_data(file_selector[0])
        tabs = create_MSD_tabs(file_data)
        return tabs


template = pn.template.VanillaTemplate(title="Music Recommender", sidebar=[])
template.main.append(pn.Column(file_selector, handle_file_selection))
template.servable()
