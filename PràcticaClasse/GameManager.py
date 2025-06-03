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

        self.platmorms = []

    def createWorld(self):
        self.platforms = []
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        num_platforms = 4
        vertical_spacing = screen_h / 2

        for i in range(num_platforms):
            
            if i % 2 == 0:
                x = screen_w * 0.25
            else:
                x = screen_w * 0.75

            # Separació vertical per 1/2 alçada, començant a dalt
            y = i * vertical_spacing

            platform = Surface(self.world, x, y, 200, 20)
            self.platforms.append(platform)

    def renderGame(self):
        self.screen.fill("gray")
        self.world.Step(self.time_step, self.vel_iters, self.pos_iters)
        self.ball.draw(self.screen)
        self.surface.draw(self.screen)


    def makeBallJump(self):
        self.ball.jump(self.screen, pygame.mouse.get_pos(), 1.5)






