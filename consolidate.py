def chunk(list,x):
    chunked = [list[i:i+x] for i in range(0,int(len(list)),x)] #Divide the list of inputs into smaller lists equal in size to the time step x
    return chunked
def consolidate(list,x):
    chunked_list = chunk(list,x) #Divide the list of inputs into smaller lists equal in size to the time step x
    consolidated_list = [round(sum(chunked_list[i])/x) for i in range(len(chunked_list))] #Average each of the smaller lists and round the result
    return consolidated_list
