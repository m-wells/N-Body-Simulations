%%init_parts = csvread('');
init_parts = randn(100,7);
G=1;
numsteps = 10;
dt = 0.1;

tic;
results = leapfrog.integrate_leapfrog(init_parts,numsteps,dt,G);
toc
