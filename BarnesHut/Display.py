import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# interactive mode for matplotlib
plt.ion()

# calculate total energy of a particle distribution
def energy(particles, newton_g):
  # kinetic energy
  ke = 0.5 * sum([particle.vx*particle.vx + particle.vy*particle.vy + \
    particle.vz*particle.vz for particle in particles])
  # accumulate potential energy from all particle pairs
  pe = 0
  for particle1 in particles:
    for particle2 in particles:
      if particle1 != particle2:
        rx = particle1.x - particle2.x
        ry = particle1.y - particle2.y
        rz = particle1.z - particle2.z
        r = (rx*rx + ry*ry + rz*rz)**0.5
        # 0.5 to account for double counting
        pe -= 0.5 * newton_g / r
  # total energy
  return ke + pe

# display particle positions in a 3D matplotlib window
def position_display(particles, disp_size, title):
  # extract coordinates
  x = [particle.x for particle in particles]
  y = [particle.y for particle in particles]
  z = [particle.z for particle in particles]

  fig = plt.figure(1)
  plt.clf()
  ax = Axes3D(fig)
  ax.set_xlabel("x [pc]")
  ax.set_ylabel("y [pc]")
  ax.set_zlabel("z [pc]")
  ax.set_title(title)
  ax.scatter(x,y,z)
  ax.set_xlim3d([-disp_size,disp_size])
  ax.set_ylim3d([-disp_size,disp_size])
  ax.set_zlim3d([-disp_size,disp_size])
  plt.draw()
