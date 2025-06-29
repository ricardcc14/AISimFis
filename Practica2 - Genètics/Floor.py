import pygame
import Box2D as b2
import utils

class Floor:
    def __init__(self, world:b2.b2World, x:float, y:float, w:float, h:float):
        self.w = w
        self.h = h

        center_x = x + w / 2
        center_y = y + h / 2
        bodydf = b2.b2BodyDef()
        bodydf.position = utils.pixelToWorld(center_x, center_y)
        bodydf.type = b2.b2_staticBody
        bodydf.userData = self
        self.body = world.CreateBody(bodydf)

        boxshape = b2.b2PolygonShape(box=utils.pixelToWorld(w/2, h/2))
        fd = b2.b2FixtureDef()
        fd.shape=boxshape
        fd.density = 1
        fd.friction = 0.1
        self.body.CreateFixture(fd)
        pass

    def draw(self, screen):
        pos = utils.worldToPixel(self.body.position) 
        pygame.draw.rect(screen, "red", pygame.Rect(pos.x, screen.get_height()-pos.y-self.h/2, self.w, self.h))
        
        pass
