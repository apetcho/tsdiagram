#!/usr/bin/env python
#-*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import gsw

def ts(salt, temp, p=0, **kw):
    """
    Plot a Temperature-Salinity diagram (a.k.a TS-diagram).

    Argument
    --------
        salt : Absolute salinity (in PSU), numpy array or python list
        temp : Conservative temperaure (in  degree C), numpy array or python list
        p    : sea pressure (in dbar),[ i.e. absolute pressure - 10.1325 dbar ]
               This is scalar value.

    Options
    -------
        rholevels: numpy.array object or python list. A series of scalar value of
            density anomaly contours to be displayed  on the TS-diagram.

    Author
    ------
        Eyram K. Apetcho

    License
    -------
        BSD License, See the license
    """
    salt = np.array(salt)
    temp = np.array(temp)
    p    = np.array(p)
    rholevels = kw.pop('rholevels', None)
    if len(salt.shape) == 2 and len(temp.shape)==2:
        ms, ns = salt.shape
        mt, nt = temp.shape
        if not ((ms == mt) and ( ns == nt)):
            raise ValueError(''' The first two input must at most 2D arrays of
            same shape''')
        salt = salt.reshape((ms*ns, ))
        temp = temp.reshape((mt*nt, ))
    elif len(salt.shape) > 2 or len(temp.shape) > 2:
        raise ValueError('''I don't know how to handle array of more 2
        dimensions ''')

    smin = np.nanmin(salt) - 0.01 * np.nanmin(salt)
    smax = np.nanmax(salt) + 0.01 * np.nanmax(salt)
    tmin = np.nanmin(temp) - 0.1 * np.nanmin(temp)
    tmax = np.nanmax(temp) - 0.1 * np.nanmax(temp)

    xdim = int(np.round((smax - smin)/0.1 + 1))
    ydim = int(np.round((tmax - tmin) + 1))

    # Remove NaNs from the input data sets.
    #n_elts, = salt.shape
    #new_temp= np.nan * np.zeros(temp.shape)
    #new_salt= np.nan * np.zeros(salt.shape)

    #for i in range(n_elts):


    rho  = np.zeros((ydim, xdim))
    tempi= np.linspace(0, ydim-1, ydim) + tmin
    salti= np.linspace(0, xdim-1, xdim)*0.1 + smin

    x , y = np.meshgrid( salti, tempi)

    rho = gsw.rho(x, y, p*np.ones(x.shape)) - 1000

    if rholevels is None:
        cs = plt.contour(x, y, rho, colors='k',linestyles='dashed',
                         linewidths=2)
    else:
        rholevels = np.array(rholelvels)
        cs = plt.contour(x, y, rho, rholevels, colors='k', linestyles='dashed',
                         linewidths=2)
    plt.clabel(cs, inline=True, colors='b', fmt='%.2f')
    plt.xlabel(r' Salinity $(PSU)$')
    plt.ylabel(r' Temperature $ (^\circ C) $')
    plt.hold(True)
    plt.plot(salt, temp, 'or', markersize=9)
    #plt.scatter(salt, temp)

if __name__ == '__main__':
    fname ='tsdata.npz'
    fd = np.load(fname)
    temp = fd['temp']
    salt = fd['salt']
    fd.close()
    ts(salt, temp)
    plt.savefig('tsplot', bbox_inches='tight')
    plt.show()
