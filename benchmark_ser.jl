include("leapfrog_2order_ser.jl")

println("serial calculation")

config="defaults"
launch_leapfrog_ser(config);
