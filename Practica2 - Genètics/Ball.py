import pygame
import Box2D as b2
import utils

class Ball:
    def __init__(self, world:b2.b2World, x:float, y:float, radius:float):
        self.radius = radius
        self.isRemoved = False
        self.touched_floor = False
        bodydf = b2.b2BodyDef()
        bodydf.position = utils.pixelToWorld(x, y)
        bodydf.type = b2.b2_dynamicBody
        bodydf.userData = self
        self.body:b2.b2Body = world.CreateBody(bodydf)

        circleshape = b2.b2CircleShape(radius=utils.pixelToWorld(radius))
        fd = b2.b2FixtureDef()
        fd.shape=circleshape
        fd.density = 1
        fd.restitution = 0
        fd.friction = 1
        self.body.CreateFixture(fd)
        pass
           

    def touchedFloor(self):
        self.touched_floor = True
        
    def hasTouchedFloor(self):
        return self.touched_floor

    def draw(self, screen:pygame.Surface):
        position:b2.b2Vec2 = utils.worldToPixel(self.body.position.copy())
        position.y = screen.get_height()-position.y

        pygame.draw.circle(screen, 'yellow', position, self.radius, 1)
        pass

    def destroy(self, world:b2.b2World):
        world.DestroyBody(self.body)
        self.isRemoved = True