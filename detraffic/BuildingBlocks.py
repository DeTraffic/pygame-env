import pygame
from Enums import Direction, TrafficLightState
import catppuccin
from time import sleep

class Road(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        going_lane_count: int,
        coming_lane_count: int,
        lane_width: int,
        lane_height: int,
        direction: "Direction",
    ):
        """_summary_

        Args:
            x (int): _description_
            y (int): _description_
            going_lane_count (int): _description_
            coming_lane_count (int): _description_
            lane_width (int): _description_
            lane_height (int): _description_
            direction (Direction): _description_
        """

        pygame.sprite.Sprite.__init__(self)

        self.width = lane_height
        self.height = (going_lane_count + coming_lane_count) * lane_width

        if direction in (Direction.TOP_TO_BOTTOM, Direction.BOTTOM_TO_TOP):
            self.width, self.height = self.height, self.width

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(catppuccin.Flavour.mocha().surface0.rgb)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.going_lane_count = going_lane_count
        self.coming_lane_count = coming_lane_count
        self.lane_width = lane_width
        self.lane_height = lane_height
        self.direction = direction

        match direction:
            case Direction.LEFT_TO_RIGHT:
                pygame.draw.line(
                    self.image,
                    catppuccin.Flavour.mocha().yellow.rgb,
                    (0, self.coming_lane_count * self.lane_width),
                    (self.lane_height, self.coming_lane_count * self.lane_width),
                )
            case Direction.RIGHT_TO_LEFT:
                pygame.draw.line(
                    self.image,
                    catppuccin.Flavour.mocha().yellow.rgb,
                    (0, self.going_lane_count * self.lane_width),
                    (self.lane_height, self.going_lane_count * self.lane_width),
                )
            case Direction.TOP_TO_BOTTOM:
                pygame.draw.line(
                    self.image,
                    catppuccin.Flavour.mocha().yellow.rgb,
                    (self.going_lane_count * self.lane_width, 0),
                    (self.going_lane_count * self.lane_width, self.lane_height),
                )
            case Direction.BOTTOM_TO_TOP:
                pygame.draw.line(
                    self.image,
                    catppuccin.Flavour.mocha().yellow.rgb,
                    (self.coming_lane_count * self.lane_width, 0),
                    (self.coming_lane_count * self.lane_width, self.lane_height),
                )

    def update(self):
        pass

    def draw(self):
        pass


class TrafficLight(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        direction: "Direction",
    ):
        """_summary_

        Args:
            x (int): _description_
            y (int): _description_
            width (int): _description_
            height (int): _description_
            accerelation (float): _description_
            speed (float): _description_
            direction (Direction): _description_
        """

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(catppuccin.Flavour.mocha().red.rgb)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.width = width
        self.height = height
        self.direction = direction
        self.state = TrafficLightState.RED

    def update(self, state: "TrafficLightState"):
        match state:
            case TrafficLightState.RED:
                self.image.fill(catppuccin.Flavour.mocha().red.rgb)
            case TrafficLightState.GREEN:
                self.image.fill(catppuccin.Flavour.mocha().green.rgb)

        self.state = state
