"""
diagnostic2-computernetworks
author: rlouie
"""

import math.sqrt as sqrt
import math.floor as floor
import time

"""question 4: a, b, c 
"""

def isPrime(n):
	""" determines primality of a integer n.
	adapted from projecteuler.net problem7 
	"""
	if n == 1:
		return False
	elif n < 4:
		return True						# 2 and 3 are prime
	elif n%2 == 0:
		return False
	elif n < 9:
		return True						# already excluded 4, 6, 8
	elif n%3 == 0:
		return False					
	else:
		r = floor(sqrt(n)) 	# no prime p s.t p*p > n 
		f = 5
		while f <= r:
			if n % f == 0:				
				return False;
			if n % (f+2) == 0:			
				return False
			f += 6
		return True						# all other cases return True

def prime100():
	""" returns the set of all primes btwn 2 and 100 
	"""
	return [p for p in xrange(2, 101) if isPrime(p)]

def timer(fn, x):
	""" measures execution time of 'fn(x)' using time.perf_counter
	"""
	pass