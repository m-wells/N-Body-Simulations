classdef n_body
methods(Static)
    function d = comp_pos_update(d,vd,ad,dt)
        d = d +vd*dt +0.5*ad*dt^2;
    end

    function vd = comp_vel_update(vd,ad0,ad1,dt)
        vd = vd+0.05*(ad0+ad1)*dt;
    end
    
    function ad = comp_accel_on_i_from_j(di,dj,r,massj)
        ad = massj*(di-dj)/(abs(r)^3);
    end
    
    function [ax,ay,az] = total_accel_on_i(i,state,G)
        numparticles = size(state,1);
        
        xi = state(i,2);
        yi = state(i,3);
        zi = state(i,4);
        
        ax = 0.;
        ay = 0.;
        az = 0.;
        
        for j = 1:numparticles
            if j ~= i
                xj = state(j,2);
                yj = state(j,3);
                zj = state(j,4);
                mj = state(j,1);
            r = sqrt((xi-xj)^2+(yi-yj)^2+(zi-zj)^2);
            ax = n_body.comp_accel_on_i_from_j(xi,xj,r,mj);
            ay = n_body.comp_accel_on_i_from_j(yi,yj,r,mj);
            az = n_body.comp_accel_on_i_from_j(zi,zj,r,mj);
            end
        end
        ax = -G*ax;
        ay = -G*ay;
        az = -G*az;
    end
    
    function newstate = leapfrog_step_for_i(i,state,dt,G)
        
        m = state(i,1);
        x = state(i,2);
        y = state(i,3);
        z = state(i,4);
        
        vx = state(i,5);
        vy = state(i,6);
        vz = state(i,7);
        
        ax0 = state(i,8);
        ay0 = state(i,9);
        az0 = state(i,10);
        
        x = n_body.comp_pos_update(x,vx,ax0,dt);
        y = n_body.comp_pos_update(y,vy,ay0,dt);
        z = n_body.comp_pos_update(z,vz,az0,dt);
        
        [ax1,ay1,az1] = n_body.total_accel_on_i(i,state,G);
        
        vx = n_body.comp_vel_update(vx,ax0,ax1,dt);
        vy = n_body.comp_vel_update(vy,ay0,ay1,dt);
        vz = n_body.comp_vel_update(vz,az0,az1,dt);
        newstate = [m,x,y,z,vx,vy,vz,ax1,ay1,az1];
    end
    
end
end


