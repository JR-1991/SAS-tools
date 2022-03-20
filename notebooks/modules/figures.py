import os
from pathlib import Path
from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd
from pyaniml import AnIMLDocument
from pydantic import validate_arguments

from modules.loggerfromjson import logger_from_json


logger = logger_from_json(Path(__file__).parents[2] / "logs/")
logger.name = __name__


def _create_figure(
    path_to_files: Union[str, bytes, os.PathLike],
    colormap: str,
    size_inches: Tuple[float, float] = (10, 10),
    x_label: str = "x",
    x_ticks: Optional[List[int]] = None,
    x_limit: Optional[Tuple[float, float]] = None,
    y_label: str = "y",
    y_ticks: Optional[List[int]] = None,
    y_limit: Optional[Tuple[float, float]] = None,
    z_label: str = "z",
    z_ticks: Optional[List[int]] = None,
    z_limit: Optional[Tuple[float, float]] = None,
    plot_marker: Optional[str] = None,
    plot_linestyle: Optional[str] = None,
) -> plt.Axes:

    files = list(Path(path_to_files).glob("*.pdh"))
    meas_files = [file for file in files if file.is_file()]
    meas_files.sort(reverse=True)
    n_meas = len(meas_files)

    figure = plt.axes(projection="3d")
    figure.figure.set_size_inches(list(size_inches))

    figure.set_xlabel(x_label)
    if x_ticks:
        figure.xaxis.set_ticks(x_ticks)
    if x_limit:
        figure.set_xlim(list(x_limit))

    figure.set_ylabel(y_label)
    if y_ticks:
        figure.yaxis.set_ticks(y_ticks)
    if y_limit:
        figure.set_ylim(list(y_limit))

    figure.set_zlabel(z_label)
    if z_ticks:
        figure.zaxis.set_ticks(z_ticks)
    if z_limit:
        figure.set_zlim(list(z_limit))

    cmap = plt.colormaps[colormap].reversed()
    temperature_list = [temperature for temperature in range(10, 91, 1)]

    for measurement in range(len(temperature_list)):
        # logger.debug(f"Adding {meas_files[measurement].stem} to figure.")
        data = pd.read_table(
            meas_files[measurement],
            delimiter="   ",
            usecols=[0, 1],
            names=["scattering_vector", "counts_per_area"],
            header=5,
            skipfooter=496,
            engine="python",
        )

        temperature_list.sort(reverse=True)
        temperature = [
            temperature_list[measurement]
            for _ in range(len(data["scattering_vector"]))
        ]

        figure.plot(
            data["scattering_vector"],
            temperature,
            data["counts_per_area"],
            marker=plot_marker,
            linestyle=plot_linestyle,
            color=cmap(measurement / float(n_meas)),
        )

    return figure


if __name__ == "__main__":
    this_file = Path(__file__)
    path_to_datasets = this_file.parents[1] / "datasets/"
    path_to_T_series = path_to_datasets / "raw/OTAC_temperature_series/"
    figure = _create_figure(
        path_to_T_series,
        colormap="inferno",
        x_label="$q$ / $\mathrm{nm}^{-1}$",
        x_ticks=[0, 1, 2, 3, 4, 5, 6, 7],
        y_label="$T$ / °C",
        y_limit=(0, 100),
        z_label="$I$ / $a.u.$",
    )
    plt.show()


# # Filter and sort list of files in directory
# files = path_to_c_series.glob("*.pdh")
# meas_files = [file for file in list(files) if file.is_file()]
# meas_files.sort(reverse=True)

# # Make and sort list of mass fractions
# mass_fractions = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# mass_fractions.sort(reverse=True)
# print(meas_files, mass_fractions)

# # Instantiate gist rainbow colormap for figure
# cmap = mpl.cm.gist_rainbow
# n_meas = 13

# # Instantiate figure
# fig = plt.figure()
# ax = plt.axes(projection="3d")
# ax.figure.set_size_inches(10, 10)
# ax.set_xlabel("$q$ / $\mathrm{nm}^{-1}$")
# ax.xaxis.set_ticks([0, 1, 2, 3, 4, 5, 6, 7])
# ax.set_ylabel("$x$ / wt%")
# ax.set_ylim(0, 100)
# ax.set_zlabel("$I$ / $a.u.$")

# # Add dataframes to figure incrementally to create 3D plot
# for measurement in range(len(mass_fractions)):
#     print(f"Adding {meas_files[measurement].stem} to figure.")

#     data = pd.read_table(
#         meas_files[measurement],
#         delimiter="   ",
#         usecols=[0, 1],
#         names=["q", "I"],
#         header=5,
#         skipfooter=496,
#         engine="python",
#     )

#     scattering_vector = data["q"]
#     mass_fraction = []
#     counts_per_area = data["I"]

#     for data_points in range(len(scattering_vector)):
#         mass_fraction.insert(data_points, mass_fractions[measurement])

#     ax.plot(
#         scattering_vector,
#         mass_fraction,
#         counts_per_area,
#         linestyle="-",
#         marker=".",
#         color=cmap(measurement / float(n_meas)),
#     )

# plt.show()
