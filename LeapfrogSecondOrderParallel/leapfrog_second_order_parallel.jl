function comp_pos_update(d::Float64,vd::Float64,ad::Float64,dt::Float64)
    #returns the next distance parameter d (i.e. x, y, or z)

    #leapfrog the position
    d = d + vd*dt + 0.5ad*dt^2;
    return d
end



function comp_vel_update(vd::Float64,ad0::Float64,ad1::Float64,dt::Float64)
    #returns the next velocity parameter vd (i.e. vx, vy, or vz)
    #a0 is the "current" acceleration, a1 is the next acceleration (i.e. the updated acc.)
    
    #leapfrog the velocity
    vd = vd + 0.5(ad0 + ad1)dt
    return vd
end



compute_r(delta_x::Float64,delta_y::Float64,delta_z::Float64) = sqrt(delta_x^2 + delta_y^2 + delta_z^2)



function comp_accel_on_i_from_j(di::Float64,dj::Float64,r::Float64,massj::Float64)
    #computes the component of gravitional acceleration on i from j (not scaled with G)
    #d represents the component dimension (i.e. x, y, or z)
    ad = massj*(di-dj)/abs(r)^3;
    return ad
end



function total_accel_on_i(i::Int64,state::Array{Float64,2},mass::Array{Float64,1},G::Float64)
    #the acceleration needs to be determined from the current collection of all the particles
    
    numparticles = size(state)[1]; #the number of rows of state

    xi = state[i,1];
    yi = state[i,2];
    zi = state[i,3];
    
    #initialize accelerations
    ax = 0.;
    ay = 0.;
    az = 0.;

    #need to compute the interaction with every particle
    for j = 1:numparticles
        #no self-interaction
        if j != i
            xj = state[j,1];
            yj = state[j,2];
            zj = state[j,3];
            
            r = compute_r(xi-xj,yi-yj,zi-zj)
            ax += comp_accel_on_i_from_j(xi,xj,r,mass[j]);
            ay += comp_accel_on_i_from_j(yi,yj,r,mass[j]);
            az += comp_accel_on_i_from_j(zi,zj,r,mass[j]);
        end
    end
    
    ax = -G*ax
    ay = -G*ay
    az = -G*az
    
    return [ax,ay,az]
end



function leapfrog_step_for_i(i::Int64,state::Array{Float64,2},mass::Array{Float64,1},dt::Float64,G::Float64)
    #take a step updating the positions and the velocities for particle i
    
    #the current position of particle i
    x = state[i,1];
    y = state[i,2];
    z = state[i,3];
    #the current velocity of particle i
    vx = state[i,4];
    vy = state[i,5];
    vz = state[i,6];
    #the current acceleration of particle i (storing this avoids double calculation of acceleration)
    ax0 = state[i,7];
    ay0 = state[i,8];
    az0 = state[i,9];
    
    #debugging
    #if i==1
    #    println("current")
    #    println("x=",x)
    #    println("vx=",vx)
    #    println("ax0=",ax0)
    #end
    
    #update the position of particle i
    x = comp_pos_update(x,vx,ax0,dt);
    y = comp_pos_update(y,vy,ay0,dt);
    z = comp_pos_update(z,vz,az0,dt);
    #update the acceleration of particle i
    # (do this after updating the positions but before updating the velocities)
    a1 = total_accel_on_i(i,state,mass,G);
    ax1 = a1[1];
    ay1 = a1[2];
    az1 = a1[3];
    #update the velocities
    vx = comp_vel_update(vx,ax0,ax1,dt);
    vy = comp_vel_update(vy,ay0,ay1,dt);
    vz = comp_vel_update(vz,az0,az1,dt);
    
    #if i==1
    #    println("updates")
    #    println("x=",x)
    #    println("ax1=",ax1)
    #    println("vx=",vx)
    #end
    
    #should check to see how large the updates are from the currents
    #output an error if it is too large of an increase
    
    #return the next state
    return [x,y,z,vx,vy,vz,ax1,ay1,az1];
end



function update_state(state::Array{Float64,2},mass::Array{Float64,1},dt::Float64,G::Float64)
    #leapfrog update for all particles
    
    #save current state so that we don't start updating until the next state has been computed for all particles
    current_state = deepcopy(state);
    
    numparticles = size(state)[1]; #the number of rows of state
    #initialize next_state to store values in
    next_state = Array(Float64,numparticles,9);
    
    #loop over all particles
    for i=1:numparticles
        next_state[i,:] = leapfrog_step_for_i(i,state,mass,dt,G);
    end
    
    return next_state;
end



function integrate_leapfrog(initialState::Array{Float64,2},mass::Array{Float64,1},N::Int64,dt::Float64,G::Float64)
    #this performs the integration with a step size of dt and N number of steps
    
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
    x = Array(Float64,numparticles,N);
    y = Array(Float64,numparticles,N);
    z = Array(Float64,numparticles,N);
    
    #store the initial positions
    x[:,1] = initialState[:,1];
    y[:,1] = initialState[:,2];
    z[:,1] = initialState[:,3];
    
    for n=2:N
        state = update_state(state,mass,dt,G);
        x[:,n] = state[:,1];
        y[:,n] = state[:,2];
        z[:,n] = state[:,3];
    end
    
    #initialize a 3-dimensional array
    positions = Array(Float64,numparticles,N,3);
    positions[:,:,1] = x;
    positions[:,:,2] = y;
    positions[:,:,3] = z;
    
    return positions
end
