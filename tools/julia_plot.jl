using PyPlot;
function julia_plot(positions)
	numparticles = size(positions)[1]; #the number of rows of state
	#linesize=mass./(maximum(mass))
	for i=1:numparticles
	    x=transpose(positions[i,:,1]);
	    y=transpose(positions[i,:,2]);
	    #z=transpose(positions[i,:,3]);
	    #print(x)
	    plot(x,y,linewidth=10)
	    #plot(x,y,linewidth=10*linesize[i])
	end
end
