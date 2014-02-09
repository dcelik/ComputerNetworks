def chunk(L,x):
    x = int(x)
    chunked = [L[i:i+x] for i in range(0,int(len(L)),x)] #Divide the list of inputs into smaller lists equal in size to the time step x
    return chunked
def consolidate(L,x):
    x = int(x)
    chunked_list = chunk(L,x) #Divide the list of inputs into smaller lists equal in size to the time step x
    consolidated_list = [round(sum(chunked_list[i])/x) for i in range(len(chunked_list))] #Average each of the smaller lists and round the result
    for i in consolidated_list:
        if i == 1:
            i = True
        else:
            i = False
    return consolidated_list
