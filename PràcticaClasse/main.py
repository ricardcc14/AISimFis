import pygame
import Box2D as b2
from Ball import Ball
from Surface import Surface

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
frames = 60
running = True

# Box2D
world = b2.b2World()
time_step = 1/frames
vel_iters, pos_iters = 8, 3

# Data
ball = Ball(world, screen.get_width()/2, screen.get_height()/2+100, 25)
surface = Surface(world, screen.get_width()/2, 0, screen.get_width(), 20)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            ball.jump(screen, pygame.mouse.get_pos(), 1.5)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray")

    # RENDER YOUR GAME HERE
    world.Step(time_step, vel_iters, pos_iters)

    ball.draw(screen)
    surface.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(frames)  # limits FPS to 60

pygame.quit()