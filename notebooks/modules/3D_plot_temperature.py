"""
Created on Tue Feb 15 12:54:02 2022

@author: Selly
"""


from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


# Create Path objects for this script
CWD = Path.cwd()
path_to_datasets = CWD / "notebooks/datasets/"
path_to_T_series = path_to_datasets / "raw/OTAC_temperature_series/"

# Filter and sort list of files in directory
files = path_to_T_series.glob("*.pdh")
meas_files = [file for file in list(files) if file.is_file()]
meas_files.sort(reverse=True)
print(meas_files)

# Make and sort list of temperatures
temperatures = [temperature for temperature in range(10, 91, 1)]
temperatures.sort(reverse=True)

# Instantiate inferno colormap for figure
cmap = mpl.cm.inferno.reversed()
n_meas = 82

# Instantiate figure
fig = plt.figure()
ax = plt.axes(projection="3d")
ax.figure.set_size_inches(10, 10)
ax.set_xlabel("$q$ / $\mathrm{nm}^{-1}$")
ax.xaxis.set_ticks([0, 1, 2, 3, 4, 5, 6, 7])
ax.set_ylabel("$T$ / °C")
ax.set_ylim(0, 100)
ax.set_zlabel("$I$ / $a.u.$")

# Add dataframes to figure incrementally to create 3D plot
for measurement in range(len(temperatures)):
    print(f"Adding {meas_files[measurement].stem} to figure.")

    data = pd.read_table(
        meas_files[measurement],
        delimiter="   ",
        usecols=[0, 1],
        names=["q", "I"],
        header=5,
        skipfooter=496,
        engine="python",
    )

    scattering_vector = data["q"]
    temperature = []
    counts_per_area = data["I"]

    for data_points in range(len(scattering_vector)):
        temperature.insert(data_points, temperatures[measurement])

    ax.plot(
        scattering_vector,
        temperature,
        counts_per_area,
        marker=",",
        color=cmap(measurement / float(n_meas)),
    )

plt.show()
