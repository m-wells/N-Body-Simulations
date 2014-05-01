include("leapfrog_2order_par.jl")

println("parallel calculation")

config="defaults";
numProcs=int(8);
launch_leapfrog_par(config,numProcs);
