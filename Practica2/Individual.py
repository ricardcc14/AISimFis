import pygame
import Box2D as b2
import utils
import time
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
    # First print the total length before the loop
        #print(f"Total rectangles in ADN: {len(self.adn)}")
        
        for rectangle in self.adn:
            rectangle.draw(screen)
            # Print individual rectangle info
            #print(f"Rectangle {self.adn.index(rectangle)}: ({rectangle.x}, {rectangle.y}), angle={rectangle.angle}")
            pygame.draw.circle(screen, 'red', (rectangle.x, rectangle.y), 5)  # Debugging point
        
        for ball in self.balls:
            ball.draw(screen)
        self.floor.draw(screen)

    def create_adn(self):
        initial = []
        print(f"Creating ADN with {self.nRectangles} rectangles")
        
        rect_length = 30  # Longitud total del rectangle
        rect_height = 10  # Alçada del rectangle
        half_length = rect_length / 2
        half_height = rect_height / 2

        for i in range(self.nRectangles):
            if i == 0:
                # Primer rectangle
                x = 100
                y = 200
                angle = 0  # Angle inicial horitzontal
                rect = Rectangle(self.world, x, y, angle)
                initial.append(rect)
                print(f"Rectangle base creat a ({x}, {y}), angle={angle:.2f}")
            else:
                # Rectangle anterior
                previous_rect = initial[i - 1]
                
                # Calculem els punts verds del rectangle anterior
                prev_center = utils.worldToPixel(previous_rect.body.position)
                prev_angle = previous_rect.body.angle
                
                # Punt verd dret (extrem dret de la línia central)
                prev_green_right = b2.b2Vec2(
                    prev_center.x + half_length * np.cos(prev_angle),
                    prev_center.y + half_length * np.sin(prev_angle)
                )
                
                # Angle del nou rectangle (petita variació)
                angle_variation = np.random.uniform(-np.pi/6, np.pi/6)  # ±30 graus
                angle = prev_angle + angle_variation
                
                # Calculem la posició del nou rectangle:
                # El seu punt verd esquerre ha de coincidir amb el punt verd dret anterior
                # Per tant, el centre estarà a half_length del punt de connexió
                new_center_x = prev_green_right.x + half_length * np.cos(angle)
                new_center_y = prev_green_right.y + half_length * np.sin(angle)
                
                rect = Rectangle(self.world, new_center_x, new_center_y, angle)
                initial.append(rect)
                
                print(f"Rectangle {i} creat a ({new_center_x:.1f}, {new_center_y:.1f}), "
                    f"connectat al punt ({prev_green_right.x:.1f}, {prev_green_right.y:.1f}), "
                    f"connectat al nou punt esquerre ({new_center_x - half_length * np.cos(angle):.1f}, {new_center_y - half_length * np.sin(angle):.1f}), "
                    f"angle={angle:.2f}")

        print(f"ADN complet. Rectangles totals: {len(initial)}")
        return initial
    
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
