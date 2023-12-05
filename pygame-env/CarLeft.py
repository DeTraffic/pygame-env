from Car import Car

class CarLeft(Car):
    def __init__(self,b1,b2):
        super().__init__(350, 300,'blue',b1,b2)

    def draw(self, screen):
        super().move("RIGHT")
        super().draw(screen)
        

class CarRight(Car):
    def __init__(self,b1,b2):
        super().__init__(800, 300,'red',b1,b2)

    def draw(self, screen):
        super().move("LEFT")
        super().draw(screen)


class CarUp(Car):
    def __init__(self,b1,b2):
        super().__init__(580, 50,'green',b1,b2)

    def draw(self, screen):
        super().move("DOWN")
        super().draw(screen)


class CarDown(Car):
    def __init__(self,b1,b2):
        super().__init__(620, 600,'orange',b1,b2)

    def draw(self, screen):
        super().move("UP")
        super().draw(screen)