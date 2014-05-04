%%init_parts = csvread('');
init_parts = randn(49,7);
G=1;
numsteps = 100;
dt = 0.1;

tic;
results = leapfrog.integrate_leapfrog(init_parts,numsteps,dt,G);
toc
