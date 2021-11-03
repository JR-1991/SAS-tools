import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from lmfit.models import LorentzianModel


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


# plot of SAXS data
def SAXSplt (pfad, label, color):
    a = pd.read_table(pfad, delimiter = '   ', usecols=[0,1], names = ['q', 'I'], header=5, skipfooter=496, engine = 'python')
    
    q = a['q']
    I = a['I']
    
    plt.plot(q, I, linestyle='-', marker=',', label = label, color = color)
    plt.yscale('log')          
    plt.xlabel('$q$ / $\mathrm{nm}^{-1}$')
    plt.ylabel('$I$ / a.u.')
    plt.xlim(0,5)
    plt.ylim(0.0001,2)    
    plt.legend(frameon=False)
    save_name = label + '.pdf'
    plt.savefig(save_name)
    plt.show()    

#calculation of lattice parameter (+ all intermediary values)
def SAXScalc(qCholpal, qSampleItem):
    dLit=[52.49824535,26.24912267,17.49941512] #literature d-values
    data = [] # list for writing to csv file
    
    qCholpalLit = [ScatteringVector(dLitItem) for dLitItem in dLit]
    
    slope, intercept = np.polyfit(qCholpal, qCholpalLit, 1)  # linear fit measured vs. literature q-values
        
    qKorr = [LinReg(slope, i, intercept) for i in qSampleItem]
    
    dMeas = [LatticePlane(qKorrItem) for qKorrItem in qKorr]
    data.append(dMeas)
    
    dRatio = [LatticeRatio(dMeasItem, dMeas[0]) for dMeasItem in dMeas[1:]]
    data.append(dRatio)
    
    if IsHexagonal(dRatio) == True:
        h = [1,1,2,2,3]
        k = [0,1,0,1,0]
        a_hex = []
        for i, dMeasItem in enumerate(dMeas):
            a_i = HexagonalLatticeParameter(dMeas[i], h[i], k[i])
            a_hex.append(a_i)
        a = ['hexagonal', (np.mean(a_hex))]
        data.append(a)
        
    elif IsCubic(dRatio) == True:
        h = [1,1,2,2,2]
        k = [0,1,0,1,2]
        l = [0,1,0,1,2]
        a_cub = []
        for i, dMeasItem in enumerate(dMeas):
            a_i = CubicLatticeParameter(dMeas[i], h[i], k[i], l[i])
            a_cub.append(a_i)
        a = ['cubic', (np.mean(a_cub))]
        data.append(a)
        
    elif IsLamellar(dRatio) == True:
        print('lamellar')
        
    else:
        a = ['not determinable', '-']
        data.append(a)
        
    return data

# Test if hexagonal, cubic oder lamellar
def IsHexagonal(arbList):
    H1 = [(1/np.sqrt(3)), (1/np.sqrt(4)), (1/np.sqrt(7)), (1/np.sqrt(9))]
    for i, arbListItem in enumerate(arbList):
        if (abs(arbList[i]-H1[i])) < 0.03:
            hexagonal = True
        else: 
            hexagonal = False
    return hexagonal
        

def IsCubic(arbList):
    Q = [(1/np.sqrt(2)), (1/np.sqrt(3)), (1/np.sqrt(4)), (1/np.sqrt(5))]
    i=0
    for i, arbListItem in enumerate(arbList):
        if (abs(arbList[i]-Q[i])) < 0.03:
            cubic = True
        else:
            cubic = False
    return cubic


def IsLamellar(arbList):
    L = [(1/2), (1/3), (1/4), (1/5)]
    for i, ArbListItem in enumerate(arbList):
        if (abs(arbList[i]-L[i])) < 0.03:
            lamellar = True
        else:
            lamellar = False
    return lamellar
        

def HexagonalLatticeParameter(d, h, k):
    a_hex = (d*((h + k + (h * k))*(np.sqrt(4/3))))
    return a_hex

def CubicLatticeParameter(d, h, k, l):
    a_cub = (d*(np.sqrt((h**2)+(k**2)+(l**2))))
    return a_cub

def LinReg(m, x, b):
    y = m*x + b
    return y

def ScatteringVector(d):
    q = (2*np.pi)/(d/10)
    return q

def LatticePlane(q):
    d = (2*np.pi)/q
    return d

def LatticeRatio(d, d_0):
    d_ratio = d/d_0
    return d_ratio