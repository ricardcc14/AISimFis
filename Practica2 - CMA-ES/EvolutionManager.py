import cma
import pygame
import numpy as np
import Box2D as b2
from ContactListener import ContactListener
from Individual import Individual

class EvolutionManager:
    def __init__(self, screen):
        self.screen = screen
        self.frames = 60

        self.population_size = 100
        self.genome_length = 20 

        self.population = []
        self.generation = 0
        self.max_generations = 500

        self.done = False
        self.optimalResultIndex = None
        self.toFinish = False

        self.displayWorld = self.createWorld()
        self.displayIndividual = Individual(self.displayWorld)

        self.sigma = 1.0
        self.mu = np.random.uniform(low=-np.pi, high=np.pi, size=self.genome_length).tolist()

        self.es = cma.CMAEvolutionStrategy(
            self.mu,
            self.sigma,
            {
                'popsize': self.population_size,
                'maxiter': self.max_generations
            }
        )

        self.population = self.askPopulation()
        self.best_individual = None

    def createWorld(self):
        world = b2.b2World()
        contactListener = ContactListener()
        world.contactListener = contactListener
        return world

    def resultFound(self):
        return self.done

    def askPopulation(self):
        
        angles_population = self.es.ask()
        population = []
        for angles in angles_population:
            individual = Individual(self.createWorld())
            individual.buildFromAngles(angles)
            population.append(individual)
        return population

    def fitness(self):
        
        fitness_values = []
        for individual in self.population:
            fitness = individual.simulate()
            fitness_values.append(fitness)
        return fitness_values

    def update(self):
        if self.done:
            return

        fitness_values = self.fitness()

        print(f"Generation {self.generation}")
        print(f"Fitness values: {fitness_values}")

        self.es.tell([individual.getAngles() for individual in self.population], fitness_values)

        prev_fit = self.best_individual.f if self.best_individual else np.inf
        self.best_individual = self.es.best

        if self.best_individual.f < 0.001 and abs(prev_fit - self.best_individual.f) < 0.0001:
            if self.toFinish:
                print("Solution converged. Stopping.")
                self.done = True
                self.prepareVisualization()

                best_angles = self.best_individual.x
                best = Individual(self.createWorld())
                best.buildFromAngles(best_angles)
                self.population = [best] * self.population_size
                self.optimalResultIndex = 0
                return
            else:
                self.toFinish = True
                print("Convergence detected, restarting optimization")
                self.es = cma.CMAEvolutionStrategy(
                    self.es.mean,
                    self.sigma,
                    {'popsize': self.population_size}
                )

        self.population = self.askPopulation()
        self.generation += 1

        if self.generation >= self.max_generations:
            print("Max generations reached.")
            self.done = True
            self.optimalResultIndex = 0


    def prepareVisualization(self):
        best_angles = self.best_individual.x
        self.displayIndividual.buildFromAngles(best_angles)


    def renderSolution(self):
    
        index = self.optimalResultIndex
        if index is None:
            return
        
        self.displayWorld.Step(1/60, 8, 3)
        self.displayIndividual.draw(self.screen)


        

