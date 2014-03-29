"""
utilities.py
------------
Author: Nick Francisci
Purpose: To provide commonly used functions to classes
    that require them.
Status: Tested and Working 2-13-14

"""
def calc_checksum(s):
    checksum = 0
    for c in s:
        checksum += ord(c)
    checksum = -(checksum % 256)
    checksum = '%2X' % (checksum % 0xFF)
    if checksum[0] == ' ':
        return '0' + checksum[1:]
    elif len(checksum) == 1:
        return '0' + checksum
    else:
        return checksum

def trimZeros(data):
    """
    Removes preceeding and trailing zeros.
    data = the string or list to have the zeros removed from
    """

    #Parses string lists to int lists for easier operation
    if isinstance(data[0], str): 
    	data = [int(i) for i in data];
    	string = True;
    else: string = False;

    #Trims 0s off head and tail of list
    while data[-1]==0:
        del data[-1];
    while data[0]==0:
        del data[0];

    #Returns data, parsing int list to string list if it was submitted as string list
    if not(string): return data;
    else: return [str(i) for i in data];

def fromBoolean(d):
    """ Translates a boolean to a character '1' or '0'. """
    if d:
        return '1'
    else:
        return '0'

def toBool(d):
    """ Translates a character '1' or '0' to a boolean """
    if d=='1':
        return True;
    else:
        return False;
