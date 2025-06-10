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

    def draw(self, screen:pygame.Surface):
        angle = self.body.angle
        center_pixel = utils.worldToPixel(self.body.position.copy())
        hw, hh = self.w / 2, self.h / 2  # Half width and height in pixels

        # Rectangle corners in local coordinates (before rotation)
        local_corners = [
            (-hw, -hh),  # Top-left
            (hw, -hh),   # Top-right
            (hw, hh),    # Bottom-right
            (-hw, hh)    # Bottom-left
        ]

        points = []
        for corner in local_corners:
            # Rotate each corner point
            rotated_x, rotated_y = utils.rotate_point(corner, angle)
            
            # Convert to screen coordinates
            screen_x = center_pixel.x + rotated_x
            screen_y = center_pixel.y + rotated_y
            points.append((screen_x, screen_y))

        # Draw the rectangle
        pygame.draw.polygon(screen, self.color, points)

        left_point = b2.b2Vec2(-hw, 0)
        right_point = b2.b2Vec2(hw, 0)
        
        # Rotate points
        rotated_left = utils.rotate_point(left_point, angle)
        rotated_right = utils.rotate_point(right_point, angle)
        
        # Convert to b2Vec2 if needed
        if isinstance(rotated_left, tuple):
            rotated_left = b2.b2Vec2(rotated_left[0], rotated_left[1])
        if isinstance(rotated_right, tuple):
            rotated_right = b2.b2Vec2(rotated_right[0], rotated_right[1])
        
        # Calculate final positions
        # line_start = center + rotated_left
        # line_end = center + rotated_right
        
        # # Draw line
        # pygame.draw.line(screen, self.line_color, 
        #             (line_start.x, line_start.y), 
        #             (line_end.x, line_end.y), 2)
        
        # # Draw endpoint circles
        # pygame.draw.circle(screen, self.circle_color,
        #                 (int(line_start.x), int(line_start.y)), 5)
        # pygame.draw.circle(screen, self.circle_color,
        #                 (int(line_end.x), int(line_end.y)), 5)

        
        

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
    

        
    
