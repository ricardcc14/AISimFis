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
        self.adn = self.create_adn()
        self.balls = []
        self.balls = self.loadBalls()
       
        self.floor = Floor(self.world, 0, 0, 640, 100)

    def draw(self, screen:pygame.Surface):
        
        for rectangle in self.adn:
            rectangle.draw(screen)
        
        for ball in self.balls:
            ball.draw(screen)
        self.floor.draw(screen)

    def create_adn(self):
        initial = []
        #print(f"Creating ADN with {self.nRectangles} rectangles")
        

        for i in range(self.nRectangles):
            if i == 0:
                
                x = 100
                y = 200
                rect = Rectangle(self.world, x, y, 0)
                
            else:
                # Rectangle anterior
                prev = initial[i - 1]
                
                distance_between_centers = np.sqrt(15**2 + 15**2 - 2 * 15 * 15 * np.cos(180 - prev.angle))
                dx = np.cos(prev.angle) * distance_between_centers
                dy = np.sin(prev.angle) * distance_between_centers
                x = prev.x + dx
                y = prev.y + dy
                rect = Rectangle(self.world, x, y, np.random.uniform(-np.pi, np.pi))
            initial.append(rect)
                
                

        #print(f"ADN complet. Rectangles totals: {len(initial)}")
        return initial
    
    def buildFromAngles(self, angles):
        initial = []
        #print(f"Creating ADN with {self.nRectangles} rectangles")
        
        for i in range(self.nRectangles):
            if i == 0:
                
                x = 100
                y = 200
                rect = Rectangle(self.world, x, y, angles[i])
                
            else:
                # Rectangle anterior
                prev = initial[i - 1]
                
                distance_between_centers = np.sqrt(15**2 + 15**2 - 2 * 15 * 15 * np.cos(180 - prev.angle))
                dx = np.cos(prev.angle) * distance_between_centers
                dy = np.sin(prev.angle) * distance_between_centers
                x = prev.x + dx
                y = prev.y + dy
                rect = Rectangle(self.world, x, y, angles[i])
            initial.append(rect)
    
    def loadBalls(self):
        #Llegir informació del JSON
        data = utils.readJson('data.json')
        #print(data)

        balls_data = data.get("balls", [])
        balls = []
        for ball in balls_data:
            new_ball = Ball(self.world, ball['position'][0], ball['position'][1],ball['radius'])
            balls.append(new_ball)

        return balls
    
    def simulate(self, screen):
        for _ in range(self.steps):
            self.world.Step(self.time_step, self.vel_iters, self.pos_iters)

        fitness = self.calculate_fitness()
        return fitness

    def calculate_fitness(self):
        for ball in self.balls:
            if ball.hasTouchedFloor():
                self.fitness += 1

        return self.fitness
    
    def getAngleFromGene(self, index):
        return self.adn[index].angle
    
    
    
    def mutateAngle(self, index):
        self.adn[index].mutateAngle()
    
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
