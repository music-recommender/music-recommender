"""
Run server via terminal with command:

panel serve msd_viewer.py

"""


import h5py
import panel as pn

pn.extension()

file_selector = pn.widgets.FileSelector("~")


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
