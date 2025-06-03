import pygame
import Box2D as b2
from utils import pixelToWorld, worldToPixel

class Surface:
    def __init__(self, world, x, y, w, h):
        self.w = pixelToWorld(w)
        self.h = pixelToWorld(h)

        self.initialX = pixelToWorld(x)
        self.initialY = pixelToWorld(y)

        bodydf = b2.b2BodyDef()
        bodydf.position = (pixelToWorld(x), pixelToWorld(y))
        bodydf.type = b2.b2_kinematicBody
        self.body:b2.b2Body = world.CreateBody(bodydf)

        boxshape = b2.b2PolygonShape(box=(self.w/2, self.h/2))
        fd = b2.b2FixtureDef()
        fd.shape=boxshape
        fd.density = 1
        fd.friction = 0.1
        self.body.CreateFixture(fd)
        
        self.body.linearVelocity = b2.b2Vec2(0, -0.6)
        pass

    def draw(self, screen):
        pos = worldToPixel(self.body.position)
        w = worldToPixel(self.w)
        h = worldToPixel(self.h)
        pygame.draw.rect(screen, "black", (pos.x-w/2, screen.get_height()-pos.y-h/2, w, h))
        pass

    def update(self):
        print("Current pos: " , self.body.linearVelocity)
        if self.body.position.y < 0:
            self.body.position.y = self.initialY
            self.body.position.x = self.initialX