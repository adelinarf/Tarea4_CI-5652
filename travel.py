from sys import maxsize 
from itertools import permutations
import random 
random.seed(0)

def travellingSalesmanProblem(graph, s): 

	vertex = [] 
	for i in range(len(graph[0])): 
		if i != s: 
			vertex.append(i) 

	min_path = maxsize 
	next_permutation=permutations(vertex)
	M = []
	for i in next_permutation:
		N = [[0 for x in range(len(graph[0]))] for i in range(len(graph[0]))]
		current_pathweight = 0

		viejo = M
		k = s 
		for j in i: 
			current_pathweight += graph[k][j] 
			N[k][j]=1
			k = j 
		current_pathweight += graph[k][s] 
		N[k][s]=1

		min_path = min(min_path, current_pathweight) 
		if min_path==viejo:
			M = N
		else:
			M = N

	return [min_path,M]



def f(solution,graph):
	suma=0
	for x in range(len(solution)):
		for y in range(len(solution[x])):
			if solution[x][y]==1:
				suma+=graph[x][y]
	return suma


def getParents(population):
	firstParent = population[random.randint(0, len(population)-1)]
	secondParent = population[random.randint(0, len(population)-1)]
	return [firstParent,secondParent]

def pos_uno(arreglo):
	found =None
	for x in range(len(arreglo)):
		if arreglo[x]==1:
			found= x
	return found


def mutation(children):
	for child in children:
		from_ = random.randint(0, len(child)-1)
		to_ = random.randint(0, len(child)-1)
		child[from_],child[to_] = child[to_],child[from_]
	return children

import numpy as np
def isSolution(children):
	suma = np.zeros([len(children),])
	for c in children:
		suma+=c
	for r in suma:
		if r!=1:
			return False
	return True

'''OPERADOR RESPETUOSO'''

def crossover_respetuoso(parents,graph):
	mother = parents[0]
	father = parents[1]
	child = [[0 for x in range(len(mother))] for i in range(len(mother))]
	taken = []

	for x in range(len(mother)):
		for y in range(len(mother[x])):
			if mother[x][y]==father[x][y]:
				taken.append(y)
				child[x][y]=mother[x][y]

	available = list(set([x for x in range(len(mother))]) - set(taken))
	for number in available:
		for x in range(len(mother)):
			if child[x][number] == 0:
				child[x][number] = 1
				available.remove(number)
	return child



'''OPERADOR SURTIDO'''

def crossover_surtido(parents,graph):
	mother = parents[0]
	father = parents[1]
	child = [[0 for x in range(len(mother))] for i in range(len(mother))]
	taken = []

	for x in range(len(mother)):
		for y in range(len(mother[x])):
			if mother[x][y]==father[x][y] and y not in taken:
				taken.append(y)
				child[x][y]=1
			else:
				pos_mother = pos_uno(mother[x])
				pos_father = pos_uno(father[x])
				s = [x for x in range(len(mother))]
				faltan = list(set(s)-set(taken))
				if pos_mother==None or pos_father==None:
					if len(faltan)>1:
						pos = random.randint(0, len(faltan)-1)
						child[x][faltan[pos]]=1
						taken.append(faltan[pos])
					else:
						continue
				else:
					if graph[x][pos_mother]<graph[x][pos_father] and (pos_mother not in taken):
						child[x][pos_mother] = 1
						taken.append(pos_mother)
					elif graph[x][pos_father]<graph[x][pos_mother] and (pos_father not in taken):
						child[x][pos_father] = 1
						taken.append(pos_father)
	return child



'''OPERADOR TRANSMISOR'''

def crossover_transmisor(parents,graph):
	mother = parents[0]
	father = parents[1]
	child = parents[random.randint(0, len(parents)-1)]
	return child

def crossover_dinastica_optima(parents,graph):
	mother = parents[0]
	father = parents[1]
	children = []
	for x in range(len(mother)):
		child = [[0 for x in range(len(mother))] for i in range(len(mother))]
		child[x] = mother[x]
		for y in range(len(father)):
			if x!=y:
				child[y] = father[x]
		if isSolution(child):
			children.append(child)

	for x in range(len(mother)):
		for y in range(len(mother[x])):
			child = [[0 for x in range(len(mother))] for i in range(len(mother))]
			child[x][y] = mother[x][y]
			for z in range(len(father)):
				for w in range(len(father)):
					if x!=z and w!=y:
						child[z][w] = father[z][w]
			if isSolution(child):
				children.append(child)
	for child in children:
		a = mutation(child)
		if isSolution(a):
			children.append(a)
	return children



def getChildren(parents,graph,crossF):
	crossing = crossF(parents,graph)
	if isSolution(crossing):
		mutations = mutation(crossing)
		if isSolution(mutations):
			return [crossing,mutations]
		return [crossing]
	t = travellingSalesmanProblem(graph,0)
	if isSolution(t[1]):
		return [t[1]]


def bestOf(population,graph):
	maximo = 0
	pp = 0
	for people in population:
		val = f(people,graph)
		if val>maximo:
			maximo=val
			pp = people
	return pp


import time

def memetic(graph, cross):
	size = 10
	s = travellingSalesmanProblem(graph,0)
	population = [s[1] for x in range(size)]
	bestSol = bestOf(population,graph)
	generation=0 
	lastGen = 0
	MAX_IT = 100
	start = time.time()
	while True:
		end = time.time()
		if end-start==100:
			break
		if (generation - lastGen > MAX_IT):
			break

		parents = getParents(population)
		if cross=="DOR":
			children = crossover_dinastica_optima(parents,graph)
		elif cross=="res":
			children = getChildren(parents,graph,crossover_respetuoso)
		elif cross=="sur":
			children = getChildren(parents,graph,crossover_surtido)
		elif cross=="trans":
			children = getChildren(parents,graph,crossover_transmisor)
		population += children
		populationBest = bestOf(population,graph)
		if f(bestSol,graph) > f(populationBest,graph):
			bestSol = populationBest
			population = [populationBest]
			lastGen = generation
		
		generation+=1
	return bestSol


def call(graph,types):
	d = memetic(graph,"DOR")
	print("Solucion "+types+" = ",d)
	print("Costo = ",f(d,graph))
	print()

def main(graph):
	print("Solución al problema del agente viajero simétrico para:")
	print(np.array(graph))
	print()
	call(graph,"DOR")
	call(graph,"res")
	call(graph,"sur")
	call(graph,"trans")

graph = [[0, 10, 15, 20], [10, 0, 35, 25], 
		[15, 35, 0, 30], [20, 25, 30, 0]] 
main(graph)