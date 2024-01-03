"""
FILL ME
"""

import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size: list, output_size):
        super().__init__()
        self.layers = []

        self.layers.append(nn.Linear(input_size, hidden_size[0]))

        for i in range(len(hidden_size) - 1):
            self.layers.append(nn.Linear(hidden_size[i], hidden_size[i + 1]))

        self.layers.append(nn.Linear(hidden_size[-1], output_size))

        self.layers = nn.ModuleList(self.layers)

    def forward(self, x):
        for layer in self.layers[:-1]:
            x = F.relu(layer(x))
        x = F.softmax(self.layers[-1](x))
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, models : list, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.models = models
        self.optimizer = optim.Adam(models[0].parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        targets= []
        preds = []
        for idx in range(len(done)):
        # 1: predicted Q values with current state
            pred0 = self.models[0](state)
            pred1 = self.models[1](state)
            pred2 = self.models[2](state)
            pred3 = self.models[3](state)

            pred = torch.tensor([torch.argmax(pred0),torch.argmax(pred1),
                                torch.argmax(pred2),torch.argmax(pred3)], dtype=torch.float32, requires_grad=True)
            preds.append(torch.argmax(pred))
            target = pred.clone()
            Q_new = reward[idx]
            if not done[idx]:
                for md in range(4):
                    Q_new = reward[idx] + (self.gamma * torch.max(self.models[md](next_state[idx])) )
                    
                    target[md] = Q_new #torch.argmax(action[idx]).item()
            else:
                target[torch.argmax(action[idx]).item()] = Q_new

            targets.append(torch.argmax(target))
    
        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(torch.tensor(targets, dtype=torch.float32, requires_grad=True), 
                              torch.tensor(preds, dtype=torch.float32, requires_grad=True))
        #loss.requires_grad = True
        loss.backward()

        self.optimizer.step()