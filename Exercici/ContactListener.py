from Box2D import *
from Bird import Bird
from Pipe import Pipe
from Surface import Surface

class ContactListener(b2ContactListener):
    def BeginContact(self, contact:b2Contact):
        f1:b2Fixture = contact.fixtureA
        f2:b2Fixture = contact.fixtureB

        b1:b2Body = f1.body
        b2:b2Body = f2.body
        
        o1 = b1.userData
        o2 = b2.userData

        if type(o1) != Bird:
            o_aux = o1
            o1 = o2
            o2 = o_aux

        if(type(o1) == Bird and type(o2) == Pipe):
            if(o1.alive): o1.collide()
        if(type(o1) == Bird and type(o2) == Surface):
            if(o1.alive): o1.collide()
        pass
    def EndContact(self, contact:b2Contact):
        pass

    def PreSolve(self, contact:b2Contact, oldManifold:b2Manifold,):
        pass
    def PostSolve(self, contact:b2Contact, impulse:b2ContactImpulse):
        pass