#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: plot.py
# Created: 2014-04-30 by gks 
"""
Description: 
"""
import os, sys
import matplotlib.pyplot as plt
import random
import numpy
import scipy
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



name_x = "2part_mov_x.csv"
name_y = "2part_mov_y.csv"
#name_z = "2part_mov_z.csv"
data_x = loadtxt(name_x,comments="#",delimiter=",",usecols=(0,1))
data_y = loadtxt(name_y,comments="#",delimiter=",",usecols=(0,1))
#data_z = loadtxt(name_z,comments="#",delimiter=",",usecols=(0,1))


#-------------------------------------------------

#------------Figure Layout--------------
#twofig
##One Figure

n_timesteps = len(data_x[:,0])
print(n_timesteps)
#PLOT

files = []
fig = plt.figure()
ax = fig.add_subplot(111)
adjustprops = dict(left=0.19,bottom=0.15,right=0.92,top=0.9,wspace=0.,hspace=0.2)
fig.subplots_adjust(**adjustprops)    
ax.set_xlabel(r'$x$',size="x-large")
ax.set_ylabel(r'$y$',size="x-large")
ax.minorticks_on()
ax.grid()
#ax.scatter(data_x[:,0],data_y[:,0],color="blue",marker=".",linewidth=1,linestyle="-",label="x")
#ax.scatter(data_x[:,1],data_y[:,1],color="green",marker=".",linewidth=1,linestyle="-",label="x")
#ax.plot(data_x[:,2],data_y[:,2],color="red",marker=".",linewidth=1,linestyle="-",label="x")

#fig.savefig("movie.pdf")
#For every kth  frame:
k = 1
for i in range(0,n_timesteps,k):  
    print(i)
    ax.set_xlim(-100000,100000)
    ax.set_ylim(-100000,100000)
    print(data_x[i,0],data_y[i,0])
    print(data_x[i,1],data_y[i,1])
    ax.plot(data_x[i,0],data_y[i,0],color="blue",marker=".",markersize=16,linewidth=0,linestyle="-",label=r"$M_1=100$")
    ax.plot(data_x[i,1],data_y[i,1],color="green",marker=".",markersize=16,linewidth=0,linestyle="-",label=r"$M_1=100$")
    legend(loc="lower right",prop={'size':16})
    #ax.plot(data_x[i,2],data_y[i,2],color="red",marker=".",linewidth=1,linestyle="-",label="x")
    fname = '_tmp%0005d.png'%i
    print 'Saving frame', fname
    fig.savefig(fname)
    files.append(fname)
    ax.clear()

print 'Making movie animation.mpg - this make take a while'
os.system("mencoder 'mf://_tmp*.png' -mf type=png:fps=10 -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o animation.mpg")
os.system("rm *.png")


#fig21
#fig12
#fig13
#---------------------------------------


#FITTING------------------------------------------
#polyfit
#optimize

#-------------------------GRAPHICS
#legend((u'',u'<++>'),loc='upper right')
#legend(loc="lower right",prop={'size':16})


#changeticks
#tickRotate
#intTick

#MISC
#plt.ticklabel_format(style="sci",scilimits=(1,2),axis="y")

#ANNOTATE
#ax.annotate(r'$M_r$', xy=(0, 2),  xycoords='data',
#                xytext=(-50, 30), textcoords='data',
#                arrowprops=dict(arrowstyle="->"))
#bx.annotate(r'$\chi^2=0.46$', xy=(750, 0.03),xytext=None, textcoords='data',arrowprops=None)




#SAVING
#fig.savefig("movie.pdf")


