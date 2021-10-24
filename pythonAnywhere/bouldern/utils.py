import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import to_rgba_array

from bouldern.color_lookup import color_lookup
from bouldern.constants import FIGURES_DIR
from bouldern.gyms import gyms


def plot_boulder_identifiers(gym):
    gym_info = gyms[gym]
    ax, fig = plot_gym(gym)
    for _, section_info in gym_info['sections'].items():
        for i, coords in enumerate(section_info['walls'], 1):
            ax.text(*coords, i, ha='center', va='center', size=gym_info['font_size'])
    return ax, fig


def plot_gym(gym):
    fig, ax = plt.subplots()
    hallenplan = plt.imread(FIGURES_DIR.joinpath(gym).joinpath('hallenplan.png'))
    ax.imshow(hallenplan, extent=[0, hallenplan.shape[1], 0, hallenplan.shape[0]])
    ax.axis('off')
    return ax, fig


def merge_back_columns(df, prefix='Unnamed', new_name='wall'):
    cols_2_merge = df.columns[df.columns.str.startswith(prefix)]
    df[new_name] = df.loc[:, cols_2_merge].bfill(axis=1).iloc[:, 0]
    return df.drop(columns=cols_2_merge)
