from torch import nn
import torch

class NeuralNetwork(nn.Module):
    def __init__(self, NC=9):
        super().__init__()
        self.linear_relu_stack = nn.Sequential(
           nn.Linear(512, 1024),
            nn.Tanh(),
            nn.Linear(1024, 512),
            nn.Tanh(),
            nn.Linear(512, 256),
            nn.Tanh(),
            nn.Linear(256, NC)
        )
    @torch.no_grad()
    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits
