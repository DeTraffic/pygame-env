
import pygame
import math

class Car(pygame.sprite.Sprite):

    def __init__(self, width, height,image, x=0, y=0):
        """_summary_

        Args:
            width (_type_): _description_
            height (_type_): _description_
            x (_type_): _description_
            y (_type_): _description_
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'assets/{image}.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (width, height)
        self.speed = 5
        self.border_x = x
        self.border_y = y

    def move(self, direction):
        if direction == "UP":
            self.rect.y -= self.speed
        elif direction == "DOWN":
            self.rect.y += self.speed
        elif direction == "LEFT":
            self.rect.x -= self.speed
        elif direction == "RIGHT":
            self.rect.x += self.speed 

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        """_summary_
        """
        newpos = self.calcnewpos(self.rect,self.vector)
        self.rect = newpos

    def calcnewpos(self,rect,vector):
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
    
    def calc_traffic_light(self,intersection):
        if self.rect.x == intersection.rect.center[0] and self.rect.y == intersection.rect.center[0]:
            print("traffic light")

