# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 18:23:47 2022

@author: Selly
"""

import os

import matplotlib.pyplot as plt
import pandas as pd


path_to_data = "C:/Users/Selly/Documents/Uni/INF_Project/measurement_data/OTAC/OTAC_measurement_data/plot_data_overview/"
files = [file for file in os.listdir(path_to_data) if file.endswith(".pdh")]

phase = ["$\mathrm{L}_{1}$", "$\mathrm{H}_{1}$", "$\mathrm{V}_{1}$", "$\mathrm{L}_{\u03B1}$", "cr"]
y_shift = [0, 0.25, 2, 10, 50]

fig = plt.figure()
ax = fig.add_subplot()
ax.set_xlabel("$q$ / $\mathrm{nm}^{-1}$")
ax.set_xlim(0,8)
ax.tick_params(which="both",
               left=False,
               labelleft=False
               )
ax.set_ylabel("log($I$ / $a.u.$)")
ax.set_ylim(0.01, 100000)
ax.set_yscale("log")

for index, file in enumerate(files):
    print(index, phase[index])
    data = pd.read_table(file,
                              delimiter = "   ",
                              usecols=[0,1],
                              names = ["q", "I"],
                              header=5,
                              skipfooter=496,
                              engine="python"
                              )
    plot_data = data[data["q"] >= 0.5]

    scattering_vector = plot_data["q"]
    counts_per_area = (((plot_data["I"]*(10**index)) + (y_shift[index]*index)))

    ax.plot(scattering_vector,
            counts_per_area,
            marker=",",
            linestyle="-",
            color="black",
            label = phase[index]
            )
    ax.text(7.5, (counts_per_area.iloc[-10]), phase[index])

plt.savefig("OTAC_overview_log.png")
plt.show()
