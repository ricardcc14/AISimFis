import pygame
import Box2D as b2
from Ball import Ball
from Surface import Surface
from GameManager import GameManager
import numpy as np
from GeneticsManager import GeneticsManager


# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
frames = 60
running = True

gameManager = GameManager(frames, screen)
timeLastJump = 0


solutionFound = False

### 1- TROBAR XXNN ÒPTIMA
### Genetics manager que controla tota la població
### CREAR POBLACIÓ: cada individu conté els pesos de la xarxa neuronal 
geneticsManager = GeneticsManager(frames, screen)


solutionFound = True 

while (solutionFound == False):
    ### CALCULAR FITNESS DE LA GENERACIÓ
    '''def getPopulationFitness(self):
        fitness_values = self.fitness()

        if 0 in fitness_values:
            solutionFound = True
            self.optimalResultModel = fitness_values.index(0).Model
            print("Fitness 0 found! Stopping evolution.")
            
        if self.generation == self.max_generations:
            print("Max generations reached")
            self.done = True

            self.optimalResultIndex = fitness_values.index(0).Model

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
        '''



### 2- RENDER DEL JOC AMB LA SOLUCIÓ FINAL

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if event.type == pygame.MOUSEBUTTONDOWN:

    if (solutionFound):

        gameManager.renderGame()
        direction = np.array([1, 1])

        currentTime = pygame.time.get_ticks()
        if currentTime - timeLastJump >= 3000:
            gameManager.makeBallJump(direction)
            timeLastJump = pygame.time.get_ticks()

        # flip() the display to put your work on screen
        pygame.display.flip()

    clock.tick(frames)  # limits FPS to 60

pygame.quit()