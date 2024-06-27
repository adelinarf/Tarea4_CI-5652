import random
import math
import copy
import sys	 
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

def fitness_rastrigin(position):
	fitnessVal = 0.0
	for i in range(len(position)):
		xi = position[i]
		fitnessVal += (xi * xi) - (10 * math.cos(2 * math.pi * xi)) + 10
	return fitnessVal

class Particle:
	def __init__(self, fitness, dim, minx, maxx, seed):
		self.rnd = random.Random(seed)
		self.seed = seed
		self.position = self.initialize_particles_pos()

		self.velocity = self.initialize_particles_vel()

		self.best_part_pos = self.position

		self.fitness = fitness(self.position)

		self.best_part_pos = copy.copy(self.position) 
		self.best_part_fitnessVal = self.fitness

	def initialize_particles_pos(self):
		X,Y=4,8
		positions = [[0,X+1],[Y+1,0],[0,-X-1],[-Y-1,0]]
		return positions[self.seed]
	def initialize_particles_vel(self):
		Z = 4
		vels = [[0,(Z+1)/2],[(Z+1)/2,0],[0,(Z+1)/2],[(Z+1)/2,0]]
		return vels[self.seed]



def plotting(X,Y,title,velX,velY,name):
	fig, ax = plt.subplots(1, 1)
	fig.set_size_inches(5,5)
	 
	def animate(i):
		ax.clear()
		colors=['green','blue','pink','red']
		for x in range(4):
			ax.annotate(str(math.trunc(velX[i][x]))+"i + "+str(math.trunc(velY[i][x]))+"j", xy=(X[i][x],Y[i][x]), 
                xytext=(X[i][x]-1,Y[i][x]+1), textcoords='offset points', 
                fontsize=8, 
                arrowprops={'arrowstyle': '-|>', 'color': 'black'})
			ax.plot(X[i][x], Y[i][x], color=colors[x], label='Partícula'+str(x+1), marker='o')
		ax.set_xlim([-10, 10])
		ax.set_ylim([-10, 10])
		ax.set_title(title+" Iteración "+str(i+1), fontsize=20)
		ax.legend()
	ani = FuncAnimation(fig, animate, frames=len(X),
						interval=500, repeat=False)
	ani.save(name+".gif", dpi=300,writer=PillowWriter(fps=1))


def pso(fitness, max_iter, n, dim, minx, maxx):
	w = 0.729 # inertia
	c1 = 1.49445 # cognitive (particle)
	c2 = 1.49445 # social (swarm)

	rnd = random.Random(0)

	swarm = [Particle(fitness, dim, minx, maxx, i) for i in range(n)] 

	best_swarm_pos = [0.0 for i in range(dim)]
	best_swarm_fitnessVal = sys.float_info.max 

	for i in range(n): 
		if swarm[i].fitness < best_swarm_fitnessVal:
			best_swarm_fitnessVal = swarm[i].fitness
			best_swarm_pos = copy.copy(swarm[i].position) 

	Iter = 0
	X1,Y1=[],[]
	X1_best,Y1_best=[],[]
	velX1, velY1 = [],[]
	while Iter < max_iter:
		
		if Iter % 10 == 0 and Iter > 1:
			print("Iter = " + str(Iter) + " best fitness = %.3f" % best_swarm_fitnessVal)

		X,Y=[],[]
		X_best,Y_best=[],[]
		velX,velY=[],[]
		print("Iteración",Iter)
		print("................")
		print()
		for i in range(n):
		
			for k in range(dim): 
				r1 = rnd.random() 
				r2 = rnd.random()
			
				swarm[i].velocity[k] = ( 
										(w * swarm[i].velocity[k]) +
										(c1 * r1 * (swarm[i].best_part_pos[k] - swarm[i].position[k])) +
										(c2 * r2 * (best_swarm_pos[k] -swarm[i].position[k])) 
									) 


				
				if swarm[i].velocity[k] < minx:
					swarm[i].velocity[k] = minx
				elif swarm[i].velocity[k] > maxx:
					swarm[i].velocity[k] = maxx


			for k in range(dim): 
				swarm[i].position[k] += swarm[i].velocity[k]

			swarm[i].fitness = fitness(swarm[i].position)

			if swarm[i].fitness < swarm[i].best_part_fitnessVal:
				swarm[i].best_part_fitnessVal = swarm[i].fitness
				swarm[i].best_part_pos = copy.copy(swarm[i].position)

			if swarm[i].fitness < best_swarm_fitnessVal:
				best_swarm_fitnessVal = swarm[i].fitness
				best_swarm_pos = copy.copy(swarm[i].position)
			
			X.append(swarm[i].position[0])
			Y.append(swarm[i].position[1])

			X_best.append(best_swarm_pos[0])
			Y_best.append(best_swarm_pos[1])

			velX.append(swarm[i].velocity[0])
			velY.append(swarm[i].velocity[1])
			print()
			print("Partícula",i+1)
			print("Posición =",swarm[i].position)
			print("Mejor posición =",best_swarm_pos)
			print("Velocidad =",swarm[i].velocity)
			print()
		X1.append(X)
		Y1.append(Y)
		X1_best.append(X_best)
		Y1_best.append(Y_best)
		velX1.append(velX)
		velY1.append(velY)
		Iter += 1
	plotting(X1,Y1,"Ejecución",velX1,velY1,"opt")
	plotting(X1_best,Y1_best,"Mejores posiciones",velX1,velY1,"best")
	return best_swarm_pos


print("Optimización de enjambre de partículas")
dim = 2
fitness = fitness_rastrigin

num_particles = 4
max_iter = 10

print("Número de partículas = " + str(num_particles))
print("Número máximo de iteraciones = " + str(max_iter))
print("\n...\n")


best_position = pso(fitness, max_iter, num_particles, dim, -10.0, 10.0)

print("\n.........\n")
print("\nMejor solución:",["%.6f"%best_position[k] for k in range(dim)])
fitnessVal = fitness(best_position)
print("Fitness para la mejor solución = %.6f" % fitnessVal)