# tile.py - simple tile class
import pygame
from settings import TILE_SIZE

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, w=TILE_SIZE, h=TILE_SIZE, image=None):
        super().__init__()
        if image is None:
            self.image = pygame.Surface((w,h))
            self.image.fill((100,100,100))
        else:
            self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))
