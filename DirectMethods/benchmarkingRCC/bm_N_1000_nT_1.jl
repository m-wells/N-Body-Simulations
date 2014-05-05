include("leapfrog_2order_ser.jl")

println("serial calculation")

config="conf_N_1000"
launch_leapfrog_ser(config);
