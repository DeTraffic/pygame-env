from sys import exit
import pygame
from Intersection import Intersection
from catppuccin import Flavour

GAME_NAME = "detraffic-pygame-env"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MAX_FPS = 60

THEME = Flavour.mocha()

BG_COLOR = THEME.mauve.rgb

pygame.init()
pygame.display.set_caption(GAME_NAME)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# screen.fill(BG_COLOR)

clock = pygame.time.Clock()

intersection_group = pygame.sprite.Group()
intersection = Intersection(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
# intersection2 = Intersection(SCREEN_WIDTH / 2 + 300, SCREEN_HEIGHT / 2)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    intersection.draw(screen)
    # intersection2.draw(screen)

    # Restrict maximum fps
    clock.tick(MAX_FPS)