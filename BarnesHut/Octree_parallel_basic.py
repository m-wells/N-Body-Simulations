from mpi4py import MPI
from Octree_common import Particle
from Octree_common import Cell
import InitialConditions
import Display

class Octree_parallel_basic:
  def __init__(self, comm, particles, newton_g, box_size, timestep, \
    tree_thres, softening):

    self.comm = comm
    self.rank = comm.Get_rank()
    self.size = comm.Get_size()

    self.particles = particles

    self.newton_g = newton_g
    self.box_size = box_size
    self.timestep = timestep
    self.tree_thres = tree_thres
    self.softening = softening

    self.timings = {"tree": 0, "broadcast": 0, "force": 0, "gather": 0}

  def evolve(self):
    # CONSTRUCT TREE
    tree_start_time = MPI.Wtime()

    # tree construction only occurs on home process
    root = None
    if self.rank == 0:
      root = Cell(-self.box_size, self.box_size, -self.box_size, \
        self.box_size, -self.box_size, self.box_size, "0")
      for particle in self.particles:
        root.add(particle) 

    tree_end_time = MPI.Wtime()
    if self.rank == 0:
      self.timings["tree"] += tree_end_time - tree_start_time

    # BROADCAST TREE TO ALL PROCESSES
    bcast_start_time =  MPI.Wtime()
    root = self.comm.bcast(root, root = 0)
    bcast_end_time =  MPI.Wtime()
    if self.rank == 0:
      self.timings["broadcast"] += bcast_end_time - bcast_start_time


    # CALCULATE FORCE
    force_start_time =  MPI.Wtime()
    # get particles from tree
    self.particles = root.particles()

    # decide how to distribute particles
    nparticles = len(self.particles) / self.size
    extras = len(self.particles) % self.size
    if self.rank < extras:
      start = self.rank * (nparticles + 1)
      end = start + nparticles + 1
    else:
      start = self.rank * nparticles + extras
      end = start + nparticles
    myparticles = self.particles[start:end]

    # each process only propagates its own particles
    for particle in myparticles:
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

    force_end_time =  MPI.Wtime()
    if self.rank == 0:
      self.timings["force"] += force_end_time - force_start_time

    # GATHER PARTICLES
    gather_start_time =  MPI.Wtime()
    # particles gathered to home processes
    particlelists = self.comm.gather(myparticles, root = 0)
    if self.rank == 0:
      # concatenate particlelists into single list of particles
      # for home process to use in tree construction next time step
      self.particles = []
      for particlelist in particlelists:
        self.particles.extend(particlelist)
    gather_end_time =  MPI.Wtime()
    if self.rank == 0:
      self.timings["gather"] += gather_end_time - gather_start_time
