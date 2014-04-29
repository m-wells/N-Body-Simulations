function read_initialState(inputname::String)
    #A function that reads the file "inputname" which assumes that the data is arranged in a CSV format
    @assert isfile(inputname)
    return readcsv(inputname)
end



#function write_initialState(x::Array, filename::String)
#    #A function that writes the array x to a file **filename** in a CSV-file format
#    #In our case, x is a multidimensional array;
#    #- x[:,1]: time
#    #- x[:,2]: detrended flux
#    #- x[:,3]: original, untrended flux
#    #- x[:,4]: flux_error - note this needs to be corrected for - not normalized!
#    writecsv(filename, x)
#end
