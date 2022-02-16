# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 12:54:02 2022

@author: Selly
"""

import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


path = 'C:/Users/Selly/Documents/Uni/INF_Project/measurement_data/OTAC/2022-01-27'
meas_files = [i for i in os.listdir(path) if i.endswith('%.pdh')]
meas_files.sort(reverse=True)

mass_fractions = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
mass_fractions.sort(reverse=True)
print(meas_files, mass_fractions)

cmap = mpl.cm.gist_rainbow
n_meas = 13

    
fig = plt.figure()
ax = plt.axes(projection ='3d')
ax.figure.set_size_inches(10,10)
ax.set_xlabel('$q$ / $\mathrm{nm}^{-1}$')
ax.xaxis.set_ticks([0,1,2,3,4,5,6,7])
ax.set_ylabel('$x$ / wt%')
ax.set_ylim(0,100)
ax.set_zlabel('$I$ / $a.u.$')


for measurement in range(len(mass_fractions)):
    print(meas_files[measurement])
    
    data = pd.read_table(meas_files[measurement],
                         delimiter = '   ',
                         usecols=[0,1],
                         names = ['q', 'I'],
                         header=5,
                         skipfooter=496,
                         engine = 'python'
                         )
    
    scattering_vector = data['q']
    mass_fraction = []
    counts_per_area = data['I']

    for data_points in range(len(scattering_vector)):
        mass_fraction.insert(data_points, mass_fractions[measurement])

    ax.plot(scattering_vector,
            mass_fraction,
            counts_per_area,
            linestyle='-',
            marker='.',
            color=cmap(measurement / float(n_meas)))

plt.show()

    



