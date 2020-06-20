import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import numpy as np

import random as rand
from game import Board

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")



class Env(Board):
    
    def __init__(self):
        super(Env, self).__init__()
        
        self.board = self.legal_board(self.rand_tensor)
        self.board = self.board.float().to(device)
        self.score = 0
        self.moves = 10
        
    def unravel_index(self, index, shape):
        out = []
        for dim in reversed(shape):
            out.append(index % dim)
            index = index // dim
        return tuple(reversed(out))
      
    def get_move(self, tensor):
        index = tensor.argmax()
        shape = tuple(tensor.shape)
        out = self.unravel_index(index, shape)
        return(out)
    
    def ಠ_ಠ(self):
        self.score -=5
    
    def move(self, m,i,j):
        
        if m == 0: #left
           if self.legal_move(self.board, i, j, i, j-1):
               self.move_left(self.board, i, j)
               self.legal_board(self.board)
           else:
               self.ಠ_ಠ()
               
        if m == 1: #right
           if self.legal_move(self.board, i, j, i, j+1):
               self.move_right(self.board, i, j)
               self.legal_board(self.board)
           else:
               self.ಠ_ಠ()
               
        if m == 2: #up
           if self.legal_move(self.board, i, j, i-1, j):
               self.move_up(self.board, i, j)
               self.legal_board(self.board)
           else:
               self.ಠ_ಠ()
               
        if m == 3: #down
           if self.legal_move(self.board, i, j, i+1, j):
               self.move_down(self.board, i, j)
               self.legal_board(self.board)
           else:
               self.ಠ_ಠ()

env = Env()




class Q_Net(nn.Module): 
    
    def __init__(self):
        super(Q_Net, self).__init__()
        
        self.fc1 = nn.Linear(80, 320)
        nn.init.xavier_uniform_(self.fc1.weight)
        
        self.fc2 = nn.Linear(320, 640)
        nn.init.xavier_uniform_(self.fc2.weight)
        
        self.fc3 = nn.Linear(640, 640)
        nn.init.xavier_uniform_(self.fc3.weight)
        
        self.fc4 = nn.Linear(640,320)
        nn.init.xavier_uniform_(self.fc4.weight)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        
        return(x.view(4, 10, 8))
        



        
model = Q_Net()
model.cuda()
print(env.board, "\n")
move = env.get_move(model(env.board.view(-1, env.board_size)))
env.move(move[0], move[1], move[2])
print(env.score)
print(env.board)



criterion = torch.nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)




