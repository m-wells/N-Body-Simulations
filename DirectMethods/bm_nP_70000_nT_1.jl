include("leapfrog_2order_ser.jl")

println("serial calculation")

config="conf_nP_70000"
launch_leapfrog_ser(config);
