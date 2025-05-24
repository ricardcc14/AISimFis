import pygame
from Box2D import *
import numpy as np
from Pipe import Pipe
import time

class Bird:
    def __init__(self, world:b2World, x, y, w):
        self.w = w
        self.x = x
        self.y = y
        self.timeAlive = time.time()
        self.alive = True

        bd = b2BodyDef()
        bd.position = (x, y)
        bd.type = b2_dynamicBody
        bd.userData = self
        self.body = world.CreateBody(bd)

        cs = b2CircleShape()
        cs.radius = w/2

        fd = b2FixtureDef()
        fd.shape=cs
        fd.density = 1
        fd.friction = 0.1
        fd.restitution = 0.5
        fd.isSensor = True
        self.body.CreateFixture(fd)
        pass

    def draw(self, screen):
        pygame.draw.circle(screen, "skyblue", (self.body.position.x, screen.get_height()-self.body.position.y), self.w/2)
        pygame.draw.circle(screen, "black", (self.body.position.x, screen.get_height()-self.body.position.y), self.w/2, 1)
        pass

    def jump(self, force):
        force = force*self.body.mass
        self.body.ApplyLinearImpulse((0, force), self.body.position, True)
        pass

    def collide(self):
        self.alive = False
        pass

    def getClosestPipe(self, pipes:list[Pipe]):
        closest:Pipe = None
        closestDistance = np.inf
        for pipe in pipes:
            distance = pipe.body.position.x - self.body.position.x
            if distance < closestDistance and distance > 0:
                closest = pipe
                closestDistance = distance
        return closest, closestDistance
        
    def resetBird(self):
        self.body.position = (self.x, self.y)
        self.body.linearVelocity.y = 0
        self.alive = True
        self.timeAlive = time.time()
        pass

    def getTimeAlive(self):
        return int(np.round(time.time()-self.timeAlive))