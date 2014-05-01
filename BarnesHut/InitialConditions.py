import numpy as np
import random
from Octree_common import Particle

# seed the RNG to give the same Plummer initial conditions
def seed():
  random.seed("this is a seed for timing purposes")

# Plummer sphere with N solar mass stars, scale radius a parsecs
def plummersphere(N, a, NEWTON_G):
  x, y, z = [], [], []
  vx, vy, vz = [], [], []
  nstars = 0
  while nstars < N:
    # Sample radius from cumulative mass distribution
    radius = a / np.sqrt(random.random()**(-2/3) - 1)
    # Sample velocity magnitude through inversion sampling from velocity
    # distribution
    xx = random.random()
    yy = random.random()*0.1
    if yy < xx**2 * (1-xx**2)**3.5: # the star is added to the sample
      nstars += 1
      vmag = xx * np.sqrt(2*NEWTON_G*N)*(radius**2+a**2)**(-0.25)
        # N = total mass by construction
      # Calculate location coordinates
      phi = random.random()*2*np.pi
      theta = np.arccos(random.random() * 2 - 1)
      x.append(radius*np.sin(theta)*np.cos(phi))
      y.append(radius*np.sin(theta)*np.sin(phi))
      z.append(radius*np.cos(theta))
      # Calculate velocity coordinates
      phi = random.random()*2*np.pi
      theta = np.arccos(random.random() * 2 - 1)
      vx.append(vmag*np.sin(theta)*np.cos(phi))
      vy.append(vmag*np.sin(theta)*np.sin(phi))
      vz.append(vmag*np.cos(theta))
  return [Particle(x[i], y[i], z[i], vx[i], vy[i], vz[i], str(i)) \
    for i in xrange(N)]

# two body problem with orbit semimajor axis a, eccentricity e
def kepler(a, e, NEWTON_G):
  rmin = a * (1-e) #periastron
  h = (rmin * (1+e) * NEWTON_G * 2)**0.5 #angular momentum
  v = h/rmin
  return [Particle(rmin/2., 0, 0, 0, 0, v/2., "A"), \
    Particle(-rmin/2., 0, 0, 0, 0, -v/2., "B")]

# four body problem with inner semimajor axis a1, eccentricity e1
#                        outer semimajor axis a2, eccentricity e2
def doublekepler(a1, e1, a2, e2, NEWTON_G):
  particles = kepler(a1, e1, NEWTON_G) #inner binary
  rmin = a2 * (1-e2) #outer periastron
  h = (rmin * (1+e2) * 9 * NEWTON_G * 2)**0.5 #outer angular momentum
    # 9 because +1 from other outer binary, and inner binary is twice as close
    # (x4) and is composed of two stars (x2), giving +8
  v = h/rmin
  particles.extend([Particle(rmin/2., 0, 0, 0, 0, v/2., "C"), \
    Particle(-rmin/2., 0, 0, 0, 0, -v/2., "D")]) #outer binary
  return particles
