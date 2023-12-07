
from enum import Enum

class Direction(Enum):
    LEFT_TO_RIGHT = 1
    RIGHT_TO_LEFT = 2
    TOP_TO_BOTTOM = 3
    BOTTOM_TO_TOP = 4

class VehicleAction(Enum):
    MOVE = 1
    STOP = 2

class TrafficLightState(Enum):
    RED = 1
    GREEN = 2