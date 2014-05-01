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

#files = []
#fig = plt.figure(figsize=(5,5))
#ax = fig.add_subplot(111)
#for i in range(50):  # 50 frames
#    ax.cla()
#    ax.imshow(numpy.random.random((5,5)), interpolation='nearest')
#    fname = '_tmp%03d.png'%i
#    print 'Saving frame', fname
#    fig.savefig(fname)
#    files.append(fname)
#
#print 'Making movie animation.mpg - this make take a while'
#os.system("mencoder 'mf://_tmp*.png' -mf type=png:fps=10 -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o animation.mpg")

name_x = "2part_mov_x.csv"
name_y = "2part_mov_y.csv"
name_z = "2part_mov_z.csv"
data_x = loadtxt(name_x,comments="#",delimiter=",",usecols=(0,1))
data_y = loadtxt(name_x,comments="#",delimiter=",",usecols=(0,1))
data_z = loadtxt(name_x,comments="#",delimiter=",",usecols=(0,1))




