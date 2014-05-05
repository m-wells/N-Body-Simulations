include("leapfrog_2order_par.jl")

println("parallel calculation")

config="conf_nP_490"
numProcs=int(8);
launch_leapfrog_par(config,numProcs);
