from mpi4py import MPI
from Octree_serial import Octree_serial as Octree_serial
from Octree_parallel_basic import Octree_parallel_basic as Octree_parallel_basic
from Octree_parallel_tree import Octree_parallel_tree as Octree_parallel_tree
import InitialConditions
import Display
import matplotlib.pyplot as plt

# ===== CHOOSE N BODY SETTINGS
# newton_g,   Newton's constant in [pc^3 M_sol^-1 Myr^-2]
# timestep,   timestep in Myr
# box_size,   half-length of simulation box in pc
# softening,  softening length in pc
# tree_thres, threshold on the radio of (distance to centre of mass) to
#             (cell size) for a cell to be used
# display_f,  number of time steps between each update for the particle display
#             and energy diagnostic
# choose one of the following three blocks of settings

# N body settings - Plummer sphere
newton_g = 0.0044995611
timestep = 0.1
box_size = 50
softening = 10.
tree_thres = 1.
display_f = 10

# N body settings - 2 body Kepler problem
#newton_g = 0.0044995611
#timestep = 10.
#box_size = 50
#softening = 0.
#tree_thres = 1.
#display_f = 100

# N body settings - 4 body Kepler problem
#newton_g = 0.0044995611
#timestep = 0.5
#box_size = 50
#softening = 0.
#tree_thres = 1.
#display_f = 200

# setting up MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

particles = None
if rank == 0:
  # ====== CHOOSE INITIAL CONDITIONS
  # include this line if you want same conditions for timing purposes
  #InitialConditions.seed()
  # choose the initial conditions corresponding to the settings you chose above

  # initial conditions - Plummer sphere
  # parameters (number of particles, scale radius [pc])
  particles = InitialConditions.plummersphere(100, 10, newton_g)

  # initial conditions - two body Kepler problem
  # parameters (semimajor axis [pc], eccentricity)
  #particles = InitialConditions.kepler(10, 0., newton_g)

  # initial conditions - four body Kepler problem
  # parameters (inner binary semimajor axis [pc], eccentricity
  #             outer binary semimajor axis [pc], eccentricity)
  #particles = InitialConditions.doublekepler(1., 0., 30., 0., newton_g)

#broadcast the initial conditions
particles = comm.bcast(particles, root = 0)

#diagnostic, initial energy
energy0 = Display.energy(particles, newton_g)

# ===== CHOOSE N BODY SOLVER
# choose one of the following three N body solvers

# N body solver - serial
#nbody = Octree_serial(particles, newton_g, box_size, timestep, tree_thres, softening)

# N body solver - force calculation parallel
#nbody = Octree_parallel_basic(comm, particles, newton_g, box_size, timestep, tree_thres, softening)

# N body solver - tree construction and force computation parallel
nbody = Octree_parallel_tree(comm, particles, newton_g, box_size, timestep, tree_thres, softening)

# store energy diagnostic
relde = []
# loop over time steps
# ===== SET THE NUMBER OF TIME STEPS
for i in xrange(10000):
  # print time step number
  if rank == 0:
    print i

  # evolve system
  nbody.evolve() 

  # display and diagnostic
  if rank == 0 and i % display_f == 0:
    Display.position_display(nbody.particles, box_size, "Step "+str(i))
    de = (Display.energy(nbody.particles, newton_g)-energy0)/energy0
    relde.append(de)
    plt.figure(2)
    plt.clf()
    plt.title('Energy Diagnostic')
    plt.xlabel('Sample Number')
    plt.ylabel('Relative change in energy')
    plt.plot(relde, 'r')
    plt.draw()

# print timings
if rank == 0:
  print nbody.timings
