
import utils
import pygame
import numpy as np
import Box2D as b2
from ContactListener import ContactListener
from Floor import Floor
from Ball import Ball
from Individual import Individual

class EvolutionManager:
    def __init__ (self, screen):

        self.screen = screen

        self.frames = 60
        # Box2D
        # self.world = b2.b2World()
        # self.time_step = 1/self.frames
        # self.vel_iters, self.pos_iters = 8, 3
        # contactListener = ContactListener()
        # self.world.contactListener = contactListener

        # self.floor = Floor(self.world, 0, 0, self.screen.get_width(), 100)


        # Genetics algorithm parameters
        
        self.population_size = 100
        self.elite_size = 20
        self.mutation_rate = 0.1
        self.crossover_rate = 0.5
        self.population = []

        self.population = self.createPopulationAdn()


    def createWorld(self):
        world = b2.b2World()
        contactListener = ContactListener()
        world.contactListener = contactListener
        return world
    #Funció que inicialitza un nivell extraient la informació del JSON
    def createPopulationAdn(self):
        population = []
        for i in range(self.population_size):
            individual = Individual(self.createWorld())
            population.append(individual)
        return population
    def fitness(self):
        fitness_values = []
        for individual in self.population:
            fitness = individual.simulate()
            fitness_values.append(fitness)
        return fitness_values
            

    def elitist_selection(self, fitness_values):
        selected_indices = np.argsort(fitness_values)
        best_indices = selected_indices[:self.elite_size]
        matching_pool = [self.population[i] for i in best_indices]
        return matching_pool

    def crossover5050(self, parent1, parent2):
        child = Individual(self.createWorld())
        for i in range(len(parent1.adn)):
            if np.random.rand() < self.crossover_rate:
                child.adn[i] = parent1.getAdn(i)
            else:
                child.adn[i] = parent2.getAdn(i)
        return child
    def mutate(self, child):
        for i in range(len(child.adn)):
            if np.random.rand() < self.mutation_rate:
                child.mutateAngle(i)
        return child

    def run(self):
        done = False
        generation = 0

        while not done:
            print(f"Generation {generation}")
            fitness_values = self.fitness()
            print(f"Fitness values: {fitness_values}")
            # Comprova si algun individu té fitness 0
            # if 0 in fitness_values:
            #     done = True
                
            #     print("Fitness 0 found! Stopping evolution.")
            #     break

            parents = self.elitist_selection(fitness_values)

            childrenPopulation = []
            while len(childrenPopulation) < self.population_size:
                parent1 = np.random.choice(parents)
                parent2 = np.random.choice(parents)
                child = self.crossover5050(parent1, parent2)

                if np.random.rand() < self.mutation_rate:
                    self.mutate(child)

                childrenPopulation.append(child)

            for individual in self.population:
                individual.destroy()

            self.population = childrenPopulation
            generation += 1
    
    def draw(self):
        for individual in self.population:
            individual.draw(self.screen)
        
        pygame.display.flip()
        pass


        