import Box2D as b2
import pygame

class ContactListener(b2.b2ContactListener):

    def __init__(self):
        super().__init__()

    def BeginContact(self, contact:b2.b2Contact):
        fixture1:b2.b2Fixture = contact.fixtureA
        fixture2:b2.b2Fixture = contact.fixtureB

        body1:b2.b2Body = fixture1.body
        body2:b2.b2Body = fixture2.body
        
        o1 = body1.userData
        o2 = body2.userData

        #if isinstance(o2, Ball): 
            #o1, o2 = o2, o1
        
        
    def EndContact(self, contact:b2.b2Contact):
        pass
    def PreSolve(self, contact:b2.b2Contact, oldManifold:b2.b2Manifold,):
        pass
    def PostSolve(self, contact:b2.b2Contact, impulse:b2.b2ContactImpulse):
        pass