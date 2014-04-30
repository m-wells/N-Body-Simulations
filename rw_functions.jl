function read_setup_from_file(inputname::String)
	#A function that reads the file "inputname" which assumes that the data is arranged in a CSV format
	filename=string("../initialStates/",inputname,".csv");
	@assert isfile(filename)
	setup=readcsv(filename);
	return setup
end



function get_mass(setup::Array{Float64,2})
	#returns the mass from the setup array which is a user defined file located with initialStates folder.
	mass=transpose(setup[:,1])
	return mass
end



function get_initialState(setup::Array{Float64,2})
	#returns the initial state of each particle (positions and velocities)
	initialState=setup[:,2:7]
	return initialState
end



function write_initialState(initialState::Array, inputname::String)
	#A function that writes the array x to a file **filename** in a CSV-file format
	filename=string("../initialStates/",inputname,".csv");

	#initialState should have 7 columns
	@assert size(initialState)[2] == 7
	writecsv(filename, initialState)
	@assert isfile(filename)
end
