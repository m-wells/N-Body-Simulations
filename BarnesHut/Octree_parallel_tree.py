from mpi4py import MPI
from Octree_common import Particle
from Octree_common import Cell
import InitialConditions
import Display

class Octree_parallel_tree:
  def __init__(self, comm, particles, newton_g, box_size, timestep, tree_thres, softening):
    self.comm = comm
    self.rank = comm.Get_rank()
    self.size = comm.Get_size()

    self.particles = particles

    self.newton_g = newton_g
    self.box_size = box_size
    self.timestep = timestep
    self.tree_thres = tree_thres
    self.softening = softening

    self.timings = {"tree": 0, "tree_assembly": 0, "broadcast": 0, "force": 0, "allgather": 0}

  def evolve(self):
    # CONSTRUCT TREE BRANCHES
    tree_start_time = MPI.Wtime()
    # generate blank granddaughters (second level daughters)
    # do this on all processes because it's cheap
    root = Cell(-self.box_size, self.box_size, -self.box_size, self.box_size, \
      -self.box_size, self.box_size, "0")
    root.makedaughters() # daughters
    granddaughters = []
    for daughter in root.daughters: # granddaughters
      daughter.makedaughters()
      granddaughters.extend(daughter.daughters)
    # the ordering of cell.daughters from cell.makedaughters()
    # guarantees that every process agrees on the order of granddaughters

    # each process starts with the rank-th granddaughter and then gets
    # every size-th
    # spreads out the granddaughters that each process gets
    subgranddaughters = granddaughters[self.rank::self.size]

    # attempt to add all particles to our granddaughters
    # only those that actually belong will remain
    for particle in self.particles:
      for granddaughter in subgranddaughters:
        granddaughter.add(particle) 

    tree_end_time = MPI.Wtime()
    if self.rank == 0:
      self.timings["tree"] += tree_end_time - tree_start_time

    # ASSEMBLE BRANCHES INTO TREE
    tree_assembly_start_time =  MPI.Wtime()
    # gather the granddaughters to home process
    granddaughterlists = self.comm.gather(subgranddaughters, root = 0)
    # construct the tree on home process
    if self.rank == 0:
      granddaughters = [] 
      for granddaughterlist in granddaughterlists:
        granddaughters.extend(granddaughterlist)

      # prepare the new tree root and first level daughters
      root = Cell(-self.box_size, self.box_size, -self.box_size, \
        self.box_size, -self.box_size, self.box_size, "0")
      root.makedaughters()

      # take the prepared granddaughters, 8 at a time and
      # place them into the daughter they belong to
      # the ordering of the list granddaughters allows this
      for i, daughter in enumerate(root.daughters):
        mygranddaughters = granddaughters[i*8:(i+1)*8]
        daughter.assigndaughters(mygranddaughters)

      # recalculate the mass and center of mass of the root
      root.assigndaughters(root.daughters)
    tree_assembly_end_time = MPI.Wtime()
    if self.rank == 0:
      self.timings["tree_assembly"] += tree_assembly_end_time - tree_assembly_start_time

    # BROADCAST TREE TO ALL PROCESSES
    bcast_start_time = MPI.Wtime()
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

    # ALLGATHER PARTICLES
    gather_start_time =  MPI.Wtime()
    # all gather is used so that processes can start their tree branches
    # independently in the next time step
    particlelists = self.comm.allgather(myparticles)
    self.particles = []
    # concatenate particlelists into a single list of particles
    for particlelist in particlelists:
      self.particles.extend(particlelist)
    gather_end_time =  MPI.Wtime()
    if self.rank == 0:
      self.timings["allgather"] += gather_end_time - gather_start_time
