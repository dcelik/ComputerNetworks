from collections import Counter

def getPulseWidth(data, verbose=False):
	"""
	Given the data from a transmission, this function will attempt to retrieve
	the number of samples taken per LED on cycle. This method assumes that the 
	sensor is over-, rather than under-, sampling. It will also deterimine the
	goodness of the data passed in and will suggest a retransmission if the 
	data is of poor quality. Currently, this suggestion is visible to the user
	but does not actually transmit a request for a retransmission. IMPORTANT:
	due to changes in integer division and print statements in python 3, this
	file is NOT backwards compatibile with python 2!
	Arguments: data = the data to analyze as a list
		   verbose = True for a full accounting of data goodness, defaults
			     to false
	Returns: the determined pulse width of the transmission
	"""

	#Get a list of the three most common lengths of zeros,
	#and the two most common lengths of ones
	pulseLengthZeros,pulseLengthOnes = getOccuranceFrequencies([int(i) for i in data]);
	
	#Compile a list of the potential pulse widths based on the known relations of morse code
	potentialWidths = [];
	print(pulseLengthZeros);
	
	if(len(pulseLengthZeros)>0):potentialWidths.append(pulseLengthZeros[0]);	#Based on symbol spaces
	if(len(pulseLengthZeros)>1):potentialWidths.append(pulseLengthZeros[1]//3);	#Based on character spaces
	#if(len(pulseLengthZeros)>2):potentialWidths.append(pulseLengthZeros[2]//7);	#Based on word spaces
	if(len(pulseLengthOnes)>0): potentialWidths.append(pulseLengthOnes[0]);	        #Based on dot length
	if(len(pulseLengthOnes)>1): potentialWidths.append(pulseLengthOnes[1]//3);	#Based on dash length
	
	pulse_width, data_goodness = findPulseWidth([round(width,0) for width in potentialWidths]);

	if(verbose):
		print("Pulse width determined to be " +str(pulse_width) +" with a  data goodness of " + str(data_goodness) +
		      " (measured from 0 to 1) which is based on " + str(len(pulseLengthOnes)+len(pulseLengthZeros)) + " evaluations out of a maximum 5.");
		print("Note: data goodness is simply a measure of the uniformity of the most common  binary occurances " +
		      "in the code for the purposes of obtaining a pulse width and should not be taken to mean that "+
		      "the message has transmitted without errors.")
		if(data_goodness<=.5): print("Recorded pulses are irregular - consider requesting repeat of message.");
	
	return pulse_width;


def getOccuranceFrequencies(data):
	"""
	Reads the list inputted and finds the most common pulses of ones and zeros.
	Arguments: data = The data to be examined as a list
	Returns: pulseLengthZeros = a sorted list of the 3 most common pulse lengths of zero
			 pulseLengthOnes = a sorted list of the 2 most common pulse lengths of ones
	"""
	#Initilize Lists and Variables
	pulsesZeros = [];
	pulsesOnes = [];
	pulseLength = 0;
	pulseIsOnes = data[0];

	#Iterate through data and add each pulse length to the correct list
	for datum in data:
		if(pulseIsOnes and datum):
			pulseLength+=1;
		elif(pulseIsOnes and not(datum)):
			pulsesOnes.append(pulseLength);
			pulseLength = 1;
			pulseIsOnes = False;
		elif(not(pulseIsOnes) and not(datum)):
			pulseLength+=1;
		else:
			pulsesZeros.append(pulseLength);
			pulseLength = 1;
			pulseIsOnes = True;

	#Account for last grouping of zeros or ones
	if pulseIsOnes: pulsesOnes.append(pulseLength);
	else: pulsesZeros.append(pulseLength);


	#Extract modes from lists
	pulseLengthZeros = Counter(pulsesZeros).most_common(2);
	pulseLengthOnes = Counter(pulsesOnes).most_common(2)
	print("Modal distribution of ones: " +str(pulseLengthZeros));
	print("Modal distribution of zeros: " +str(pulseLengthOnes));

	return sorted([int(key) for key in dict(pulseLengthZeros).keys()]),sorted([int(key) for key in dict(pulseLengthOnes).keys()]);


def findPulseWidth(data):
	"""
	Determines whether the data are uniform and valid and returns the mode of the data
	as the pulse width
	Returns: pulse_width = the mode of the inputted data
			 data_goodness = the proportion of the data that is equal to the 
			 pulse width from 0-1
	"""

	print("Final Data Set: " + str(data));
	
	pulse_width = Counter(data).most_common(1);
	pulse_width, value = dict(pulse_width).popitem();
	data_goodness = 0;

	for datum in data:
		if datum==pulse_width:
			data_goodness+=1
	
	return pulse_width, data_goodness/len(data);
