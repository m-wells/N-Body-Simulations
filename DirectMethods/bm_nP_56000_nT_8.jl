include("leapfrog_2order_par.jl")

println("parallel calculation")

config="conf_nP_56000"
numProcs=int(8);
launch_leapfrog_par(config,numProcs);
