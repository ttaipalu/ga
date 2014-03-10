"""
Genetic algorithm basic functionality
Tapio Taipalus 2014
"""

import random

class GA():
	def __init__(self, generationSize, numberOfGenes, mutationPropability = 0.01):
		"""
		GA(generationSize, numberOfGenes, mutationPropability = 0.01)
		Does the book keeping of GA, the fitness has 
		to be evaluated by the application using this. 
		One gene is a float between 0 and 1. Creates
		the initial generation at init and creates 
		consecutive generations after fitnessUpdate by 
		createNextGeneration() call
		"""
		self.size = generationSize
		self.numberOfGenes = numberOfGenes
		self.genomes = []
		self.generations = []
		self.fitness = []
		self.fitnessHistory = []
		self.generationFitness = 0.
		self.mutationPropability = mutationPropability


	def seedGenomes(self):
		for i in range(self.size):
			self.genomes.append([])
			self.fitness.append(0.)
			for j in range(self.numberOfGenes):
				self.genomes[i].append(random.random())
		return self.genomes[:]
		
	
	def fitnessUpdate(self, fitness):
		"""fitnessUpdate(fitness)
		input "fitness" is a list of fitness values for genomes
		"""
		self.generationFitness = 0.
		for fit in fitness:
			self.generationFitness += fit
		self.fitness = fitness[:]
		
	def createNextGeneration(self):
		"""Creates new generation of genomes and returns it"""
		self.generations.append((self.genomes, self.fitness))
		self.fitnessHistory.append(self.generationFitness)
                #the best performer lives for ever
		self.genomes[0] = self.genomes[self.fitness.index(max(self.fitness))]
		#rest of the next generation
		for i in range(1, self.size):
			a = self.selectMate(-1)
			b = self.selectMate(a)
			self.genomes[i] = self.crossing(self.genomes[a], self.fitness[a],
			                                self.genomes[b], self.fitness[b])
		return self.genomes
			
	def selectMate(self, pPartner):
		"""Selectes the mate based on roulette selection
		pPartner is ID of already found partner so that it wont be 
		selected again. If pPartner is below zero, it is ignored."""
		if pPartner < 0:
			m = (self.generationFitness)*random.random()
			for i in range(self.size):
				m -= self.fitness[i]
				if m <= 0:
					return i
		else:
			m = (self.generationFitness - self.fitness[pPartner])*random.random()
			for i in range(self.size):
				if i == pPartner:
					continue
				m -= self.fitness[i]
				if m <= 0:
					return i
		print "You should never see this print from GA.py!!!"
		return 0
		
	def crossing(self, genom1, fitness1, genom2, fitness2):
		newGenom = []
		s = fitness1 + fitness2
		for i in range(len(genom1)):
			#mutation
			if random.random() < self.mutationPropability:
				newGenom.append(random.random())
				continue
			#selection
			r = random.random()
			if r < 0.5:
				newGenom.append(genom1[i])
			else:
				newGenom.append(genom2[i])
		return newGenom
  
