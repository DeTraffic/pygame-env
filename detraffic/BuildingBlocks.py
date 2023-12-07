import pygame
from Enums import VehicleAction, Direction, TrafficLightState
import catppuccin
from random import randint
from Vehicles import Car
import itertools


class Intersection(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        lane_width: int,
        lane_height: int,
        left_to_right_lane_count: int,
        right_to_left_lane_count: int,
        top_to_bottom_lane_count: int,
        bottom_to_top_lane_count: int,
        left_to_right_car_spawn_probability: float = 0.6,
        right_to_left_car_spawn_probability: float = 0.6,
        top_to_bottom_car_spawn_probability: float = 0.6,
        bottom_to_top_car_spawn_probability: float = 0.6,
        left_to_right_special_car_spawn_probability: float = 0.05,
        right_to_left_special_car_spawn_probability: float = 0.05,
        top_to_bottom_special_car_spawn_probability: float = 0.05,
        bottom_to_top_special_car_spawn_probability: float = 0.05,
        color: tuple = catppuccin.Flavour.mocha().base.rgb,
    ):
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
        self.rect.center = (x, y)
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
            "left_traffic_light": 0,
            "right_traffic_light": 0,
            "top_traffic_light": 0,
            "bottom_traffic_light": 0,
        }

        self.decay = 0

    def update(self, traffic_light_action):
        now = pygame.time.get_ticks()
        reward = 0

        if (now - self.last_time) >= 100:
            self.last_time = now

            if [self.state["left_traffic_light"], self.state["right_traffic_light"], self.state["top_traffic_light"], self.state["bottom_traffic_light"]] == traffic_light_action:
                self.decay += 1
            else:
                self.decay = 0

            (
                self.state["left_traffic_light"],
                self.state["right_traffic_light"],
                self.state["top_traffic_light"],
                self.state["bottom_traffic_light"],
            ) = traffic_light_action

            print(traffic_light_action)

            for action, traffic_light in zip(
                traffic_light_action, self.traffic_lights_group.sprites()
            ):
                if action:
                    traffic_light.update(TrafficLightState.GREEN)
                else:
                    traffic_light.update(TrafficLightState.RED)

            # Left to right car spawn
            if randint(1, 100) > (
                100 - (self.left_to_right_car_spawn_probability * 100)
            ):
                lane_index = randint(0, self.left_to_right_lane_count - 1)

                for i in range(self.left_to_right_lane_count):
                    i = (i + lane_index) % self.left_to_right_lane_count

                    car = Car(
                        x=self.lane_width / 4,
                        y=self.lane_height
                        + (self.right_to_left_lane_count * self.lane_width)
                        + (i * self.lane_width)
                        + (self.lane_width / 2)
                        - (self.lane_width / 4),
                        width=self.lane_width / 2,
                        height=self.lane_width / 2,
                        accerelation=0.2,
                        speed=5,
                        direction=Direction.LEFT_TO_RIGHT,
                        reward=1,
                    )

                    if car.rect.collideobjects(self.left_cars_group.sprites()):
                        continue

                    self.left_cars_group.add(car)
                    self.state["left_car_count"] += 1
                    break

            # Right to left car spawn
            if randint(1, 100) > (
                100 - (self.right_to_left_car_spawn_probability * 100)
            ):
                lane_index = randint(0, self.right_to_left_lane_count - 1)

                for i in range(self.right_to_left_lane_count):
                    i = (i + lane_index) % self.right_to_left_lane_count

                    car = Car(
                        x=self.width - (3 * self.lane_width / 4),
                        y=self.lane_height
                        + (i * self.lane_width)
                        + (self.lane_width / 2)
                        - (self.lane_width / 4),
                        width=self.lane_width / 2,
                        height=self.lane_width / 2,
                        accerelation=0.2,
                        speed=5,
                        direction=Direction.RIGHT_TO_LEFT,
                        reward=1,
                    )

                    if car.rect.collideobjects(self.right_cars_group.sprites()):
                        continue

                    self.right_cars_group.add(car)
                    self.state["right_car_count"] += 1
                    break

            # Top to bottom car spawn
            if randint(1, 100) > (
                100 - (self.top_to_bottom_car_spawn_probability * 100)
            ):
                lane_index = randint(0, self.top_to_bottom_lane_count - 1)

                for i in range(self.top_to_bottom_lane_count):
                    i = (i + lane_index) % self.top_to_bottom_lane_count

                    car = Car(
                        x=self.lane_height
                        + (i * self.lane_width)
                        + (self.lane_width / 2)
                        - (self.lane_width / 4),
                        y=self.lane_width / 4,
                        width=self.lane_width / 2,
                        height=self.lane_width / 2,
                        accerelation=0.2,
                        speed=5,
                        direction=Direction.TOP_TO_BOTTOM,
                        reward=1,
                    )

                    if car.rect.collideobjects(self.top_cars_group.sprites()):
                        continue

                    self.top_cars_group.add(car)
                    self.state["top_car_count"] += 1
                    break

            # Bottom to top car spawn
            if randint(1, 100) > (
                100 - (self.bottom_to_top_car_spawn_probability * 100)
            ):
                lane_index = randint(0, self.bottom_to_top_lane_count - 1)

                for i in range(self.bottom_to_top_lane_count):
                    i = (i + lane_index) % self.bottom_to_top_lane_count

                    car = Car(
                        x=self.lane_height
                        + (self.top_to_bottom_lane_count * self.lane_width)
                        + (i * self.lane_width)
                        + (self.lane_width / 2)
                        - (self.lane_width / 4),
                        y=self.height - (3 * self.lane_width / 4),
                        width=self.lane_width / 2,
                        height=self.lane_width / 2,
                        accerelation=0.2,
                        speed=5,
                        direction=Direction.BOTTOM_TO_TOP,
                        reward=1,
                    )

                    if car.rect.collideobjects(self.bottom_cars_group.sprites()):
                        continue

                    self.bottom_cars_group.add(car)
                    self.state["bottom_car_count"] += 1
                    break

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
                reward -= 20
                self.score -= 20
                game_over = True

                return reward, self.score, game_over

        to_remove = []

        for car in self.left_cars_group:
            x, y = car.rect.midright

            if x > self.width:
                reward += 1
                self.score += 1
                to_remove.append(car)
                continue

            look_ahead_rect = pygame.Rect(x + car.speed, y, 1, 1)

            traffic_light_collision = look_ahead_rect.collideobjects(
                self.traffic_lights_group.sprites()
            )
            if (
                traffic_light_collision is not None
                and traffic_light_collision.state == TrafficLightState.RED
            ):
                if car.action != VehicleAction.STOP:
                    self.state["left_waiting"] += 1
                car.update(VehicleAction.STOP)
                continue

            if look_ahead_rect.collideobjects(self.left_cars_group.sprites()):
                if car.action != VehicleAction.STOP:
                    self.state["left_waiting"] += 1
                car.update(VehicleAction.STOP)
                continue

            if car.action == VehicleAction.STOP:
                self.state["left_waiting"] -= 1

            car.update(VehicleAction.MOVE)

        for car in to_remove:
            self.state["left_car_count"] -= 1
            self.left_cars_group.remove(car)

        to_remove = []

        for car in self.right_cars_group:
            x, y = car.rect.midleft

            if x < -(self.lane_width / 2):
                reward += 1
                self.score += 1
                to_remove.append(car)
                continue

            look_ahead_rect = pygame.Rect(x - car.speed, y, 1, 1)

            traffic_light_collision = look_ahead_rect.collideobjects(
                self.traffic_lights_group.sprites()
            )
            if (
                traffic_light_collision is not None
                and traffic_light_collision.state == TrafficLightState.RED
            ):
                if car.action != VehicleAction.STOP:
                    self.state["right_waiting"] += 1
                car.update(VehicleAction.STOP)
                continue

            if look_ahead_rect.collideobjects(self.right_cars_group.sprites()):
                if car.action != VehicleAction.STOP:
                    self.state["right_waiting"] += 1
                car.update(VehicleAction.STOP)
                continue

            if car.action == VehicleAction.STOP:
                self.state["right_waiting"] -= 1

            car.update(VehicleAction.MOVE)

        for car in to_remove:
            self.state["right_car_count"] -= 1
            self.right_cars_group.remove(car)

        to_remove = []

        for car in self.top_cars_group:
            x, y = car.rect.midbottom

            if y > self.height:
                reward += 1
                self.score += 1
                to_remove.append(car)
                continue

            look_ahead_rect = pygame.Rect(x, y + car.speed, 1, 1)

            traffic_light_collision = look_ahead_rect.collideobjects(
                self.traffic_lights_group.sprites()
            )
            if (
                traffic_light_collision is not None
                and traffic_light_collision.state == TrafficLightState.RED
            ):
                if car.action != VehicleAction.STOP:
                    self.state["top_waiting"] += 1
                car.update(VehicleAction.STOP)
                continue

            if look_ahead_rect.collideobjects(self.top_cars_group.sprites()):
                if car.action != VehicleAction.STOP:
                    self.state["top_waiting"] += 1
                car.update(VehicleAction.STOP)
                continue

            if car.action == VehicleAction.STOP:
                self.state["top_waiting"] -= 1

            car.update(VehicleAction.MOVE)

        for car in to_remove:
            self.state["top_car_count"] -= 1
            self.top_cars_group.remove(car)

        to_remove = []

        for car in self.bottom_cars_group:
            x, y = car.rect.midtop

            if y < -(self.lane_width / 2):
                reward += 1
                self.score += 1
                to_remove.append(car)
                continue

            look_ahead_rect = pygame.Rect(x, y - car.speed, 1, 1)

            traffic_light_collision = look_ahead_rect.collideobjects(
                self.traffic_lights_group.sprites()
            )
            if (
                traffic_light_collision is not None
                and traffic_light_collision.state == TrafficLightState.RED
            ):
                if car.action != VehicleAction.STOP:
                    self.state["bottom_waiting"] += 1
                car.update(VehicleAction.STOP)
                continue

            if look_ahead_rect.collideobjects(self.bottom_cars_group.sprites()):
                if car.action != VehicleAction.STOP:
                    self.state["bottom_waiting"] += 1
                car.update(VehicleAction.STOP)
                continue

            if car.action == VehicleAction.STOP:
                self.state["bottom_waiting"] -= 1

            car.update(VehicleAction.MOVE)

        for car in to_remove:
            self.state["bottom_car_count"] -= 1
            self.bottom_cars_group.remove(car)

        game_over = False

        reward -= self.state['left_waiting'] * (self.decay ** 2)
        reward -= self.state['right_waiting'] * (self.decay ** 2)
        reward -= self.state['top_waiting'] * (self.decay ** 2)
        reward -= self.state['bottom_waiting'] * (self.decay ** 2)

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
