import pygame
from sys import exit
from random import randint
from Vehicles import Car
from Enums import VehicleAction, Direction, TrafficLightState
from BuildingBlocks import Road,TrafficLight
import itertools

import catppuccin


class IntersectionGame(pygame.sprite.Sprite):
    def __init__(
        self,
        GAME_NAME,
        GAME_WIDTH,
        GAME_HEIGHT,
        MAX_FPS,
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
        color: tuple = catppuccin.Flavour.mocha().base.rgb,
        BG_COLOR: tuple = catppuccin.Flavour.mocha().mauve.rgb,
        
    ):
        
        #--------------------------------------
        self.GAME_WIDTH = GAME_WIDTH
        self.GAME_HEIGHT = GAME_HEIGHT
        self.MAX_FPS = MAX_FPS
        self.BG_COLOR = BG_COLOR

        pygame.init()
        pygame.display.set_caption(GAME_NAME)

        self.screen = pygame.display.set_mode((self.GAME_WIDTH, self.GAME_HEIGHT))
        self.clock = pygame.time.Clock()
        
        #---------------- Yukarısı taşınacak
        pygame.sprite.Sprite.__init__(self)

        self.center_width = lane_width * (
            top_to_bottom_lane_count + bottom_to_top_lane_count
        )
        self.center_height = lane_width * (
            left_to_right_lane_count + right_to_left_lane_count
        )


        self.lane_width = lane_width
        self.lane_height = lane_height

        self.left_to_right_lane_count = left_to_right_lane_count
        self.right_to_left_lane_count = right_to_left_lane_count
        self.top_to_bottom_lane_count = top_to_bottom_lane_count
        self.bottom_to_top_lane_count = bottom_to_top_lane_count

        self.left_to_right_car_spawn_probability = left_to_right_car_spawn_probability
        self.right_to_left_car_spawn_probability = right_to_left_car_spawn_probability
        self.top_to_bottom_car_spawn_probability = top_to_bottom_car_spawn_probability
        self.bottom_to_top_car_spawn_probability = bottom_to_top_car_spawn_probability
        
        self.left_to_right_special_car_spawn_probability = left_to_right_special_car_spawn_probability
        self.right_to_left_special_car_spawn_probability = right_to_left_special_car_spawn_probability
        self.top_to_bottom_special_car_spawn_probability = top_to_bottom_special_car_spawn_probability
        self.bottom_to_top_special_car_spawn_probability = bottom_to_top_special_car_spawn_probability

        self.left_to_right_special_car_spawn_probability = (
            left_to_right_special_car_spawn_probability
        )
        self.right_to_left_special_car_spawn_probability = (
            right_to_left_special_car_spawn_probability
        )
        self.top_to_bottom_special_car_spawn_probability = (
            top_to_bottom_special_car_spawn_probability
        )
        self.bottom_to_top_special_car_spawn_probability = (
            bottom_to_top_special_car_spawn_probability
        )

        self.width = (lane_height * 2) + self.center_width
        self.height = (lane_height * 2) + self.center_height

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.GAME_WIDTH / 2,self.GAME_HEIGHT / 2)
        self._init_intersection()

        self.last_time = pygame.time.get_ticks()

        self.score = 0
        self.state = {
            "left_car_count": 0,
            "right_car_count": 0,
            "top_car_count": 0,
            "bottom_car_count": 0,
            "left_waiting": 0,
            "right_waiting": 0,
            "top_waiting": 0,
            "bottom_waiting": 0,
            "left_decay": 0,
            "right_decay": 0,
            "top_decay": 0,
            "bottom_decay": 0,
            "left_center": 0,
            "right_center": 0,
            "top_center": 0,
            "bottom_center": 0,
            "left_traffic_light": 0,
            "right_traffic_light": 0,
            "top_traffic_light": 0,
            "bottom_traffic_light": 0,
        }

        self.iteration = 0
        self.reset()

    def __car_spawn(self,lane_probability,lane_count,cars_group,lane_count_pos, car_x, car_y, car_direction,cr_dir):
        if randint(1, 100) > (
                100 - (lane_probability * 100)
            ):
                lane_index = randint(0, lane_count - 1)

                for i in range(lane_count):
                    i = (i + lane_index) % lane_count
                    
                    car = Car(
                        x=car_x(lane_count_pos,i),
                        y=car_y(lane_count_pos,i),

                        width=self.lane_width / 2,
                        height=self.lane_width / 2,
                        accerelation=0.2,
                        speed=5,
                        direction=car_direction,
                        reward=1,
                    )

                    if car.rect.collideobjects(cars_group.sprites()):
                        continue

                    cars_group.add(car)
                    self.state[cr_dir+"_car_count"] += 1
                    break

    # ------------------------- Helper Functions -------------------------------------------------------------
    def __param_plus(self,param,car):
        # x + car.speed, y,
        return param + car   
    
    def __param_minus(self,param,car):
        #x - car.speed - 1, y
        return param - car - 1
    
    def __param_just(self,param,car):
        #x, y + car.speed
        return param
    
    def __div4(self,lane_count,i):
        return self.lane_width / 4
    
    def __width_div4(self,lane_count,i):
        return self.width - (3 * self.lane_width / 4)
    
    def __height_div4(self,lane_count,i):
        return self.height - (3 * self.lane_width / 4)
    
    def __long_calc1(self,lane_count,i):
        return self.lane_height + (lane_count * self.lane_width) + (i * self.lane_width) + (self.lane_width / 2) - (self.lane_width / 4)
    
    def __long_calc2(self,lane_count,i):
        return self.lane_height + (i * self.lane_width) + (self.lane_width / 2) - (self.lane_width / 4)
    # ------------------------- /Helper Functions -------------------------------------------------------------
    


    def __car_control(self,car_group,to_remove,rect_x,rect_y,car_direction,reward):
        for car in car_group:
            if car_direction == "left":
                x, y = car.rect.midright
            elif car_direction == "right":
                x, y = car.rect.midleft
            elif car_direction == "top":
                x, y = car.rect.midbottom
            elif car_direction == "bottom":
                x, y = car.rect.midtop
            else:
                x,y = -1,-1

            if x > self.width or x < 0 or x < -(self.lane_width / 2) or y > self.height or y < -(self.lane_width / 2):
                reward += 1
                self.score += 1
                to_remove.append(car)
                continue

            look_ahead_rect = pygame.Rect(rect_x(x,car.speed), rect_y(y,car.speed), 1, 1)


            traffic_light_collision = look_ahead_rect.collideobjects(
                self.traffic_lights_group.sprites()
            )

            if (
                traffic_light_collision is not None
                and traffic_light_collision.state == TrafficLightState.RED
            ):
                if car.action != VehicleAction.STOP:
                    self.state[str(car_direction)+"_waiting"] += 1
                car.update(VehicleAction.STOP)

                continue

            

            if look_ahead_rect.collideobjects(car_group.sprites()):
                if car.action != VehicleAction.STOP:
                    self.state[str(car_direction)+"_waiting"] += 1
                car.update(VehicleAction.STOP)
                continue

            

            if car.action == VehicleAction.STOP:
                self.state[str(car_direction)+"_waiting"] -= 1

            car.update(VehicleAction.MOVE)

        for car in to_remove:
            self.state[str(car_direction)+"_car_count"] -= 1
            car_group.remove(car)

        to_remove = []

    def update(self, traffic_light_action):
        now = pygame.time.get_ticks()
        reward = 0

        if (now - self.last_time) >= 100:
            self.last_time = now

            if self.state["left_traffic_light"] == traffic_light_action[0]:
                self.state["left_decay"] += 1
            else:
                self.state["left_decay"] = 0

            if self.state["right_traffic_light"] == traffic_light_action[1]:
                self.state["right_decay"] += 1
            else:
                self.state["right_decay"] = 0

            if self.state["top_traffic_light"] == traffic_light_action[2]:
                self.state["top_decay"] += 1
            else:
                self.state["top_decay"] = 0

            if self.state["bottom_traffic_light"] == traffic_light_action[3]:
                self.state["bottom_decay"] += 1
            else:
                self.state["bottom_decay"] = 0

            # ---------------------------------------------------------------------------
            # Left to right car spawn
            self.__car_spawn(self.left_to_right_car_spawn_probability,self.left_to_right_lane_count,self.left_cars_group,
                             self.right_to_left_lane_count,self.__div4, self.__long_calc1, Direction.LEFT_TO_RIGHT,"left" )
            # ---------------------------------------------------------------------------        
            # Right to left car spawn
            self.__car_spawn(self.right_to_left_car_spawn_probability,self.right_to_left_lane_count,self.right_cars_group, 
                            self.left_to_right_lane_count,self.__width_div4,self.__long_calc2,Direction.RIGHT_TO_LEFT,"right")
            # ---------------------------------------------------------------------------  
            # Top to bottom car spawn
            self.__car_spawn(self.top_to_bottom_car_spawn_probability,self.top_to_bottom_lane_count,self.top_cars_group,    
                             self.bottom_to_top_lane_count,self.__long_calc2,self.__div4,Direction.TOP_TO_BOTTOM,"top")
            # ---------------------------------------------------------------------------  
            # Bottom to top car spawn
            self.__car_spawn(self.bottom_to_top_car_spawn_probability,self.bottom_to_top_lane_count,self.bottom_cars_group,                         
                             self.top_to_bottom_lane_count,self.__long_calc1,self.__height_div4,Direction.BOTTOM_TO_TOP,"bottom")
            # ---------------------------------------------------------------------------          

        (
            self.state["left_traffic_light"],
            self.state["right_traffic_light"],
            self.state["top_traffic_light"],
            self.state["bottom_traffic_light"],
            _,
        ) = traffic_light_action

        for i in range(4):
            if traffic_light_action[i]:
                self.traffic_lights_group.sprites()[i].update(TrafficLightState.GREEN)
            else:
                self.traffic_lights_group.sprites()[i].update(TrafficLightState.RED)

        for group_1, group_2 in itertools.combinations(
            (
                self.left_cars_group,
                self.right_cars_group,
                self.top_cars_group,
                self.bottom_cars_group,
            ),
            2,
        ):
            if pygame.sprite.groupcollide(group_1, group_2, False, False):
                reward -= 10
                self.score -= 10
                game_over = True

                return reward, self.score, game_over

        center_rect = pygame.Rect(
                    self.lane_height,
                    self.lane_height,
                    self.center_width,
                    self.center_height)

        self.state["left_center"] = len(center_rect.collidelistall(self.left_cars_group.sprites()))
        self.state["right_center"] = len(center_rect.collidelistall(self.right_cars_group.sprites()))
        self.state["top_center"] = len(center_rect.collidelistall(self.top_cars_group.sprites()))
        self.state["bottom_center"] = len(center_rect.collidelistall(self.bottom_cars_group.sprites()))

        to_remove = []

        #---------------------------------------------------------------------------------
        # Left Car groups
        self.__car_control(self.left_cars_group,to_remove,self.__param_plus,self.__param_just,"left",reward)
        #---------------------------------------------------------------------------------
        # Right Car groups
        self.__car_control(self.right_cars_group,to_remove,self.__param_minus,self.__param_just,"right",reward)
        #---------------------------------------------------------------------------------
        # Top Car groups
        self.__car_control(self.top_cars_group,to_remove,self.__param_just,self.__param_plus,"top",reward)
        #---------------------------------------------------------------------------------
        # Bottom Car groups
        self.__car_control(self.bottom_cars_group,to_remove,self.__param_just,self.__param_minus,"bottom",reward)
        #---------------------------------------------------------------------------------

        game_over = False

        reward -= self.state["left_waiting"] * (
            max(0, self.state["left_decay"] / 60) ** 2
        )
        reward -= self.state["right_waiting"] * (
            max(0, self.state["right_decay"] / 60) ** 2
        )
        reward -= self.state["top_waiting"] * (max(0, self.state["top_decay"] / 60) ** 2)
        reward -= self.state["bottom_waiting"] * (
            max(0, self.state["bottom_decay"] / 60) ** 2
        )

        print("Reward:", reward)
        print(self.state)

        return reward, self.score, game_over

    def draw(self, surface):
        """_summary_

        Args:
            surface (_type_): _description_
        """
        self.roads_group.draw(self.image)
        self.image.blit(self.center_road, (self.lane_height, self.lane_height))
        self.traffic_lights_group.draw(self.image)
        self.left_cars_group.draw(self.image)
        self.right_cars_group.draw(self.image)
        self.top_cars_group.draw(self.image)
        self.bottom_cars_group.draw(self.image)
        surface.blit(self.image, self.rect)

    def _init_intersection(self):
        """_summary_"""

        self.roads_group = pygame.sprite.Group()
        self.traffic_lights_group = pygame.sprite.Group()
        self.left_cars_group = pygame.sprite.Group()
        self.right_cars_group = pygame.sprite.Group()
        self.top_cars_group = pygame.sprite.Group()
        self.bottom_cars_group = pygame.sprite.Group()

        left_road = Road(
            0,
            (self.height - self.center_height) / 2,
            self.left_to_right_lane_count,
            self.right_to_left_lane_count,
            self.lane_width,
            self.lane_height,
            Direction.LEFT_TO_RIGHT,
        )
        right_road = Road(
            self.width - self.lane_height,
            (self.height - self.center_height) / 2,
            self.right_to_left_lane_count,
            self.left_to_right_lane_count,
            self.lane_width,
            self.lane_height,
            Direction.RIGHT_TO_LEFT,
        )
        top_road = Road(
            (self.width - self.center_width) / 2,
            0,
            self.top_to_bottom_lane_count,
            self.bottom_to_top_lane_count,
            self.lane_width,
            self.lane_height,
            Direction.TOP_TO_BOTTOM,
        )
        bot_road = Road(
            (self.width - self.center_width) / 2,
            self.height - self.lane_height,
            self.bottom_to_top_lane_count,
            self.top_to_bottom_lane_count,
            self.lane_width,
            self.lane_height,
            Direction.BOTTOM_TO_TOP,
        )
        self.center_road = pygame.Surface((self.center_width, self.center_height))
        self.center_road.fill(catppuccin.Flavour.mocha().surface0.rgb)

        self.roads_group.add(left_road)
        self.roads_group.add(right_road)
        self.roads_group.add(top_road)
        self.roads_group.add(bot_road)

        left_traffic_light = TrafficLight(
            self.lane_height - (self.lane_width / 2),
            self.lane_height + (self.right_to_left_lane_count * self.lane_width),
            self.lane_width / 2,
            self.left_to_right_lane_count * self.lane_width,
            Direction.LEFT_TO_RIGHT,
        )

        right_traffic_light = TrafficLight(
            self.lane_height + self.center_width,
            self.lane_height,
            self.lane_width / 2,
            self.right_to_left_lane_count * self.lane_width,
            Direction.RIGHT_TO_LEFT,
        )

        top_traffic_light = TrafficLight(
            self.lane_height,
            self.lane_height - (self.lane_width / 2),
            self.top_to_bottom_lane_count * self.lane_width,
            self.lane_width / 2,
            Direction.TOP_TO_BOTTOM,
        )

        bot_traffic_light = TrafficLight(
            self.lane_height + (self.top_to_bottom_lane_count * self.lane_width),
            self.lane_height + self.center_height,
            self.bottom_to_top_lane_count * self.lane_width,
            self.lane_width / 2,
            Direction.BOTTOM_TO_TOP,
        )

        self.traffic_lights_group.add(left_traffic_light)
        self.traffic_lights_group.add(right_traffic_light)
        self.traffic_lights_group.add(top_traffic_light)
        self.traffic_lights_group.add(bot_traffic_light)
    

    def run(self):
        while True:
            reward, score, game_over = self.play_step(action)

            if game_over:
                break
        
        print(f"Final score: {score}")
        
    def play_step(self, action):
        
        # ----------------------- burayı olduğu gibi taşı

        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        reward, score, game_over = self.update(action)
        self.draw(self.screen)
        pygame.display.flip()

        self.clock.tick(self.MAX_FPS)
        
        return reward, score, game_over

    def reset(self):

        self._init_intersection()

        #----------------------alt taraf taşınacak

        background = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))
        background.fill(self.BG_COLOR)
        self.screen.blit(background, (0, 0))

        self.iteration += 1
        self.frame_iteration = 0

    def reward(self):
        pass