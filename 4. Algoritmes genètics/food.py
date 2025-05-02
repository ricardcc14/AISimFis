import pygame
import numpy as np

class Food:
    def __init__ (self, radius, color):
        self.radius = radius
        self.pos = np.array([np.random.randint(self.radius, 800 - self.radius), np.random.randint(self.radius, 600 - self.radius)])
        self.color = color

    def reposition(self, screen):
        self.pos = np.array([np.random.randint(self.radius, screen.get_width() - self.radius), np.random.randint(self.radius, screen.get_height() - self.radius)])

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
