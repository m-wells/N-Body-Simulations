import time
from Octree_common import Particle
from Octree_common import Cell
import InitialConditions
import Display

class Octree_serial:
  def __init__(self, particles, newton_g, box_size, timestep, tree_thres, \
    softening):

    self.particles = particles

    self.newton_g = newton_g
    self.box_size = box_size
    self.timestep = timestep
    self.tree_thres = tree_thres
    self.softening = softening

    self.timings = {"tree": 0, "force": 0}

  def evolve(self):
    # CONSTRUCT TREE
    tree_start_time = time.time()

    root = Cell(-self.box_size, self.box_size, -self.box_size, self.box_size, \
      -self.box_size, self.box_size, "0")
    for particle in self.particles:
      root.add(particle) 

    tree_end_time = time.time()
    self.timings["tree"] += tree_end_time - tree_start_time

    # CALCULATE FORCE
    force_start_time =  time.time()
    # get particles from tree
    self.particles = root.particles()

    # for each particle,
    for particle in self.particles:
      # traverse the tree, starting from the root node
      # start a queue with just root node
      cells = [root]
      while cells:
        # take the next cell
        cell = cells.pop()
        # if this cell is far enough, use it
        if cell.meetscriterion(particle, self.tree_thres, self.softening):
          if cell.n > 0:
            particle.kick(cell, self.newton_g, self.timestep, self.softening)
        # otherwise, try its daughters
        else:
          cells.extend(cell.daughters)
      # drift the particle to the next time step
      particle.drift(self.timestep)

    force_end_time =  time.time()
    self.timings["force"] += force_end_time - force_start_time
