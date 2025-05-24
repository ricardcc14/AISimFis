import pygame
from Box2D import *

class Surface:
    def __init__(self, world, x, y, w, h):
        self.w = w
        self.h = h

        bd = b2BodyDef()
        bd.position = (x, y)
        bd.type = b2_staticBody
        bd.userData = self
        self.body = world.CreateBody(bd)

        ps = b2PolygonShape()
        ps.SetAsBox(w/2, h/2)
        fd = b2FixtureDef()
        fd.shape=ps
        fd.density = 1
        fd.friction = 0.1
        fd.restitution = 0.5
        self.body.CreateFixture(fd)
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, "black", (self.body.position.x-self.w/2, screen.get_height()-self.body.position.y-self.h/2, self.w, self.h))