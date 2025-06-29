import pygame
import Box2D as b2
import utils
import numpy as np
from Ball import Ball
from Floor import Floor
from Rectangle import Rectangle
from ContactListener import ContactListener

class Individual:
    def __init__(self, world:b2.b2World):
        self.world = world
        contactListener = ContactListener()
        self.world.contactListener = contactListener
    
        self.time_step = 1/60
        self.vel_iters = 8
        self.pos_iters = 3
        self.steps = 300
        self.body = None
        self.nRectangles = 20
        self.fitness = 0
        self.adn = []
        self.balls = []
        self.balls = self.loadBalls()
       
        self.floor = Floor(self.world, 0, 0, 640, 100)

    def draw(self, screen:pygame.Surface):
    
        for rectangle in self.adn:
            rectangle.draw(screen)
        
        for ball in self.balls:
            
            ball.draw(screen)
        self.floor.draw(screen)

    def buildFromAngles(self, angles):
       
        self.adn = []

        for i in range(len(angles)):
            if i == 0:
                x, y = 100, 200
                rect = Rectangle(self.world, x, y, angles[i])
            else:
                prev = self.adn[-1]
                distance_between_centers = np.sqrt(15**2+15**2 - 2*15*15*np.cos(180 - angles[i]))
                dx = np.cos(prev.angle) * distance_between_centers
                dy = np.sin(prev.angle) * distance_between_centers
                x = prev.x + dx
                y = prev.y + dy
                rect = Rectangle(self.world, x, y, angles[i])
            self.adn.append(rect)

    def getAngles(self):
        return [rect.angle for rect in self.adn]       

    
    def loadBalls(self):
      
        data = utils.readJson('data.json') 
        balls_data = data.get("balls", [])
        balls = []
        for ball in balls_data:
            new_ball = Ball(self.world, ball['position'][0], ball['position'][1],ball['radius'])
            balls.append(new_ball)

        return balls
    
    def simulate(self):
        for step in range(self.steps):
            self.world.Step(self.time_step, self.vel_iters, self.pos_iters)

        fitness = self.calculate_fitness()
        return fitness

    def calculate_fitness(self):
        for ball in self.balls:      
            if ball.hasTouchedFloor():
                self.fitness += 1

        return self.fitness
    
    
    def destroy(self):
        for ball in self.balls:
            ball.destroy(self.world)
        self.balls.clear()

        if self.body:
            self.world.DestroyBody(self.body)
            self.body = None
            
        for i in range(len(self.adn)):
            self.adn[i].destroy(self.world)

        if self.floor and self.floor.body:
            self.world.DestroyBody(self.floor.body)
            self.floor.body = None

        self.adn.clear()
        self.fitness = 0.0
