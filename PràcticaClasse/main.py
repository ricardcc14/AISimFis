import pygame
import Box2D as b2
from Ball import Ball
from Surface import Surface
from GameManager import GameManager

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
frames = 60
running = True

gameManager = GameManager(frames, screen)
timeLastJump = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if event.type == pygame.MOUSEBUTTONDOWN:
        
    gameManager.renderGame()
    currentTime = pygame.time.get_ticks()
    if currentTime - timeLastJump >= 3000:
        gameManager.makeBallJump()
        timeLastJump = pygame.time.get_ticks()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(frames)  # limits FPS to 60

pygame.quit()