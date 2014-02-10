def trimZeros(data):
    """Expects a list of ints or strings and will return a list corresponding to the type inputted with any trailing zeros removed."""
    
    if isinstance(data[0], str): 
    	data = [int(i) for i in data];
    	string = True;
    else: string = False;

    while data[-1]==0:
        del data[-1];
    while data[0]==0:
        del data[0];

    if not(string): return data;
    else: return [str(i) for i in data];
