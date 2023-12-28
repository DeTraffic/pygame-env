import torch
import random
import numpy as np
from collections import deque
#from Game import Game
from IntersectionGame import IntersectionGame
from Model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 1_000_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self, epsilon=120, gamma=0.9):
        self.n_games = 0
        self.epsilon = epsilon  # randomness
        self.gamma = gamma  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(16, [128, 16], 5)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        state = game.state

        state = [
            state["left_car_count"],
            state["right_car_count"],
            state["top_car_count"],
            state["bottom_car_count"],
            state["left_waiting"],
            state["right_waiting"],
            state["top_waiting"],
            state["bottom_waiting"],
            state["left_decay"],
            state["right_decay"],
            state["top_decay"],
            state["bottom_decay"],
            state["left_center"],
            state["right_center"],
            state["top_center"],
            state["bottom_center"],
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append(
            (state, action, reward, next_state, game_over)
        )  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)
        # for state, action, reward, nexrt_state, game_over in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, game_over)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        final_move = [0, 0, 0, 0, 0]
        if random.randint(1, 200) <= self.epsilon:
            move = random.randint(0, len(final_move) - 1)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        print(final_move)

        return final_move


def train(
    lane_width,
    lane_height,
    left_to_right_lane_count: int = 1,
    right_to_left_lane_count: int = 1,
    top_to_bottom_lane_count: int = 1,
    bottom_to_top_lane_count: int = 1,
    left_to_right_car_spawn_probability: float = 0.6,
    right_to_left_car_spawn_probability: float = 0.6,
    top_to_bottom_car_spawn_probability: float = 0.6,
    bottom_to_top_car_spawn_probability: float = 0.6,
    left_to_right_special_car_spawn_probability: float = 0.05,
    right_to_left_special_car_spawn_probability: float = 0.05,
    top_to_bottom_special_car_spawn_probability: float = 0.05,
    bottom_to_top_special_car_spawn_probability: float = 0.05,
):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = IntersectionGame(
        "detraffic-pygame-env",
        900,
        700,
        144,
        int(lane_width),
        int(lane_height),
        int(left_to_right_lane_count),
        int(right_to_left_lane_count),
        int(top_to_bottom_lane_count),
        int(bottom_to_top_lane_count),
        left_to_right_car_spawn_probability,
        right_to_left_car_spawn_probability,
        top_to_bottom_car_spawn_probability,
        bottom_to_top_car_spawn_probability,
        left_to_right_special_car_spawn_probability,
        right_to_left_special_car_spawn_probability,
        top_to_bottom_special_car_spawn_probability,
        bottom_to_top_special_car_spawn_probability
    )
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, score, game_over = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over or game.frame_iteration > 3600:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.epsilon = max(0, agent.epsilon - 1)
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print("Game", agent.n_games, "Score", score, "Record:", record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == "__main__":
    train()
