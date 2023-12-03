
import pygame
from catppuccin import Flavour

THEME = Flavour.mocha()

class Road(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        """_summary_

        Args:
            x (_type_): _description_
            y (_type_): _description_
            width (_type_): _description_
            height (_type_): _description_
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(THEME.surface0.rgb)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        pass

    def draw(self):
        pass

    
