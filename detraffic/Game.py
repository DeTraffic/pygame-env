import pygame
from sys import exit
import random
from BuildingBlocks import Intersection

import catppuccin


class Game:
    def __init__(
        self,
        GAME_NAME,
        GAME_WIDTH,
        GAME_HEIGHT,
        MAX_FPS,
        BG_COLOR: tuple = catppuccin.Flavour.mocha().mauve.rgb,
    ):
        self.GAME_WIDTH = GAME_WIDTH
        self.GAME_HEIGHT = GAME_HEIGHT
        self.MAX_FPS = MAX_FPS
        self.BG_COLOR = BG_COLOR

        pygame.init()
        pygame.display.set_caption(GAME_NAME)

        self.screen = pygame.display.set_mode((self.GAME_WIDTH, self.GAME_HEIGHT))
        self.clock = pygame.time.Clock()

        self.iteration = 0
        self.reset()

    def run(self):
        while True:
            reward, score, game_over = self.play_step(action)

            if game_over:
                break
        
        print(f"Final score: {score}")
        
    def play_step(self, action):

        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        reward, score, game_over = self.intersection.update(action)
        self.intersection.draw(self.screen)
        pygame.display.flip()

        self.clock.tick(self.MAX_FPS)
        
        return reward, score, game_over

    def reset(self):

        self.intersection = Intersection(
            x=self.GAME_WIDTH / 2,
            y=self.GAME_HEIGHT / 2,
            lane_width=30,
            lane_height=200,
            left_to_right_lane_count=2,
            right_to_left_lane_count=1,
            top_to_bottom_lane_count=1,
            bottom_to_top_lane_count=1,
        )

        background = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))
        background.fill(self.BG_COLOR)
        self.screen.blit(background, (0, 0))

        self.iteration += 1
        self.frame_iteration = 0

    def reward(self):
        pass