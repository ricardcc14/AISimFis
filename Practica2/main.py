#Libraries
import pygame
import Box2D as b2
import utils
import time

from Ball import Ball
from EvolutionManager import EvolutionManager

# pygame setup
pygame.init()
screen = pygame.display.set_mode((640, 400))
clock = pygame.time.Clock()
frames = 60
running = True

#Controllers
evolutionManager = EvolutionManager(screen)
evolutionManager.run()

while running:
    screen.fill('gray')
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(frames)

pygame.quit()