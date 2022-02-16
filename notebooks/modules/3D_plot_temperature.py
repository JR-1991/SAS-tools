# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 12:54:02 2022

@author: Selly
"""

import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


path = 'C:/Users/Selly/Documents/Uni/INF_Project/measurement_data/OTAC/OTAC70wt%_T/desmeared'
meas_files = [i for i in os.listdir(path) if i.endswith('[7].pdh')]
meas_files.sort(reverse=True)

temperatures = [t for t in range(10,91,1)]
temperatures.sort(reverse=True)

cmap = mpl.cm.inferno.reversed()
n_meas = 82

    
fig = plt.figure()
ax = plt.axes(projection ='3d')
ax.figure.set_size_inches(10,10)
ax.set_xlabel('$q$ / $\mathrm{nm}^{-1}$')
ax.xaxis.set_ticks([0,1,2,3,4,5,6,7])
ax.set_ylabel('$T$ / °C')
ax.set_ylim(0,100)
ax.set_zlabel('$I$ / $a.u.$')


for measurement in range(len(temperatures)):
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
    temperature = []
    counts_per_area = data['I']

    for data_points in range(len(scattering_vector)):
        temperature.insert(data_points, temperatures[measurement])

    ax.plot(scattering_vector,
            temperature,
            counts_per_area,
            marker=',',
            color=cmap(measurement / float(n_meas)))

plt.show()

    



