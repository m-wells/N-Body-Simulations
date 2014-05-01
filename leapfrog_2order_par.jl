function update_state_par(state::SharedArray{Float64,2},mass::Array{Float64},dt::Float64,G::Float64)
    #leapfrog update for all particles in parallel
    
    numparticles = size(state)[1]; #the number of rows of state
    #should think how to do this when particles is not evenly divisible by procs
    particles_per_proc=int(numparticles/nworkers());
    ilist=int(linspace(1,particles_per_proc,particles_per_proc));
    #initialize next_state to store values in
    next_state = SharedArray(Float64,(numparticles,9));

    map(fetch,{@spawnat workers()[i] leapfrogStepForIList!(ilist.+particles_per_proc*(i-1),state,next_state,mass,dt,G) for i=1:nworkers()})
    
    return next_state;
end



function integrate_leapfrog_par(initialState::Array{Float64,2},mass::Array{Float64},numSteps::Int64,dt::Float64,G::Float64)
    #this performs the integration with a step size of dt and numSteps number of steps
    
    numparticles = size(initialState)[1]; #the number of rows of state
    
    #initialize an initial accelerations array (will hcat this to initialState)
    initialAccelerations = Array(Float64,numparticles,3);
    
    #need to compute the initial acceleration for each particle
    for i=1:numparticles
        initialAccelerations[i,:] = total_accel_on_i(i,initialState,mass,G);
    end
    
    state=hcat(initialState,initialAccelerations);
    #pos[i,:,1],pos[i,:,2]
    sharedState=SharedArray(Float64,numparticles,9);
    sharedState[:,:]=state[:,:];
    #initialize x, y, and z arrays to track each particle (row) at each step (column)
    x = Array(Float64,numparticles,numSteps);
    y = Array(Float64,numparticles,numSteps);
    z = Array(Float64,numparticles,numSteps);
    
    #store the initial positions
    x[:,1] = initialState[:,1];
    y[:,1] = initialState[:,2];
    z[:,1] = initialState[:,3];
    
    for n=2:numSteps
        sharedState = update_state_par(sharedState,mass,dt,G);
        x[:,n] = sharedState[:,1];
        y[:,n] = sharedState[:,2];
        z[:,n] = sharedState[:,3];
    end
    
    #initialize a 3-dimensional array
    positions = Array(Float64,numparticles,numSteps,3);
    positions[:,:,1] = x;
    positions[:,:,2] = y;
    positions[:,:,3] = z;
    
    return positions;
end



function launch_leapfrog_par(config::String,numProcs::Int64)
    include("init_tools.jl")
    #tic();

    set_procs(numProcs);
    require("leapfrog_2order_functions.jl")
    #@everywhere include("leapfrog_2order_functions.jl")
    initialSystem=generate_initialSystem_from_config(config);

    mass=initialSystem[:,1];
    initialState=initialSystem[:,2:7];

    configParameters=retrieve_parameters_from_config(config);
    numSteps=int(configParameters[9]);
    dt=configParameters[10];
    G=configParameters[11];

    tic();
    positions=integrate_leapfrog_par(initialState,mass,numSteps,dt,G);
    toc();
    return positions;
end
