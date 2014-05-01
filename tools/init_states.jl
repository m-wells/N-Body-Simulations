function retrieve_parameters_from_config(config_name::String)
    parameters=read_config_from_file(config_name);
    @assert size(parameters)[1] == 11
    @assert size(parameters)[2] == 2
    return parameters[:,2]
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



function comp_mass_pos(d::Array{Float64,1},mass::Array{Float64,1})
    #component center of mass calculation
    return sum(d.*mass)/sum(mass)
end



function comp_mass_vel(vd::Array{Float64,1},mass::Array{Float64,1})
    #component center of mass calculation
    return sum(vd.*mass)/sum(mass)
end



function generate_initialSystem(minmass,maxmass,minpos,maxpos,minvel,maxvel,num_particles::Int64,seed::Int64)
    #generates an initial state
    mass = generate_masses(minmass,maxmass,num_particles,seed)
    x = generate_positions(minpos,maxpos,num_particles,seed+1)
    y = generate_positions(minpos,maxpos,num_particles,seed+2)
    z = generate_positions(minpos,maxpos,num_particles,seed+3)
    vx = generate_velocities(minvel,maxvel,num_particles,seed+4)
    vy = generate_velocities(minvel,maxvel,num_particles,seed+5)
    vz = generate_velocities(minvel,maxvel,num_particles,seed+6)
    
    #correct to the center of mass position
    x = x .- comp_mass_pos(x,mass);
    y = y .- comp_mass_pos(y,mass);
    z = z .- comp_mass_pos(z,mass);

    #correct to the center of mass frame
    vx = vx .- comp_mass_vel(vx,mass);
    vy = vy .- comp_mass_vel(vy,mass);
    vz = vz .- comp_mass_vel(vz,mass);
    
    initialState = hcat(mass,x,y,z,vx,vy,vz)
    return initialState
end



function generate_initialSystem_from_config(config_name::String)
    parameters = retrieve_parameters_from_config(config_name);
    
    minmass = parameters[1];
    maxmass = parameters[2];
    minpos = parameters[3];
    maxpos = parameters[4];
    minvel = parameters[5];
    maxvel = parameters[6];
    num_particles = int(parameters[7]);
    seed = int(parameters[8]);
    numSteps = int(parameters[9]);
    dt = parameters[10];
    G = parameters[11];


    initialState = generate_initialSystem(minmass,maxmass,minpos,maxpos,minvel,maxvel,num_particles,seed)
    return initialState
end



function generate_sharedInitialSystem_from_config(config_name::String)
    initialSystem=generate_InitialSystem_from_config(config_name);
    sharedInitialState=SharedArray(Float64,(size(initialSystem)[1],size(initialSystem)[2]))
    sharedInitialState[:,:]=initialSystem[:,:]
    return sharedInitialState
end
