
import numpy as np
import Box2D as b2
from Ball import Ball
from GameManager import GameManager

class GeneticsManager:
    def __init__(self, frames, screen):
        self.population_size = 6
        self.elite_size = 3
        self.mutation_rate = 0.1
        self.crossover_rate = 0.5
        self.population = []

        self.generation = 0
        self.max_generations = 10

        self.done = False
        self.optimalResultIndex = None

        self.screen = screen
        self.frames = frames

        self.population = self.createPopulationAdn()
    
    def createPopulationAdn(self):
        population = []
        for i in range(self.population_size):
            individual = GameManager(self.frames, self.screen)
            population.append(individual)
        return population
    
    def getPopulationFitness(self):
        fitness_values = []
        for individual in self.population:
            fitness = self.simulate(self.screen, individual)
            fitness_values.append(fitness)
        return fitness_values
    

    def simulate(self, individual):
        #fitness = individual.geneticSimulation(500)
        fitness = 10

        return fitness

    def elitist_selection(self, fitness_values):
        selected_indices = np.argsort(fitness_values)
        best_indices = selected_indices[:self.elite_size]
        matching_pool = [self.population[i] for i in best_indices]
        return matching_pool

    #def crossover5050(self, parent1, parent2):

    
    #def mutate(self, child):
    