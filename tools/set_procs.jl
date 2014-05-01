function handle_procs(num_desired_procs::Int64)
    current_proc_ids=procs();
    num_current_procs=nprocs();
    if (num_current_procs < num_desired_procs);
        addprocs(num_desired_procs-num_current_procs);
    elseif (num_current_procs > num_desired_procs);
        for i in 0:(num_current_procs-num_desired_procs)-1;
            rmprocs(current_proc_ids[num_current_procs-i]);
        end
    else
        println("WARNING: Number of processes unchanged!")
    end
end

function set_procs(num_desired_procs::Int64)
    handle_procs(num_desired_procs);
    sleep(0.25);
    num_procs=nprocs();
    num_workers=nworkers();
    if num_procs > 1
        @printf("Using %d processes\n",num_procs)
        @printf("Using %d workers\n",num_workers)
    else
        @printf("Using %d process\n",num_procs)
        @printf("Using %d worker\n",num_workers)
    end
end
