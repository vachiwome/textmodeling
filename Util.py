"""
Valentine Chiwome
ESN for text modelling
"""

from math import exp
from numpy import *
import random
import visualization

def sigmoind(x):
	rows = matrix(x).shape[0]
	cols = matrix(x).shape[1]
	for i in range(rows):
		for j in range(cols):
			if (x[i][j] < -500):
				x[i][j] = -500;
			x[i][j] = (1 / (1 + exp(-1*x[i][j])))

def encode(character):
		vector = []
		for i in range(29):
			vector.append(0)

		if (character == ','):
			vector[28] = 1

		elif (character == ' '):
			vector[27] = 1

		elif (character == '.'):
			vector[26] = 1

		elif (ord(character) >= ord('a') and ord(character) <= ord('z')):
			vector[ord(character) - ord('a')] = 1

		return vector 

def decode(next):
		if (next == 28):
			return ','

		if (next == 27):
			return ' '

		if (next == 26):
			return '.'

		next += ord('a')
		if (next >= ord('a') and next <= ord('z')):
			return str(unichr(next))
		
		print next, " did not match anything"
		return ' ' 

def winnertakesall(prediction):
	maximum = prediction[0]
	next = 0;
	#print "len ", len(prediction.T), "\n"
	for i in range(1,len(prediction)):
		#print "pi ", prediction[i]
		if (prediction[i] > maximum):
			next = i
			break
	return next

def draw(prediction):
	newlist = []
	for i in range(len(prediction)):
		for j in range(5):
			if (random.random() < prediction[i]):
				newlist.append(i)

	if (len(newlist) == 0):
		return 0
	random.shuffle(newlist)
	#print newlist
	#visualization.plot_vector(newlist)
	index = random.randint(0, len(newlist)-1)
	return newlist[index]

def mixedstrategy(prediction, power):
	newlist = []
	for i in range(len(prediction)):
		p = prediction[i, 0]
		newlist.append(pow(p, power))
	#visualization.plot_vector(prediction)
	return draw(newlist)

def rmse(prediction, target):
	N = len(prediction)
	return (linalg.norm(prediction - target) / sqrt(N))







