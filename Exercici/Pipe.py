import pygame
from Box2D import *
import numpy as np

class Pipe:
    def __init__(self, world:b2World, x, y, ry, w, h):
        self.w = w
        self.h = h
        self.x = x
        self.y = y

        bd = b2BodyDef()
        bd.position = (x, y+ry)
        bd.type = b2_kinematicBody
        bd.userData = self
        self.body = world.CreateBody(bd)
        
        self.body.linearVelocity = (-50, 0)

        ts = b2PolygonShape()
        ts.SetAsBox(w/2, h/2, (0,y), 0)
        td = b2FixtureDef()
        td.shape=ts
        td.density = 1
        td.friction = 0.1
        td.restitution = 0.5
        #td.isSensor = True
        self.body.CreateFixture(td)

        bs = b2PolygonShape()
        bs.SetAsBox(w/2, h/2, (0,-y), 0)
        bd = b2FixtureDef()
        bd.shape=bs
        bd.density = 1
        bd.friction = 0.1
        bd.restitution = 0.5
        #bd.isSensor=True
        self.body.CreateFixture(bd)
        pass

    def draw(self, screen):
        for fixture in self.body.fixtures:
            pygame.draw.polygon(screen, "black", [(self.body.position.x+x, screen.get_height()-self.body.position.y-y) for (x, y) in fixture.shape.vertices])        
        pass

    def checkpos(self, screen:pygame.Surface):
        if self.body.position.x < -self.w:
            self.body.position = (screen.get_width()+self.w, screen.get_height()/2 + np.random.uniform(-screen.get_height()/5, screen.get_height()/5))
        pass

    def resetPipe(self):
        self.body.position = (self.x, self.y)
        pass