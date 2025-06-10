import pygame
import Box2D as b2
import numpy as np
from utils import pixelToWorld, worldToPixel, drawRotatedImage

class Ball:
    def __init__(self, world, x, y, radius):
        self.radius = pixelToWorld(radius)

        bodydf = b2.b2BodyDef()
        bodydf.position = (pixelToWorld(x), pixelToWorld(y))
        bodydf.type = b2.b2_dynamicBody
        self.body:b2.b2Body = world.CreateBody(bodydf)
        self.body.angularDamping = 20

        circleshape = b2.b2CircleShape()
        circleshape.radius = self.radius
        fd: b2.b2FixtureDef = b2.b2FixtureDef()
        fd.shape=circleshape
        fd.density = 1
        fd.friction = 1
        fd.restitution = 0.1
        self.body.CreateFixture(fd)
        self.sprite = pygame.image.load("doodle.png")
        pass

    def draw(self, screen):
        position:b2.b2Vec2 = worldToPixel(self.body.position.copy())
        position.y = screen.get_height()-position.y

        r = worldToPixel(self.radius)

        drawRotatedImage(screen, pygame.transform.scale(self.sprite, (r*2, r*2)), position, r*2, r*2, self.body.angle)
        pass


    def destroyBody(self, world):
        world.DestroyBody(self.body)
        pass

    def jump(self, screen:pygame.Surface, direction, mult):
        #pointer = np.array([pointer[0], screen.get_height() - pointer[1]])

        #direction = pointer - np.array(worldToPixel(self.body.position))
        direction = direction/np.linalg.norm(direction)

        self.body.ApplyLinearImpulse(direction*mult, self.body.position, True)
        pass