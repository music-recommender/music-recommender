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

    Hint: For debugging purposes, setting the path makes navigation much quicker and easier.
    """
    load_dotenv()
    MSD_PATH = os.environ.get("MSD_PATH")
    return pn.widgets.FileSelector(MSD_PATH)

file_selector = initialize_MSD_file_selector()


@pn.depends(file_selector)
def create_tabs_from_hdf5(file_selector):
    if len(file_selector) == 1:
        tabs = pn.Tabs()
        with h5py.File(file_selector[0], "r") as f:
            for group_name in f.keys():
                group_column = pn.Column()
                for key, value in f[group_name].items():
                    value_str = (
                        f"\nshape: {str(value.shape)}\n"
                        f"\ndtype: {str(value.dtype)}\n"
                        f"\nvalue:\n\n{str(value[:])}"
                    )
                    text_area = pn.widgets.TextAreaInput(
                        name=str(key),
                        value=value_str,
                        disabled=True,
                        width=1000,
                        height=250,
                    )
                    group_column.append(text_area)
                tabs.append((group_name, group_column))

        return tabs


template = pn.template.VanillaTemplate(title="Music Recommender", sidebar=[])
template.main.append(pn.Column(file_selector, create_tabs_from_hdf5))
template.servable()
