import pygame
import pygame.freetype
from Box2D import *
from ContactListener import ContactListener
import numpy as np
from Bird import Bird
from Pipe import Pipe
from Surface import Surface

import pandas as pd
import matplotlib.pyplot as plt
import torch as torch
from torch.utils.data import TensorDataset, random_split, DataLoader
import torch.nn as nn
import torch.optim as optim
import seaborn as sns
from sklearn.metrics import confusion_matrix 

# Xarxa neuronal & Genetics

data = pd.read_csv("dataset_sallebird.csv")
#print(data.head())

X = data.drop(columns=["action"]).values
y = data["action"]

X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32)

dataset = TensorDataset(X, y)

train, test = random_split(dataset, [0.8, 0.2])
train = DataLoader(train, batch_size=32, shuffle=True)
test = DataLoader(test, batch_size=32, shuffle=False)

class MLP(nn.Module):
    def __init__(self, *args, **kwargs):
        super(MLP, self).__init__(*args, **kwargs)

        self.model = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU(),
            nn.Linear(4, 1),
            nn.Sigmoid()
        )

    #El que executa quan es crida aquest model
    def forward(self, x):
        return self.model(x)
    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

model = MLP().to(device)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


epochs = 25
model.train()
loss_all = []

for i in range(epochs):

    loss_value = 0

    for batch, labels in train:
        batch = batch.to(device)
        labels = labels.view(-1, 1).to(device)

        optimizer.zero_grad()
        pred = model(batch)

        loss = criterion(pred, labels)
        loss.backward()

        optimizer.step()

        loss_value += loss.item()

    print(f'Epoch {i+1} of {epochs}' )    
    loss_all.append(loss_value)

plt.figure()
plt.plot(loss_all)
plt.show()

all_pred = []
all_labels = []

model.eval()

with torch.no_grad():
    for batch, labels in train:
        batch = batch.to(device)
        labels = labels.view(-1, 1).to(device)

        pred = model(batch)

        pred = (pred >= 0.5)

        all_pred.extend(pred.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

correct_pred = np.sum(np.array(all_pred).flatten() == np.array(all_labels))
accuracy = correct_pred / len(all_labels)

plt.figure()
plt.title(f'Accuracy: {accuracy}')
sns.heatmap(confusion_matrix(all_labels, all_pred))
plt.show()


# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
font = pygame.freetype.SysFont("Consolas", 24)
running = True
frames = 120
frame = 0

# Box2D
world = b2World()
timeStep = 1.0/frames
vel_iters, pos_iters = 8, 3
world.gravity = b2Vec2(0, -200)
contactListener = ContactListener()
world.contactListener = contactListener

# Inicialització del joc
bird = Bird(world, 50, screen.get_height()/2, 40)

pipes = []

pipes.append(Pipe(world, 2*screen.get_width()/3, screen.get_height()/2, np.random.uniform(-screen.get_height()/4, screen.get_height()/4), 50, screen.get_height()/2))
pipes.append(Pipe(world, screen.get_width()+25, screen.get_height()/2, np.random.uniform(-screen.get_height()/4, screen.get_height()/4), 50, screen.get_height()/2))
pipes.append(Pipe(world, 4*screen.get_width()/3+50, screen.get_height()/2, np.random.uniform(-screen.get_height()/4, screen.get_height()/4), 50, screen.get_height()/2))

surface = Surface(world, screen.get_width()/2, 0, screen.get_width(), 20)
surface_top = Surface(world, screen.get_width()/2, screen.get_height(), screen.get_width(), 20)

def observe(bird, pipes):
    i1 = bird.body.position.y
    i2 = bird.body.linearVelocity.y
    p, d = bird.getClosestPipe(pipes)
    i3 = d+p.w
    i4 = p.body.position.y
    return np.array([i1, i2, i3, i4])

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        match(event.type):
            case pygame.QUIT:
                running = False
            case pygame.MOUSEBUTTONDOWN:
                bird.jump(250)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray55")

    # RENDER YOUR GAME HERE
    world.Step(timeStep, vel_iters, pos_iters)

    bird.draw(screen)

    for pipe in pipes:
        pipe.draw(screen)
        pipe.checkpos(screen)

    surface.draw(screen)
    surface_top.draw(screen)

    font.render_to(screen, (10, 10), "Time alive: "+str(bird.getTimeAlive())+" seconds", "thistle1")

    if not bird.alive:
        bird.resetBird()
        for pipe in pipes:
            pipe.resetPipe()

    if frame == 0:
        observation = observe(bird, pipes)
        observation = torch.tensor(observation, dtype=torch.float32).unsqueeze(0).to(device)

        with torch.no_grad():
            action = model(observation).cpu().numpy()
            action = (action > 0.5)
            
        if action == 1:
            bird.jump(250)

    frame = (frame+1)%60

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(frames)  # limits FPS to 60
pygame.quit()