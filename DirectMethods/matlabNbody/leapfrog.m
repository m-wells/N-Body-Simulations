classdef leapfrog
    methods(Static)
        function next_state = update_state(state,dt,G)
           numparticles =  size(state,1);
           next_state = zeros(numparticles,10);
           for i = 1:numparticles
               next_state(i,:) = n_body.leapfrog_step_for_i(i,state,dt,G);
           end
        end
        
        function positions = integrate_leapfrog(initialState,numsteps,dt,G)
            numparticles =  size(initialState,1);
            
            initialAccelerations = zeros(numparticles,3);
            
            for i=1:numparticles
                initialAccelerations(i,:) = n_body.total_accel_on_i(i,initialState,G);
            end
        
            state = cat(2,initialState,initialAccelerations);
            
            x=zeros(numparticles,numsteps);
            y=zeros(numparticles,numsteps);
            z=zeros(numparticles,numsteps);
        
            x(:,1) = initialState(:,2);
            y(:,1) = initialState(:,3);
            z(:,1) = initialState(:,4);
            
            for n=2:numsteps
                state = leapfrog.update_state(state,dt,G);
                x(:,n)=state(:,2);
                y(:,n)=state(:,3);
                z(:,n)=state(:,4);
            end
            
            positions = zeros(numparticles,numsteps,3);
            positions(:,:,1) = x;
            positions(:,:,2) = y;
            positions(:,:,3) = z;
        end
       
        
    end
end