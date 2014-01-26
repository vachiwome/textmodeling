"""
Valentine Chiwome
Echo State Network for text modelling
"""
from numpy import *
from matplotlib.pyplot import *
import scipy.linalg

from Util import encode, decode, winnertakesall, mixedstrategy, draw, sigmoind, rmse

class myesn:
	def __init__(self, _in_units, _h_units, _out_units, _a):
		self._in_units = _in_units
		self._h_units = _h_units
		self._out_units = _out_units
		self._Win = []
		self._W = []
		self._Wout = []
		self._X = []
		self._Y = []
		self._a = _a
		self._data = []
 
	def initData(self, filename):
		f = open(filename, "r")
		text = ""
		for line in f.readlines():
			text += " " + line
		for example in range(len(text)):
			vector = encode(text[example])
			self._data.append(vector)
		print "self._data has dimension => ", array(self._data).shape		


	def setWinAndW(self):
		Win = random.rand(self._h_units,self._in_units+1) - 0.5
		self._Win = Win

		W = random.rand(self._h_units,self._h_units) - 0.5 

		rhow = max(abs(linalg.eig(W)[0]))	
		W *= 1.25 / rhow
		#W /= (0.2 + rhow)
		self._W = W

	def runAndCollectX(self, initLen):
		self._X = zeros((1 + self._in_units + self._h_units, len(self._data) - initLen - 1))
		self._Y = self._data[initLen+1:len(self._data)] 
		#print array(self._X).shape, " _X VS _Y ", matrix(self._Y).shape

		x = zeros((self._h_units,1))
		for t in range(len(self._data)-1):
    			u = self._data[t]
			u = array([u]).T
			#print array(u).shape
    			x = (1-self._a)*x + self._a*tanh( dot( self._Win, vstack((1,u)) ) + dot( self._W, x ) )
			if (t > initLen):			
				self._X[:,t - initLen] = vstack((1,u,x))[:,0]
				#print array(u).shape, array(x).shape

	def trainWout(self, reg):
		X_T = self._X.T
		Y_T = array(self._Y).T

		self._Wout = dot( dot(Y_T,X_T), linalg.inv( dot(self._X,X_T) + reg*eye(1+self._in_units + self._h_units)))
		#print self._Wout

	def run(self, testLen, initLen, power):
		Y = zeros((self._out_units,testLen))
		u = self._data[0]
		u = array([u]).T
		poem = ""
		x = zeros((self._h_units,1))
		trainingError = 0
		for t in range(testLen - 1):
    			x = (1-self._a)*x + self._a*tanh( dot( self._Win, vstack((1,u)) ) + dot( self._W, x ) )
			y = dot( self._Wout, vstack((1,u,x)) )
    			Y[:,t] = y[0,:]
			#y += 0.1
			#sigmoind(y)
			u = y
			"""for index in range(29):
				if (random.rand() < 0.05):
					u[index,0] = u[index,0] + random.rand()
			"""
			if (t > initLen):
				#print "P ", y.T
				#next = decode(draw(y[0,:]))
				#next = decode(winnertakesall(y[0,:]))
				next = decode(mixedstrategy(y, power))
				poem += next
				trainingError += rmse(y[0,:], self._data[t+1]) 
			#u = array([encode(decode(mixedstrategy(y, power)))]).T
			u = array([self._data[t+1]]).T

		print "Training error ", trainingError	
		print poem
		print "\n"

alpha = 0.7
while (alpha >= 0):
	resSize = 400
	while (resSize < 500):
		ridge = 1e-9
		while (ridge <= 1):
			power = 1.5
			while (power < 2.5):
				print "alpha=", alpha, " resSize=", resSize, " ridge=", ridge, " power=", power
				esn = myesn(29, resSize, 29, alpha)
				esn.initData("backup.txt")
				esn.setWinAndW()
				esn.runAndCollectX(1000)
				esn.trainWout(ridge)
				esn.run(1000, 500, power)
				power += 0.5
			ridge *= 10
		resSize *= 2
	alpha -= 0.1
"""
esn = myesn(29, 58, 29, 0.7)
esn.initData("mytext.txt")
esn.setWinAndW()
esn.runAndCollectX(1000)
esn.trainWout(1e-12)
esn.run(1000, 500, 2)
"""

