function random_array(minmax,length::Int64,seed::Int64)
    #generates a random array of length with values between +/- minmax
    srand(seed);
    ret_array = zeros(length);
    rand!(ret_array)
    
    return 2minmax.*(ret_array.-0.5)
end



function generate_masses(minmass,maxmass,num_particles::Int64,seed::Int64)
    #generates a random array of num_particles with values between minmass and maxmass
    @assert minmass < maxmass
    @assert seed >= 0
    @assert num_particles > 0
    srand(seed);
    ret_array = zeros(num_particles);
    rand!(ret_array)
    ret_array = (maxmass-minmass).*ret_array.+minmass
    @assert minimum(ret_array) > minmass
    @assert maximum(ret_array) < maxmass
    println("masses successfully generated within limits")

    if minimum(ret_array) < 0
	    println("Warning: negative masses are present!")
    end

    return ret_array 
end



function generate_positions(minposition,maxposition,num_particles::Int64,seed::Int64)
    #generates a random array of num_particles with values between minposition and maxposition
    @assert minposition < maxposition
    @assert seed >= 0
    @assert num_particles > 0
    srand(seed);
    ret_array = zeros(num_particles);
    rand!(ret_array)
    ret_array = (maxposition-minposition).*ret_array.+minposition
    @assert minimum(ret_array) > minposition
    @assert maximum(ret_array) < maxposition
    println("positions successfully generated within limits")
    return ret_array 
end



function generate_velocities(minvelocity,maxvelocity,num_particles::Int64,seed::Int64)
    #generates a random array of num_particles with values between minvelocity and maxvelocity
    @assert minvelocity < maxvelocity
    @assert seed >= 0
    @assert num_particles > 0
    srand(seed);
    ret_array = zeros(num_particles);
    rand!(ret_array)
    ret_array = (maxvelocity-minvelocity).*ret_array.+minvelocity
    @assert minimum(ret_array) > minvelocity
    @assert maximum(ret_array) < maxvelocity
    println("velocities successfully generated within limits")
    return ret_array 
end



function generate_initialState(minmass,maxmass,minpos,maxpos,minvel,maxvel,num_particles::Int64,seed::Int64)
    #generates an initial state
    mass = generate_masses(minmass,maxmass,num_particles,seed)
    x = generate_positions(minpos,maxpos,num_particles,seed+1)
    y = generate_positions(minpos,maxpos,num_particles,seed+2)
    z = generate_positions(minpos,maxpos,num_particles,seed+3)
    vx = generate_velocities(minvel,maxvel,num_particles,seed+4)
    vy = generate_velocities(minvel,maxvel,num_particles,seed+5)
    vz = generate_velocities(minvel,maxvel,num_particles,seed+6)
    
    initialState = hcat(mass,x,y,z,vx,vy,vz)
end
