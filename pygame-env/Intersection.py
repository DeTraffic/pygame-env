
import pygame
from Road import Road
from catppuccin import Flavour

THEME = Flavour.mocha()

class Intersection(pygame.sprite.Sprite):

    width = 600
    height = 600

    def __init__(self, x, y):
        """_summary_

        Args:
            x (_type_): _description_
            y (_type_): _description_
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(THEME.mauve.rgb)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self._init_intersection()


    def update(self):
        pass

    def draw(self, surface):
        """_summary_

        Args:
            surface (_type_): _description_
        """
        self.roads_group.draw(self.image)
        surface.blit(self.image, self.rect)

    def _init_intersection(self):
        """_summary_
        """

        road_long = 100
        road_short = 50

        self.roads_group = pygame.sprite.Group()

        left_road = Road(0, self.height / 2, 500, 100)
        right_road = Road(self.width, self.height / 2, 500, 100)
        top_road = Road(self.width / 2, 0, 100, 500)
        bot_road = Road(self.width / 2, self.height, 100, 500)
        center_road = Road(self.width / 2, self.height / 2, 100, 100)

        self.roads_group.add(left_road)
        self.roads_group.add(right_road)
        self.roads_group.add(top_road)
        self.roads_group.add(bot_road)
        self.roads_group.add(center_road)

        self.traffic_lights_group = pygame.sprite.Group()

        left_light = pygame.Surface((5, 50))
        left_light.fill(THEME.red.rgb)
        center_road.image.blit(left_light, (0, 50))

        top_light = pygame.Surface((50, 5))
        top_light.fill(THEME.red.rgb)
        center_road.image.blit(top_light, (0, 0))

        right_light = pygame.Surface((5, 50))
        right_light.fill(THEME.red.rgb)
        center_road.image.blit(right_light, (100-5, 0))

        bot_light = pygame.Surface((50, 5))
        bot_light.fill(THEME.red.rgb)
        center_road.image.blit(bot_light, (100 - 50, 100 - 5))