
import pygame

class Car(pygame.sprite.Sprite):

    def __init__(self, width, height, x, y):
        """_summary_

        Args:
            width (_type_): _description_
            height (_type_): _description_
            x (_type_): _description_
            y (_type_): _description_
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/car.png')
        self.rect = self.image.get_rect()

    # Functions below are just examples from the internet. They do not work.

    def update(self):
        """_summary_
        """
        newpos = self.calcnewpos(self.rect,self.vector)
        self.rect = newpos

    def calcnewpos(self, rect, vector):
        """_summary_

        Args:
            rect (_type_): _description_
            vector (_type_): _description_

        Returns:
            _type_: _description_
        """
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return rect.move(dx,dy)

class PoliceCar(Car):

    def __init__(self, width, height, x, y):
        """_summary_

        Args:
            width (_type_): _description_
            height (_type_): _description_
            x (_type_): _description_
            y (_type_): _description_
        """
        pygame.sprite.Sprite.__init__(self, width, height, x, y)
        self.image = pygame.image.load('assets/police-car.png')

class Ambulance(Car):

    def __init__(self, width, height, x, y):
        """_summary_

        Args:
            width (_type_): _description_
            height (_type_): _description_
            x (_type_): _description_
            y (_type_): _description_
        """
        pygame.sprite.Sprite.__init__(self, width, height, x, y)
        self.image = pygame.image.load('assets/police-car.png')
