import torch
import torch.nn as nn

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU(),
            nn.Linear(4, 2),       
            nn.Tanh()              
        )

    def forward(self, x):
        return self.model(x)       

def get_genome(model):
    return torch.cat([p.data.view(-1) for p in model.parameters()])

def set_genome(model, genome):
    pointer = 0
    for param in model.parameters():
        num_params = param.numel()
        param.data = genome[pointer:pointer+num_params].view_as(param)
        pointer += num_params

