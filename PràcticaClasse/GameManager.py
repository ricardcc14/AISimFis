from Ball import Ball
from Surface import Surface
import Box2D as b2
import pygame


class GameManager:
    def __init__(self, frames, screen):
        # Box2D
        self.screen = screen
        self.world = b2.b2World()
        self.time_step = 1/frames
        self.vel_iters, self.pos_iters = 8, 3

        self.ball = Ball(self.world, self.screen.get_width()/2, self.screen.get_height()/2+100, 25)
        self.surface = Surface(self.world, self.screen.get_width()/2, 0, self.screen.get_width(), 20)

    def renderGame(self):
        self.screen.fill("gray")
        self.world.Step(self.time_step, self.vel_iters, self.pos_iters)
        self.ball.draw(self.screen)
        self.surface.draw(self.screen)

    def makeBallJump(self):
        self.ball.jump(self.screen, pygame.mouse.get_pos(), 1.5)






