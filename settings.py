# settings.py - game configuration
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
FPS = 60
GRAVITY = 0.9

TILE_SIZE = 64

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
UI_BG = (18,18,20)
UI_ACCENT = (120, 200, 255)

# Player
PLAYER_SPEED = 5
PLAYER_JUMP_FORCE = -16
PLAYER_WIDTH = 48
PLAYER_HEIGHT = 56

# Enemy
ENEMY_SPEED = 1.6

# Paths
ASSETS_DIR = "assets"
LEVELS_DIR = "levels"


# Backgrounds based on level index
LEVEL_BACKGROUNDS = [
    {
        "far": "assets/bg_far/bg_far.png",
        "mid": "assets/bg_mid/bg_mid.png"
    },
    {
        "far": "assets/bg_far/bg_far2.png",
        "mid": "assets/bg_mid/bg_mid2.png"
    },
    {
        "far": "assets/bg_far/bg_far3.png",
        "mid": "assets/bg_mid/bg_mid3.png"
    }
]
