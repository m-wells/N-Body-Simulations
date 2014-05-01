#for reading in ascii files
include("../rw_functions.jl");
#contains the leapfrog serial rountine
include("leapfrog_second_order_serial.jl")
setup=read_setup_from_file("test2particle");
mass=get_mass(setup);
initialState=get_initialState(setup);
nsteps=1000000;
stepsize=0.5;
grav_constant=100.;

tic();
pos=integrate_leapfrog_ser(initialState,mass,nsteps,stepsize,grav_constant);
toc();
