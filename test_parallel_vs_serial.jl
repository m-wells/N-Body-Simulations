using Base.Test
function test_parallel_vs_serial(config::String,numProcs::Int64)
	include("leapfrog_2order_ser.jl")
	include("leapfrog_2order_par.jl")

	pos_ser=launch_leapfrog_ser(config);
	pos_par=launch_leapfrog_par(config,numProcs);

#	println(pos_ser)
#	println("==================== ")
	#println(pos_par)
	#@test_approx_eq_eps(pos_ser,pos_par,5.0)
	if pos_ser==pos_par;
		println("serial and parallel methods agree")
	else
		println("serial and parallel methods do not agree")
	end
	#include("tools/julia_plot.jl")
	#julia_plot(pos_par)
	return
end
