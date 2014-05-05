include("leapfrog_2order_par.jl")

println("parallel calculation")

config="conf_nT"
numProcs=int(3);
launch_leapfrog_par(config,numProcs);
