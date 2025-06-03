
import numpy as np
import Box2D as b2
from Ball import Ball

class GeneticsManager:
    def __init__(self, screen):
        self.steps = 100
        self.time_step = 1/60
        self.vel_iters, self.pos_iters = 8, 3
        self.screen = screen
        self.population_size = 50
        self.elite_size = 20
        self.mutation_rate = 0.1
        self.crossover_rate = 0.5
        self.population = []

        self.generation = 0
        self.max_generations = 300

        self.done = False
        self.optimalResultIndex = None

        self.population = self.createPopulationAdn()
    
    def createWorld(self):
        world = b2.b2World()
        return world
    def createPopulationAdn(self):
        population = []
        for i in range(self.population_size):
            individual = Ball(self.createWorld, self.screen.get_width()/2, self.screen.get_height()/2+100, 25)
            population.append(individual)
        return population
    
    def fitness(self):
        fitness_values = []
        for individual in self.population:
            fitness = self.simulate(self.screen, individual)
            fitness_values.append(fitness)
        return fitness_values
    
    def simulate(self, screen, individual):
        fitness = 0
        for _ in range(self.steps):
            individual.world.Step(self.time_step, self.vel_iters, self.pos_iters)
            if individual.position.y > 0:
                fitness += 1

        return fitness



    def elitist_selection(self, fitness_values):
        selected_indices = np.argsort(fitness_values)
        best_indices = selected_indices[:self.elite_size]
        matching_pool = [self.population[i] for i in best_indices]
        return matching_pool

    def crossover5050(self, parent1, parent2):
        child = Ball(self.createWorld())
        for i in range(len(parent1.adn)):
            if np.random.rand() < self.crossover_rate:
                child.adn[i].angle = parent1.getAngleFromGene(i)
                child.adn[i].y = parent1.getYPosFromGene(i)
                child.adn[i].x = parent1.getXPosFromGene(i)
            else:
                child.adn[i].angle = parent2.getAngleFromGene(i)
                child.adn[i].y = parent2.getYPosFromGene(i)
                child.adn[i].x = parent2.getXPosFromGene(i)
        return child
    def mutate(self, child):
        for i in range(len(child.adn)):
            if np.random.rand() < self.mutation_rate:
                child.mutateAngle(i)
                child.mutateYPos(i)
                child.mutateXPos(i)
        return child
    


    def update(self):
        if (self.done == True):
            return

        fitness_values = self.fitness()
        self.population[0].draw(self.screen)

        print(f"Generation {self.generation}")
        print(f"Fitness values: {fitness_values}")

        if 0 in fitness_values:
            self.done = True
            self.optimalResultIndex = fitness_values.index(0)
            print("Fitness 0 found! Stopping evolution.")
            
            
        if self.generation == self.max_generations:
            print("Max generations reached")
            self.done = True

            self.optimalResultIndex = fitness_values.index(min(fitness_values))

        parents = self.elitist_selection(fitness_values)
        childrenPopulation = []

        while len(childrenPopulation) < self.population_size:
            parent1 = np.random.choice(parents)
            parent2 = np.random.choice(parents)
            
            child = self.crossover5050(parent1, parent2)

            if np.random.rand() < self.mutation_rate:
                self.mutate(child)

            childrenPopulation.append(child)

        #revisar destroy
        
        self.population.clear()

        print("Skipping to Next Generation")
        self.population = childrenPopulation
        self.generation += 1