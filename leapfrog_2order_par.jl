function update_state_par(state::SharedArray{Float64,2},mass::Array{Float64},dt::Float64,G::Float64)
    #leapfrog update for all particles in parallel
    
    numparticles = size(state)[1]; #the number of rows of state
    #initialize next_state to store values in
    next_state = SharedArray(Float64,(numparticles,9),init=false);
    #next_state = Array(Float64,numparticles,9);

    #loop over all particles
    
     #
     #   for i=1:numparticles
     #   	
     #   	retval = map(fetch,{  (@spawnat worker_ids[i%num_workers+1] leapfrog_step_for_i(i,state,mass,dt,G))});
     #   	next_state[i,:] = transpose(retval[1]);
     #   	#@printf("particle %d on worker %d\n",i,worker_ids[i%num_workers+1])
     #   end

	#println(typeof(next_state))
	retval = map(fetch,{  (@spawnat procs()[i%nprocs()+1] leapfrog_step_for_i(i,state,mass,dt,G)) for i=1:numparticles});
	#retval = map(fetch,{  (@spawnat workers()[i%nworkers()+1] leapfrog_step_for_i(i,state,mass,dt,G)) for i=1:numparticles});
	#next_state = reshape(1:numparticles, numparticles, 9)
	#println(typeof(retval))
	#test = convert(Array{Float64,1},retval)
	for i=1:numparticles
	break
	next_state[i,:] = retval[i];
	#println(next_state[i,:])
	end
	#println(typeof(next_state))
	#println(" ")
	#print(retval[1][1:3])
	#next_state[:,:] = transpose(retval[1]);
	#@printf("particle %d on worker %d\n",i,worker_ids[i%num_workers+1])
    
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
	#@printf("step=%d\n",n)
        state = update_state_par(sharedState,mass,dt,G);
        x[:,n] = state[:,1];
        y[:,n] = state[:,2];
        z[:,n] = state[:,3];
    end
    
    #initialize a 3-dimensional array
    positions = Array(Float64,numparticles,numSteps,3);
    positions[:,:,1] = x;
    positions[:,:,2] = y;
    positions[:,:,3] = z;
    
    return positions
end



function launch_leapfrog_par(config::String,numProcs::Int64)
    include("init_tools.jl")
    #tic();

    set_procs(numProcs);
    require("leapfrog_2order_functions.jl")
    initialSystem=generate_initialSystem_from_config(config);

    mass=initialSystem[:,1];
    initialState=initialSystem[:,2:7];

    configParameters=retrieve_parameters_from_config(config)
    numSteps=int(configParameters[9]);
    dt=configParameters[10];
    G=configParameters[11];

    tic();
    positions=integrate_leapfrog_par(initialState,mass,numSteps,dt,G);
    toc();
end
