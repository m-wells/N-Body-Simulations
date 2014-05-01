#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: plot_ii_rcc.py
# Created: 2014-04-27 by gks 
"""
Description: Plot .txt
"""
import numpy as np
from pylab import *
from scipy import *
import matplotlib.pyplot as plt
import scipy.constants as const
from scipy import optimize
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm

#---------------------FONT and other graphics------------------------
font = {'family'         : 'serif',
	'weight'         : 'bold',
	'size'	         : 16}
matplotlib.rc('font',**font)
matplotlib.rc('grid',linewidth=1)
matplotlib.rc('xtick.major',width=2)
matplotlib.rc('xtick.major',size=7)
matplotlib.rc('xtick.minor',width=2)
matplotlib.rc('xtick.minor',size=4)
matplotlib.rc('ytick.major',width=2)
matplotlib.rc('ytick.major',size=7)
matplotlib.rc('ytick.minor',width=2)
matplotlib.rc('ytick.minor',size=4)

#-------------------------------------------------

#plotall

#---------------------DATA------------------------
name='bm_N_nT_1.txt'
data = loadtxt(name,comments="#",usecols=(0,1))

timesteps = data[:,0]
time = data[:,1]
#gflops = data[:,2]
#serial_time = time[0] #seconds
#speedup = serial_time/time

#-------------------------------------------------

#------------Figure Layout--------------
#twofig
#



##PLOT 1
##One Figure
#fig = plt.figure()
#ax = fig.add_subplot(111)
#adjustprops = dict(left=0.19,bottom=0.15,right=0.92,top=0.9,wspace=0.,hspace=0.2)
#fig.subplots_adjust(**adjustprops)    
#ax.set_xlabel(r'Thread number',size="x-large")
#ax.set_ylabel(r'GFLOP/s',size="x-large")
##ax.set_xlim()
##ax.set_ylim()
#ax.minorticks_on()
#ax.grid()
##PLOT
#ax.plot(numprocs,gflops,color="blue",linewidth=3,linestyle="-",label="GFLOP/s")
#ax.legend(loc="upper left",prop={'size':16})
#fig.savefig("ii_rcc_gflops.pdf")

#PLOT 2
#One Figure
fig = plt.figure()
ax = fig.add_subplot(111)
adjustprops = dict(left=0.19,bottom=0.15,right=0.92,top=0.9,wspace=0.,hspace=0.2)
fig.subplots_adjust(**adjustprops)    
ax.set_xlabel(r'Timesteps N',size="x-large")
ax.set_ylabel(r'Time (s)',size="x-large")
ax.set_xlim(10,5e6)
#ax.set_ylim()
ax.set_xscale('log')
ax.set_yscale('log')
ax.minorticks_on()
ax.grid()
#PLOT
ax.plot(timesteps,time,color="blue",marker="D", markersize=8,linewidth=3,linestyle="-",label="Serial; #Particles=49")
ax.set_title("Serial scaling with timesteps N")
ax.legend(loc="upper left",prop={'size':16})
fig.savefig("bm_N_nT_1.pdf")
fig.savefig("bm_N_nT_1.png")

##PLOT 3
##One Figure
#fig = plt.figure()
#ax = fig.add_subplot(111)
#adjustprops = dict(left=0.19,bottom=0.15,right=0.92,top=0.9,wspace=0.,hspace=0.2)
#fig.subplots_adjust(**adjustprops)    
#ax.set_xlabel(r'Thread number',size="x-large")
#ax.set_ylabel(r'Speedup',size="x-large")
##ax.set_xlim()
##ax.set_ylim()
#ax.minorticks_on()
#ax.grid()
##PLOT
#ax.plot(numprocs,speedup,color="blue",linewidth=3,linestyle="-",label="Speeedup")
#ax.legend(loc="upper left",prop={'size':16})
#fig.savefig("ii_rcc_speedup.pdf")






