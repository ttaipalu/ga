"""  
Genetic algorithm basic functionality testing
Tapio Taipalus 2014
"""

import GA 
import math
import matplotlib.pyplot as plt
import unittest 

SCALE = 10.0
DATA_POINTS_NUM = 100
A = -3.2
B = -2.3
C = 4.
D = 0.

REFERENCE = [A, B, C, D]
	
def polynomi_3N(N,X):
	"""Third degree polynomial function
	N - list of polynom terms [A, B, C, D]
	X - point to calculate the value from
	Returns value of the polynomial function with terms N at X.
	"""
	Y = N[0]*X*X*X + N[1]*X*X + N[2]*X + N[3]
	return Y
  
def calculate_fitness(pTarget, pCandidate):
	"""compare pTarget and pCandidate and tell 
	how good mach they are. Bigger number -> better match"""
	err = 0
	for i in range(len(pTarget)):
		err += math.sqrt((pTarget[i] - pCandidate[i]) * (pTarget[i] - pCandidate[i])) 
	ret = 1000 - err
	if ret < 0:
		ret = 0
	return ret
	#return 1./err
  
def test_GA_sanity():
	"""test the GA algorithm syntax"""
	ga = GA.GA(2,3)
	genomes = ga.seedGenomes()
	if len(genomes) != 2:
		print "Wrong number of genomes"
	if len(genomes[0]) != 3:
		print "Wrong size in genomes"
	#print genomes
	#live and learn
	fitnesses = [23, 45]
	ga.fitnessUpdate(fitnesses)
	genomes2 = ga.createNextGeneration()
	if len(genomes2) != 2:
		print "Wrong number of genomes"
	if len(genomes2[0]) != 3:
		print "Wrong size in genomes"
	#print genomes2

class SanityCheck(unittest.TestCase):        
	def testSanity(self):                    
		"""test the GA algorithm syntax"""
		ga = GA.GA(2,3)
		genomes = ga.seedGenomes()
		self.assertEqual(len(genomes), 2, 
		                 "Wrong number of genomes")
		self.assertEqual(len(genomes[0]), 3, 
		                 "Wrong size in genomes")
		#print genomes
		#live and learn
		fitnesses = [23, 45]
		ga.fitnessUpdate(fitnesses)
		genomes2 = ga.createNextGeneration()
		self.assertEqual(len(genomes2), 2, 
                                 "Wrong number of genomes")
		self.assertEqual(len(genomes2[0]), 3, 
                                 "Wrong size in genomes")
	
class FitnessCheck(unittest.TestCase):        
	def test_greaterThanZero(self):                    
		"""generate two sets of numbers and compare them"""
		X = []
		Y1 = []
		Y2 = []
		candidate = [0,2,3,4]
		for i in range(DATA_POINTS_NUM):
			X.append((i - DATA_POINTS_NUM/2)*0.1)
			Y1.append(polynomi_3N(REFERENCE, X[-1]))
			Y2.append(polynomi_3N(candidate, X[-1]))
		ret = calculate_fitness(Y1, Y2)
		self.assertFalse( 0 > ret, 
		                 "Something wrong with fitness calculation")
		print ret
  
def prescale(pData):
	data = []
	for d in pData:
		data.append(d*SCALE - SCALE/2.)
	return data

def normalize(pData):
	data = []
	for d in pData:
		data.append((d + SCALE/2.)/SCALE)
	return data
  
def test_GA():
	"""test the GA algorithm with 3th degree polynom"""
	generationSize = 150
	mutationProb = 0.01
	generations = 500
	X = []
	T = []
	Y = []  
	fitnesses = [0]*generationSize
	for i in range(DATA_POINTS_NUM):
		X.append((i - DATA_POINTS_NUM/2)*0.1)
		T.append(polynomi_3N(REFERENCE, X[-1]))
		Y.append(0)
	
	ga = GA.GA(generationSize, 4, mutationProb)
	genomes = ga.seedGenomes()
	#plot initial genomes
	plt.figure(1)
	plt.title('Initial genomes')
	for i in range(len(genomes)):
		Genome = prescale(genomes[i])
		print Genome
		for j in range(DATA_POINTS_NUM):
			Y[j] = (polynomi_3N(Genome, X[j]))
		fitnesses[i] = calculate_fitness(T, Y)
		plt.plot(X,Y, 'b-')
	plt.plot(X,T, 'r-')
		
	
	#live and learn
	for k in range(generations):
		print ".",
		for i in range(len(genomes)):
			Genome = prescale(genomes[i])
			for j in range(DATA_POINTS_NUM):
				Y[j] = (polynomi_3N(Genome,X[j]))
			fitnesses[i] = calculate_fitness(T, Y)
		ga.fitnessUpdate(fitnesses)
		genomes = ga.createNextGeneration()
		
	#plot final genomes
	plt.figure(2)
	plt.title('Final genomes')
	print "\nfinal Genomes"
	for i in range(len(genomes)):
		Genome = prescale(genomes[i])
		for j in range(DATA_POINTS_NUM):
			Y[j] = (polynomi_3N(Genome,X[j]))
		print "fit:%5.1f [%7.4f, %7.4f, %7.4f, %7.4f]"%\
		      (calculate_fitness(T, Y), Genome[0],
		       Genome[1], Genome[2], Genome[3])
		plt.plot(X,Y, 'b-')
	plt.plot(X,T, 'r-')
		
	#plot progress
	P = []
	history = ga.generations[:]
	for f in history:
		#f[1].sort()
		P.append(max(f[1]))
	plt.figure(3)
	plt.title('progress')
	plt.plot(P)
	plt.show()
	
	#print the result:	
	bestGene = fitnesses.index(max(fitnesses))
	G = prescale(genomes[bestGene])
        print ""
	print "And the result is:"
	print "%.4f => %.4f (%.4f)"%(A, G[0], abs(A - G[0]))
	print "%.4f => %.4f (%.4f)"%(B, G[1], abs(B - G[1]))
	print "%.4f => %.4f (%.4f)"%(C, G[2], abs(C - G[2]))
	print "%.4f => %.4f (%.4f)"%(D, G[3], abs(D - G[3]))

  
if __name__=="__main__":
	#unittest.main()
	test_GA()
	
