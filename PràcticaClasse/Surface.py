import pygame
import Box2D as b2
from utils import pixelToWorld, worldToPixel

class Surface:
    def __init__(self, world, x, y, w, h):
        self.w = pixelToWorld(w)
        self.h = pixelToWorld(h)

        bodydf = b2.b2BodyDef()
        bodydf.position = (pixelToWorld(x), pixelToWorld(y))
        bodydf.type = b2.b2_staticBody
        self.body:b2.b2Body = world.CreateBody(bodydf)

        boxshape = b2.b2PolygonShape(box=(self.w/2, self.h/2))
        fd = b2.b2FixtureDef()
        fd.shape=boxshape
        fd.density = 1
        fd.friction = 0.1
        self.body.CreateFixture(fd)
        pass

    def draw(self, screen):
        pos = worldToPixel(self.body.position)
        w = worldToPixel(self.w)
        h = worldToPixel(self.h)
        pygame.draw.rect(screen, "black", (pos.x-w/2, screen.get_height()-pos.y-h/2, w, h))
        pass