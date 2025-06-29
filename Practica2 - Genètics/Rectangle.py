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
        self.line_color = "red"  # Color de la línia divisòria
        self.circle_color = "green"

        boxshape = b2.b2PolygonShape(box=utils.pixelToWorld(self.w/2, self.h/2))
        fd = b2.b2FixtureDef()
        fd.shape=boxshape
        fd.density = 1
        fd.restitution = 0
        fd.friction = 1
        self.body.CreateFixture(fd)
        pass

    def draw(self, screen: pygame.Surface):
        angle = self.body.angle
        center_world = self.body.position  # En metres

        # Mides del rectangle en metres
        hw = self.w / 200  # half-width in meters (30px / 2 / 100)
        hh = self.h / 200  # half-height in meters

        # Corners en coordenades locals (en metres)
        local_corners = [
            (-hw, -hh),
            ( hw, -hh),
            ( hw,  hh),
            (-hw,  hh)
        ]

        # Rotar i transformar a coordenades globals
        world_corners = []
        for lx, ly in local_corners:
            rx = lx * np.cos(angle) - ly * np.sin(angle)
            ry = lx * np.sin(angle) + ly * np.cos(angle)
            wx = center_world.x + rx
            wy = center_world.y + ry
            world_corners.append(b2.b2Vec2(wx, wy))

        # Convertir a píxels per dibuixar amb pygame
        pixel_corners = [utils.worldToPixel(corner) for corner in world_corners]
        pygame.draw.polygon(screen, self.color, [(p.x, p.y) for p in pixel_corners])

        # Dibuixa els punts verds als extrems
        left_world = b2.b2Vec2(
            center_world.x + (-hw) * np.cos(angle),
            center_world.y + (-hw) * np.sin(angle)
        )
        right_world = b2.b2Vec2(
            center_world.x + (hw) * np.cos(angle),
            center_world.y + (hw) * np.sin(angle)
        )

        pygame.draw.circle(screen, "green", utils.worldToPixel(left_world), 3)
        pygame.draw.circle(screen, "green", utils.worldToPixel(right_world), 3)

        

        
        

    #def update(self, world):
    def mutateAngle(self):
        self.angle = np.random.uniform(-np.pi, np.pi)
    def mutateYPos(self):
        self.y = np.random.randint(100, 250)
        self.body.position.y = utils.pixelToWorld(self.y)
    def mutateXPos(self):
        self.x = np.random.randint(30, 610)
        self.body.position.x = utils.pixelToWorld(self.x)

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
    

        
    
