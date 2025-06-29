import pygame
import numpy as np
import Box2D as b2
from ContactListener import ContactListener
from Individual import Individual
from Rectangle import Rectangle


class EvolutionManager:
    def __init__ (self, screen):

        self.screen = screen
        self.frames = 60

        self.population_size = 100
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
        contactListener = ContactListener()
        world.contactListener = contactListener
        return world
    
    def resultFound(self):
        return (self.done)
    
    def createPopulationAdn(self):
        population = []
        for i in range(self.population_size):
            individual = Individual(self.createWorld())
            population.append(individual)
        return population
    
    def fitness(self):
        fitness_values = []
        for individual in self.population:
            fitness = individual.simulate(self.screen)
            fitness_values.append(fitness)
        return fitness_values
            
    def elitist_selection(self, fitness_values):
        selected_indices = np.argsort(fitness_values)
        best_indices = selected_indices[:self.elite_size]
        matching_pool = [self.population[i] for i in best_indices]
        return matching_pool

    def crossover5050(self, parent1, parent2):
        child = Individual(self.createWorld())
        # Primer copia angles
        angles = []
        for i in range(len(parent1.adn)):
            if np.random.rand() < self.crossover_rate:
                angles.append(parent1.getAngleFromGene(i))
            else:
                angles.append(parent2.getAngleFromGene(i))

        # Ara reconstruim rectangles connectats segons angles
        distance_between_centers = 50
        child.adn = []

        for i in range(len(angles)):
            if i == 0:
                x = 100
                y = 200
                angle = angles[i]
                rect = Rectangle(child.world, x, y, angle)
                child.adn.append(rect)
            else:
                prev = child.adn[-1]
                angle = angles[i]

                dx = np.cos(prev.angle) * distance_between_centers
                dy = np.sin(prev.angle) * distance_between_centers

                new_x = prev.x + dx
                new_y = prev.y + dy

                rect = Rectangle(child.world, new_x, new_y, angle)
                child.adn.append(rect)
        return child

    def mutate(self, child):
        for i in range(len(child.adn)):
            if np.random.rand() < self.mutation_rate:
                child.mutateAngle(i)
                
        return child
    
    def update(self):
        if (self.done == True):
            return

        fitness_values = self.fitness()
       

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
        
        self.population.clear()

        print("Skipping to Next Generation")
        self.population = childrenPopulation
        self.generation += 1

    def drawSolution(self):

        index = self.optimalResultIndex
        
        if (index != None):
            self.population[index].draw(self.screen)
        for ball in self.population[index].balls:
            ball.draw(self.screen)

        pygame.display.flip()
        pass






        