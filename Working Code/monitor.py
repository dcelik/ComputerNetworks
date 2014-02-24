import takeMeasurement.takeMeasurement as takeMeasurement

def monitorStart():
    """ Determines if we've started receiving an actual transmission.

    If something interesting is noticed (i.e. a '1'), we start paying attention 
    by storing it in cache.

    If we continue to capture something interesting (measured by if the cache = [1, 1, 1]) 
    as opposed to some noise (a random '1' amongst a list of '0's), 
    we know that a real message is now being received. 

    Return the initial part of the new message, so that capturing of the full message
    can begin.
    
    """

    cache = []

    while len(cache) < 3:   # exit loop when cache=[True]*3 i.e. when a msg is coming through
        z = takeMeasurement()
        if z:   # Something interesting!
            cache.append(True)    
        else:               # nothing interesting
            cache = []      

    return cache            # return the inital part of the new incoming message