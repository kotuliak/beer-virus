from enum import Enum

class GameState(Enum):
    NOT_STARTED = 0
    STARTED = 1
    GOOD_GUYS_WON = 2
    BAD_GUYS_WON = 3