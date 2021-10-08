# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 15:15:59 2021

@author: Selly
"""

################################
#### import needed packages ####
################################

from lmfit.models import LorentzianModel
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



#################################
#### define needed functions ####
#################################

def lorentzian( y0, a, w, x, xc ):
    # y0=offset, xc=center, w=FWHM, a=area
    return y0 + (2*a/np.pi)*(w/(4*(x-xc)^2 + w^2))

def LorentzFit (x, y, fig, add, q):
    model = LorentzianModel()

    params = model.guess(y, x=x)
    result = model.fit(y, params, x=x)
    res_fit = []

    for item in (result.fit_report()).split():
       try:
            res_fit.append(float(item))
       except ValueError:
            pass
        
    q.append(res_fit[9])
    
    add.plot(x, result.best_fit, linestyle = ':', color = 'blue', label = 'best fit')

    return q


##################################
#### import needed input data ####
##################################

path = 'C:/Users/Selly/Documents/Uni/4_Semester/Masterarbeit/Python/Lorentzian' 
a = pd.read_table('CholPal_210713[7].pdh', delimiter = '   ', usecols=[0,1], names = ['q', 'I'], header=5, skipfooter=496, engine = 'python')
q = a['q']
I = a['I']

# peak 1: 1.0<q<1.3 // peak 2: 1.5<q<3 // peak 3: 3<q<4

a1_idx = a.index[(a['q'] > 0.6) & (a['q'] < 1.5)].tolist()
a1 = a.loc[a1_idx]
q1 = np.array(a1['q'].tolist())
I1 = np.array(a1['I'].tolist())

a2_idx = a.index[(a['q'] > 1.5) & (a['q'] < 3)].tolist()
a2 = a.loc[a2_idx]
q2 = np.array(a2['q'].tolist())
I2 = np.array(a2['I'].tolist())

a3_idx = a.index[(a['q'] > 3) & (a['q'] < 4)].tolist()
a3 = a.loc[a3_idx]
q3 = np.array(a3['q'].tolist())
I3 = np.array(a3['I'].tolist())


#########################
#### actual code ... ####
#########################  

qCholpal = []

fig = plt.figure()
add = fig.add_subplot(1,1,1)
add.plot(q,I, marker = ',', color = 'orange', label = 'diffractogram')

plt.xlabel('$q$ / $\mathrm{nm}^{-1}$')
plt.ylabel('$I$ / a.u.')
plt.xlim(0,5)
plt.ylim(0, (max(I)+(0.1*max(I))))

LorentzFit(q1,I1, fig, add, qCholpal)
plt.legend(frameon=False)
LorentzFit(q2,I2, fig, add, qCholpal)
LorentzFit(q3,I3, fig, add, qCholpal)

plt.show()

print(qCholpal)

