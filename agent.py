# Libraries
import pygame
import random
import numpy as np
from snake_game import SnakeGameAI 
import torch.nn as nn
import torch 
import torch.optim as optim

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.linear1(x))
        x = self.linear2(x)
        return x

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        # Convert data to tensors and ensure correct dimensions [Batch_Size, Features]
        state = torch.tensor(np.array(state), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(np.array(action), dtype=torch.long)
        reward = torch.tensor(np.array(reward), dtype=torch.float)
        
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1. Predicted Q-values with the current state
        pred = self.model(state)

        # 2. Calculate target Q-values using the Bellman Equation
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                # Correct dimension handling for PyTorch max prediction
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            # Locate the exact action index and update its Q-value
            action_idx = torch.argmax(action[idx]).item()
            target[idx][action_idx] = Q_new
            
        # 3. Reset gradients, backpropagate loss, and update weights
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()        

class Agent:
    def __init__(self):
        self.game = SnakeGameAI()
        self.n_games = 0
        self.epsilon = 100  # Start at 100 to maximize initial exploration
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=0.001, gamma=0.9)

    def get_state(self, game):
        aplle_right = aplle_left = aplle_up = aplle_down = False
        if game.x < game.aplle_x: aplle_right = True
        if game.x > game.aplle_x: aplle_left = True
        if game.y > game.aplle_y: aplle_up = True
        if game.y < game.aplle_y: aplle_down = True

        move_straight = game.dx == game.speed and game.dy == 0 
        move_back = game.dx == -game.speed and game.dy == 0   
        move_right = game.dy == game.speed and game.dx == 0   
        move_left = game.dy == -game.speed and game.dx == 0   
        
        head_x = game.snake_body[0][0]
        head_y = game.snake_body[0][1]

        point_straight = [head_x + game.dx, head_y + game.dy]
        
        if move_straight: 
            point_right = [head_x, head_y + game.speed] 
            point_left = [head_x, head_y - game.speed]  
        elif move_back: 
            point_right = [head_x, head_y - game.speed] 
            point_left = [head_x, head_y + game.speed]  
        elif move_right: 
            point_right = [head_x - game.speed, head_y] 
            point_left = [head_x + game.speed, head_y]  
        else: 
            point_right = [head_x + game.speed, head_y] 
            point_left = [head_x - game.speed, head_y]  

        danger_straight = (point_straight in game.snake_body or point_straight[0] > 977 or point_straight[0] < 1 or point_straight[1] > 480 or point_straight[1] < 1)
        danger_right = (point_right in game.snake_body or point_right[0] > 977 or point_right[0] < 1 or point_right[1] > 480 or point_right[1] < 1)
        danger_left = (point_left in game.snake_body or point_left[0] > 977 or point_left[0] < 1 or point_left[1] > 480 or point_left[1] < 1)

        state = [
            danger_straight, danger_right, danger_left,
            move_straight, move_right, move_left, move_back,
            aplle_left, aplle_right, aplle_up, aplle_down
        ]
        return np.array(state, dtype=int)

    def get_action(self, state):
        state_tensor = torch.tensor(state, dtype=torch.float)
        finall_move = [0, 0, 0]
        if random.randint(0, 100) < self.epsilon:
            move = random.randint(0, 2)
        else:
            prediction = self.model(state_tensor)
            move = torch.argmax(prediction).item()
        finall_move[move] = 1    
        return finall_move 

def train():
    game = SnakeGameAI()
    agent = Agent()
    
    while True:
        state_old = agent.get_state(game)
        finall_move = agent.get_action(state_old)
        
        # Calculate Euclidean distance to dynamically shape rewards
        dist_old = np.sqrt((game.x - game.aplle_x)**2 + (game.y - game.aplle_y)**2)
        
        done, score, reward = game.play_step(finall_move)
        
        dist_new = np.sqrt((game.x - game.aplle_x)**2 + (game.y - game.aplle_y)**2)
        
        # Reward shaping based on approaching or moving away from food
        if not done:
            if dist_new < dist_old:
                reward += 1.0
            else:
                reward -= 1.5
        
        state_new = agent.get_state(game)
        
        agent.trainer.train_step(state_old, finall_move, reward, state_new, done)
        
        if done == True:
            # Reset game immediately without delay to maintain data flow
            game.reset()
            agent.n_games += 1
            if agent.epsilon > 0:
                agent.epsilon -= 1
                
            # Log training progress to monitor epsilon decay and performance
            print(f"Game: {agent.n_games}, Score: {score}, Epsilon: {agent.epsilon}")

if __name__ == "__main__":
    train()

        




