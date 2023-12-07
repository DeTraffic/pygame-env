import pygame
from Enums import VehicleAction, Direction

import catppuccin

class Car(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        accerelation: float,
        speed: float,
        direction: "Direction",
        reward: int,
        color: tuple = catppuccin.Flavour.mocha().green.rgb,
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
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.width = width
        self.height = height
        self.accerelation = accerelation
        self.speed = speed
        self.direction = direction

        self.reward = reward
        self.action = VehicleAction.MOVE

    def update(self, action: "VehicleAction"):

        if action == VehicleAction.STOP:
            return

        match self.direction:
            case Direction.LEFT_TO_RIGHT:
                self.rect.x += self.speed
            case Direction.RIGHT_TO_LEFT:
                self.rect.x -= self.speed
            case Direction.TOP_TO_BOTTOM:
                self.rect.y += self.speed
            case Direction.BOTTOM_TO_TOP:
                self.rect.y -= self.speed
