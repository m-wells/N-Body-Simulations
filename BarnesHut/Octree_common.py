# holds phase space information of a particle
class Particle:
  def __init__(self, x, y, z, vx, vy, vz, name):
    self.x, self.y, self.z = x, y, z
    self.vx, self.vy, self.vz = vx, vy, vz
    self.name = name

  # kick step where the velocity is changed by force
  def kick(self, cell, NEWTON_G, TIMESTEP, SOFTENING):
    # distance
    rx = cell.xcen - self.x
    ry = cell.ycen - self.y
    rz = cell.zcen - self.z
    r2 = rx*rx + ry*ry + rz*rz

    # if outside softening length, don't need softening
    if r2 > SOFTENING*SOFTENING:
      self.vx += NEWTON_G * TIMESTEP * rx * cell.n / r2**1.5
      self.vy += NEWTON_G * TIMESTEP * ry * cell.n / r2**1.5
      self.vz += NEWTON_G * TIMESTEP * rz * cell.n / r2**1.5
    # else use solid sphere softening
    else:
      r = r2**0.5
      x = r / SOFTENING
      f = x * (8 - 9 * x + 2 * x * x * x) # Dyer and Ip 1993, ApJ 409(1)
      self.vx += NEWTON_G * TIMESTEP * f * rx * cell.n / (SOFTENING*SOFTENING*r)
      self.vy += NEWTON_G * TIMESTEP * f * ry * cell.n / (SOFTENING*SOFTENING*r)
      self.vz += NEWTON_G * TIMESTEP * f * rz * cell.n / (SOFTENING*SOFTENING*r)

  # drift step where position is changed by velocity
  def drift(self, TIMESTEP):
    self.x += self.vx * TIMESTEP
    self.y += self.vy * TIMESTEP
    self.z += self.vz * TIMESTEP

# trees are composed of cells referring to their daughter cells
class Cell:
  def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax, name):
    self.xmin, self.xmax = xmin, xmax
    self.ymin, self.ymax = ymin, ymax
    self.zmin, self.zmax = zmin, zmax
    self.name = name
    # start with no particles
    self.n = 0 
    self.xcen, self.ycen, self.zcen = 0, 0, 0
    self.daughters = []
    self.particle = None

  # test if a (x,y,z) coordinate is in this cell's bounds
  def incell(self, x, y, z):
    if x > self.xmin and x <= self.xmax and y > self.ymin and y <= self.ymax \
      and z > self.zmin and z <= self.zmax:
      return True
    else:
      return False

  def add(self, particle):
     # if particle not in bounds of cell, do nothing
     if not self.incell(particle.x, particle.y, particle.z):
       return

     # if this cell already has some particles, also add this particle
     # to our descendents
     if self.n > 0:
       # if this is the second particle this cell has encountered,
       # need to make descendents, and try adding the first particle
       # to our descendents
       if self.n == 1:
         self.makedaughters()
         for daughter in self.daughters:
           daughter.add(self.particle)
         self.particle = None # this cell no longer holds just 1 particle
       # add incoming particle to descendents
       for daughter in self.daughters:
         daughter.add(particle)
     # if this is the first particle this cell has encountered
     else:
       self.particle = particle

     # change center of mass
     self.xcen = (self.n * self.xcen + particle.x) / float(self.n + 1)
     self.ycen = (self.n * self.ycen + particle.y) / float(self.n + 1)
     self.zcen = (self.n * self.zcen + particle.z) / float(self.n + 1)
     # increment particle counter
     self.n += 1

  # create this cell's eight daughters
  def makedaughters(self):
    xhalf = (self.xmin + self.xmax) / 2.
    yhalf = (self.ymin + self.ymax) / 2.
    zhalf = (self.zmin + self.zmax) / 2.
    daughter1 = Cell(self.xmin, xhalf, self.ymin, yhalf, self.zmin, zhalf, self.name+".0")
    daughter2 = Cell(xhalf, self.xmax, self.ymin, yhalf, self.zmin, zhalf, self.name+".1")
    daughter3 = Cell(self.xmin, xhalf, yhalf, self.ymax, self.zmin, zhalf, self.name+".2")
    daughter4 = Cell(xhalf, self.xmax, yhalf, self.ymax, self.zmin, zhalf, self.name+".3")
    daughter5 = Cell(self.xmin, xhalf, self.ymin, yhalf, zhalf, self.zmax, self.name+".4")
    daughter6 = Cell(xhalf, self.xmax, self.ymin, yhalf, zhalf, self.zmax, self.name+".5")
    daughter7 = Cell(self.xmin, xhalf, yhalf, self.ymax, zhalf, self.zmax, self.name+".6")
    daughter8 = Cell(xhalf, self.xmax, yhalf, self.ymax, zhalf, self.zmax, self.name+".7")
    self.daughters = [daughter1, daughter2, daughter3, daughter4, daughter5, daughter6, daughter7, daughter8]

  # makes cell forget current daughters and take in new daughters,
  # recalculating mass and center of mass
  def assigndaughters(self, daughters):
    self.daughters = []
    self.daughters = daughters
    self.n = sum([daughter.n for daughter in daughters])
    # only need to calculate center of mass if cell is not empty
    if self.n > 0:
      self.xcen = sum([daughter.n * daughter.xcen for daughter in daughters]) / float(self.n)
      self.ycen = sum([daughter.n * daughter.ycen for daughter in daughters]) / float(self.n)
      self.zcen = sum([daughter.n * daughter.zcen for daughter in daughters]) / float(self.n)

  # traverse the tree to get a list of particles in this cell and below
  def particles(self):
    # if this is a bottom level cell with a particle
    if self.particle:
      return [self.particle]
    # else, if this cell has daughters, forward request to its daughters and
    # accumulate their answers
    elif self.daughters:
      l = []
      for daughter in self.daughters:
        l.extend(daughter.particles())
      return l
    # else, this is a bottom level cell with no particle
    else:
      return []

  # test if this cell is far enough from the specified particle for
  # force calculation
  def meetscriterion(self, particle, TREE_THRES, SOFTENING):
     # if this cell has many particles,
     # cell center of mass must be farther from particle than size of cell
     if self.daughters:
       s = self.xmax - self.xmin
       dx = particle.x - self.xcen
       dy = particle.y - self.ycen
       dz = particle.z - self.zcen
       d  = (dx*dx + dy*dy + dz*dz)**0.5
       # test d/s > tree_thres (equivalent to s/d < theta = tree_thres^-1)
       # also, we want to calculate individual particle forces within the
       # softening length
       return (d/s) > TREE_THRES and d > SOFTENING
     # else, just check that particle isn't trying to interact with itself
     # using object identity
     else:
       return self.particle != particle
