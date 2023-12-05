from sys import exit
import pygame
from Intersection import Intersection
from Car import Car
from CarLeft import *
from catppuccin import Flavour
import random
import gc

def move_car(car):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car.move("UP")
    if keys[pygame.K_DOWN]:
        car.move("DOWN")
    if keys[pygame.K_LEFT]:
        car.move("LEFT")
    if keys[pygame.K_RIGHT]:
        car.move("RIGHT")


def createCar(car_array):
    i = random.randint(0,3)
    if i == 0:
        car_array.append(CarLeft(SCREEN_WIDTH, SCREEN_HEIGHT))

    elif i == 1:
        car_array.append(CarRight(SCREEN_WIDTH, SCREEN_HEIGHT))

    elif i == 2:
        car_array.append(CarUp(SCREEN_WIDTH, SCREEN_HEIGHT))

    elif i == 3:
        car_array.append(CarDown(SCREEN_WIDTH, SCREEN_HEIGHT))


def delete_object(obj,car_array):
    if obj.rect.y < 0 or obj.rect.y > obj.border_y or obj.rect.x < 0 or obj.rect.x > obj.border_x:
        #print("passed border")
        del obj
        gc.collect()
        obj = createCar(car_array=car_array)





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

#car1 = CarLeft(SCREEN_WIDTH, SCREEN_HEIGHT)
#car2 = CarRight(SCREEN_WIDTH, SCREEN_HEIGHT)
#car3 = CarUp(SCREEN_WIDTH, SCREEN_HEIGHT)
#car4 = CarDown(SCREEN_WIDTH, SCREEN_HEIGHT)

car_array = []

for iter in range(4):
    createCar(car_array=car_array)  

# Reference Car
car5 = Car(100,100,'car')

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    

    pygame.display.update()
    intersection.draw(screen)

    for car in car_array:
        car.draw(screen=screen)
        car.calc_traffic_light(intersection)
        delete_object(car,car_array=car_array)

    # intersection2.draw(screen)

    # Restrict maximum fps
    clock.tick(MAX_FPS)