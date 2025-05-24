
import utils
import pygame
import numpy
import Box2D as b2
from ContactListener import ContactListener
from Floor import Floor
from Ball import Ball

class EvolutionManager:
    def __init__ (self, screen, data_route):
        self.data_route = data_route
        self.screen = screen

        self.frames = 60
        # Box2D
        self.world = b2.b2World()
        self.time_step = 1/self.frames
        self.vel_iters, self.pos_iters = 8, 3
        contactListener = ContactListener()
        self.world.contactListener = contactListener

        self.floor = Floor(self.world, 0, 0, self.screen.get_width(), 100)

        self.balls = []


    #Funció que inicialitza un nivell extraient la informació del JSON

    def loadElements(self):
        #Llegir informació del JSON
        data = utils.readJson(self.data_route)
        print(data)

        balls_data = data.get("balls", [])

        for ball in balls_data:
            new_ball = Ball(self.world, ball['position'][0], ball['position'][1],ball['radius'])
            self.balls.append(new_ball)

        return True
                    
                    
    def runLevel(self):
        # RENDER YOUR GAME HERE
        self.world.Step(self.time_step, self.vel_iters, self.pos_iters)
        
    
    def draw(self):
        
        self.floor.draw(self.screen)

        for i, ball in enumerate(self.balls):
            if(ball.isRemoved):
                self.balls.pop(i)
            else:
                ball.update(self.world)
                ball.draw(self.screen)


        