from Ball import Ball
from Surface import Surface
import Box2D as b2
import pygame
from utils import pixelToWorld, worldToPixel
from Model import Model
from Observe import observe


class GameManager:
    def __init__(self, frames, screen):
        # Box2D
        self.screen = screen
        self.world = b2.b2World()
        self.time_step = 1/frames
        self.vel_iters, self.pos_iters = 8, 3
        self.Model = Model()

        self.platforms = self.createPlatforms()
        spawnDoodle = self.platforms[0].getDoodleSpawnPoint()

        self.ball = Ball(self.world, spawnDoodle.x, spawnDoodle.y + 15, 25)
        #self.surface = Surface(self.world, self.screen.get_width()/2, 0, self.screen.get_width(), 20)

    def createPlatforms(self):
        platforms = []
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        num_platforms = 4
        vertical_spacing = screen_h / 2

        for i in range(num_platforms):
            
            if i % 2 == 0:
                x = screen_w * 0.25
            else:
                x = screen_w * 0.75

            y = i * vertical_spacing

            platform = Surface(self.world, x, y + 30, 200, 20)
            platforms.append(platform)
        return platforms

    def renderGame(self):
        self.screen.fill("gray")
        self.world.Step(self.time_step, self.vel_iters, self.pos_iters)
        self.updatePlatforms()
        self.ball.draw(self.screen)
        self.drawPlatformsInScreen()

    def makeBallJump(self, direction):
        self.ball.jump(self.screen, direction, 1.5)

    def updatePlatforms(self):
        
        for platform in self.platforms:
            print("Platform Y:", platform.body.position.y)

            if platform.body.position.y < 0:
                platform.respawn(self.getRespawnPosition())

    def getRespawnPosition(self):
        highest_y = float('-inf')

        for platform in self.platforms:
            if platform.body.position.y > highest_y:
                highest_y = platform.body.position.y

        offset = pixelToWorld(self.screen.get_height() / 2)

        return highest_y + offset

    def drawPlatformsInScreen(self):
        for platform in self.platforms:
            platform.draw(self.screen)


    def geneticSimulation(self, iterations=300):
        for i in range(iterations):

            #Quan ha passat 3 segons, que faci observació
            if i % 3*60 == 0:
                observation = observe(self.ball, self.platforms, self.screen.get_height())
                #observation = torch.tensor(observation, dtype=torch.float32).unsqueeze(0).to(device)
                
                #Definir direcció depenent de la observació

                #with torch.no_grad():
                    #direction = model(observation).cpu().numpy()

                    #self.ball.jump(screen, direction)


            self.world.Step(self.time_step, self.vel_iters, self.pos_iters)












