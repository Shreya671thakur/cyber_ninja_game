# level.py – UPDATED (uses sprite Groups for enemies & tiles)
import csv, os
import pygame
from settings import LEVELS_DIR, TILE_SIZE
from tile import Tile
from enemy import Enemy

def parse_cell(cell):
    try:
        return int(cell)
    except:
        return 0

def load_level(filename):
    """
    Loads a level CSV file:
    0 = empty
    1 = tile
    2 = enemy
    3 = player start
    4 = goal
    Returns tile_group, player_start, enemies_group, goal_rect
    """
    path = os.path.join(LEVELS_DIR, filename)

    tiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player_start = (100, 100)
    goal_rect = None

    with open(path, newline='') as csvfile:
        rows = list(csv.reader(csvfile))

    for r_idx, row in enumerate(rows):
        for c_idx, cell in enumerate(row):
            val = parse_cell(cell)
            x = c_idx * TILE_SIZE
            y = r_idx * TILE_SIZE

            if val == 1:
                tiles.add(Tile(x, y))

            elif val == 2:
                e = Enemy(x, y - 48)
                enemies.add(e)

            elif val == 3:
                player_start = (x, y - 48)

            elif val == 4:
                goal_rect = pygame.Rect(
                    x + TILE_SIZE // 4,
                    y + TILE_SIZE // 4,
                    TILE_SIZE // 2,
                    TILE_SIZE // 2
                )

    return tiles, player_start, enemies, goal_rect
