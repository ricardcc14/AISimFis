import pygame
import Box2D as b2
import utils
import time
import numpy as np

class Rectangle:
    def __init__(self, world:b2.b2World, x:float, y:float, angle:float):
        self.w = 30
        self.h = 10

        self.x = x
        self.y = y

        self.angle = angle

        self.world = world
        self.timer = 0
        bodydf = b2.b2BodyDef()
        bodydf.position = utils.pixelToWorld(x, y)
        bodydf.angle = self.angle  
        bodydf.type = b2.b2_staticBody
        bodydf.userData = self
        self.body:b2.b2Body = world.CreateBody(bodydf)
        self.color = "blue"

        boxshape = b2.b2PolygonShape(box=utils.pixelToWorld(self.w/2, self.h/2))
        fd = b2.b2FixtureDef()
        fd.shape=boxshape
        fd.density = 1
        fd.restitution = 0
        fd.friction = 1
        self.body.CreateFixture(fd)
        pass

    def draw(self, screen:pygame.Surface):
        angle = self.body.angle
        center = utils.worldToPixel(self.body.position.copy())
        center.y = screen.get_height() - center.y  

        hw, hh = self.w / 2, self.h / 2

        corners = [
            b2.b2Vec2(-hw, -hh),
            b2.b2Vec2(hw, -hh),
            b2.b2Vec2(hw, hh),
            b2.b2Vec2(-hw, hh)
        ]

        points = []
        
        for corner in corners:
            rotated_x, rotated_y = utils.rotate_point(corner, angle)
            rotated = b2.b2Vec2(rotated_x, rotated_y)
            final = center + rotated
            points.append((final.x, final.y))

        pygame.draw.polygon(screen, self.color, points)



        
        

    #def update(self, world):
    def mutateAngle(self):
        self.angle = np.random.uniform(-np.pi, np.pi)

    def destroy(self, world:b2.b2World):
        if self.body:
            world.DestroyBody(self.body)
            self.body = None 
        

    def setLinearVelocity(self, x:float, y:float, scale:float=5):
        self.body.linearVelocity = scale*utils.pixelToWorld(x, y)

    def setAngularVelocity(self, a:float):
        self.body.angularVelocity = a

    def boxCollided(self):
        if(not self.collided):
            self.collided = True
            self.prevSec = time.time()
        pass

    def getLinearVelocity(self):
        return self.body.linearVelocity
    

        
    
