SCREEN_TITLE = "Asteroids"
WIDTH = 700
HEIGHT = 700
FPS = 60
ALPHA = 60
####################
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
####################
OBJECT_POINTS = {
    'Player': {
        'Ship-1': {
            'radius': [1, 1, 1, 2],
            'angles': [225, 90, 315, 270]
        },
    },
    'Enemy': {
        'Asteroid-1': {
            'radius': [1, 2, 1, 1, 1, 2, 1, 1],
            'angles': [5, 35, 105, 165, 245, 285, 315, 335]
        },
    },
}
