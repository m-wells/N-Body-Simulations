include("leapfrog_2order_ser.jl")

println("serial calculation")

config="conf_nP_5600"
launch_leapfrog_ser(config);
