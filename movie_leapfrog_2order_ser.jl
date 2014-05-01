function update_state_ser(state::Array{Float64,2},mass::Array{Float64},dt::Float64,G::Float64)
    #leapfrog update for all particles
    
    numparticles = size(state)[1]; #the number of rows of state
    #initialize next_state to store values in
    next_state = Array(Float64,numparticles,9);
    
    #loop over all particles
    for i=1:numparticles
        next_state[i,:] = leapfrog_step_for_i(i,state,mass,dt,G);
    end
    
    return next_state;
end



function integrate_leapfrog_ser(initialState::Array{Float64,2},mass::Array{Float64},numSteps::Int64,dt::Float64,G::Float64)
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
    
    #initialize x, y, and z arrays to track each particle (row) at each step (column)
    x = Array(Float64,numparticles,numSteps);
    y = Array(Float64,numparticles,numSteps);
    z = Array(Float64,numparticles,numSteps);
    
    #store the initial positions
    x[:,1] = initialState[:,1];
    y[:,1] = initialState[:,2];
    z[:,1] = initialState[:,3];
    
    for n=2:numSteps
        state = update_state_ser(state,mass,dt,G);
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

    using PyPlot;

function movie_launch_leapfrog_ser(n_part::Int64)
    include("init_tools.jl")
    #tic();
    include("leapfrog_2order_functions.jl")
    #-------------------------------
    #-------------------------------
    #-------------------------------
    #-------------------------------
    #FOR 3 PARTICLES:: in 3part_mov.csv
    if(n_part ==3)
        initialSystem=read_setup_from_file("3part_mov")
        numSteps=100000;
        dt = 0.5;
        G = 0.1;
        #-----------------------------

        mass=initialSystem[:,1];
        initialState=initialSystem[:,2:7];
        println("mass")
        println(mass)
        println("intState");
        println(initialState)

        tic();
        positions=integrate_leapfrog_ser(initialState,mass,numSteps,dt,G);
        toc();

        numparticles = size(initialState)[1]; #the number of rows of state
        linesize=mass./(maximum(mass))
        for i=1:numparticles
            x=transpose(positions[i,:,1]);
            y=transpose(positions[i,:,2]);
            #z=transpose(positions[i,:,3]);
           #print(x)
            plot(x,y,linewidth=10*linesize[i])
        end
        write_pos_out_interval(positions,500,"3part_mov")
    end
    ##-----------------------------
    #-------------------------------
    #-------------------------------
    #FOR 2 PARTICLES:: in 2part_mov.csv
    if(n_part ==2)
        initialSystem=read_setup_from_file("2part_mov")
        numSteps=1000000;
        dt = 1.;
        G = 100.;
        #-----------------------------

        mass=initialSystem[:,1];
        initialState=initialSystem[:,2:7];
        println("mass")
        println(mass)
        println("intState");
        println(initialState)

        tic();
        positions=integrate_leapfrog_ser(initialState,mass,numSteps,dt,G);
        toc();

        numparticles = size(initialState)[1]; #the number of rows of state
        linesize=mass./(maximum(mass))
        for i=1:numparticles
            x=transpose(positions[i,:,1]);
            y=transpose(positions[i,:,2]);
            #z=transpose(positions[i,:,3]);
           #print(x)
            plot(x,y,linewidth=10*linesize[i])
            xlim(-100000,100000)
            ylim(-100000,100000)
        end
        write_pos_out_interval(positions,5000,"2part_mov")
    end

end
