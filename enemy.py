# enemy.py – UPDATED WORKING ENEMY WITH HEALTH / DAMAGE / DEATH
import pygame
from utils import load_image, load_sound
from settings import ENEMY_SPEED

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = load_image("sprites/enemy.png", fallback_size=(40, 48))
        self.image = pygame.transform.scale(self.image, (40, 48))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vx = 0
        self.vy = 0
        self.on_ground = False

        self.health = 3
        self.hit_flash_timer = 0

        self.snd_hit = load_sound("sounds/hit.wav")

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash_timer = 6

        if self.snd_hit:
            try:
                self.snd_hit.play()
            except:
                pass

        if self.health <= 0:
            self.kill()
            return True
        return False

    def update(self, dt, tiles, player):
        # Follow player if close
        if abs(self.rect.centerx - player.rect.centerx) < 400:
            self.vx = ENEMY_SPEED if self.rect.centerx < player.rect.centerx else -ENEMY_SPEED

        # Horizontal movement
        self.rect.x += int(self.vx * dt)
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vx > 0:
                    self.rect.right = tile.rect.left
                else:
                    self.rect.left = tile.rect.right

        # Gravity
        self.vy += 0.9
        if self.vy > 12:
            self.vy = 12

        # Vertical movement
        self.rect.y += int(self.vy * dt)
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vy > 0:
                    self.rect.bottom = tile.rect.top
                    self.vy = 0
                else:
                    self.rect.top = tile.rect.bottom
                    self.vy = 0

        # Flashing when hit
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1
            self.image.set_alpha(150)
        else:
            self.image.set_alpha(255)
