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
font = pygame.freetype.SysFont("Consolas", 24, "white")

algorithm = "genetic"

algorithmStarted = False
resultFound = False

#Controllers
evolutionManager = EvolutionManager(screen)
optimalResultIndex = None

while running:
    screen.fill('gray')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if (evolutionManager.resultFound() == False):
        evolutionManager.update()
        
        font.render_to(screen, (10, 10), "Running " + algorithm + " algorithm...")

    else:
        font.render_to(screen, (10, 10), "Solution found!")
        evolutionManager.renderSolution()

    pygame.display.flip()
    clock.tick(frames)

pygame.quit()