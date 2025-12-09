# player.py - player class with shooting & melee (updated)
import pygame
from settings import PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_JUMP_FORCE, GRAVITY
from utils import load_image, load_sound

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, vx):
        super().__init__()
        self.image = pygame.Surface((12, 6), pygame.SRCALPHA)
        self.image.fill((255, 200, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx

    def update(self, dt, tiles):
        self.rect.x += int(self.vx * dt)
        if self.rect.right < -200 or self.rect.left > 4000:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("sprites/player.png", fallback_size=(PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.facing = 1

        self.health = 6
        self.last_shot = 0
        self.projectiles = pygame.sprite.Group()
        self.melee_cooldown_end = 0

        # sounds (may be None if missing)
        self.snd_jump = load_sound("sounds/jump.wav")
        self.snd_shoot = load_sound("sounds/shoot.wav")

    def reset_state(self):
        self.health = 6
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        try:
            self.projectiles.empty()
        except:
            self.projectiles = pygame.sprite.Group()

    def handle_input(self, keys):
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
            self.facing = 1

    def jump(self):
        if self.on_ground:
            self.vy = PLAYER_JUMP_FORCE
            self.on_ground = False
            if self.snd_jump:
                self.snd_jump.play()

    def shoot(self, now=None):
        # now optional; default to pygame ticks
        if now is None:
            now = pygame.time.get_ticks()
        if now - self.last_shot < 300:
            return
        vx = 12 * self.facing
        px = self.rect.centerx + self.facing * 30
        py = self.rect.centery - 6
        proj = Projectile(px, py, vx)
        self.projectiles.add(proj)
        self.last_shot = now
        if self.snd_shoot:
            self.snd_shoot.play()

    def melee(self, now=None):
        if now is None:
            now = pygame.time.get_ticks()
        if now < self.melee_cooldown_end:
            return None
        self.melee_cooldown_end = now + 450
        return pygame.Rect(self.rect.centerx + self.facing*20, self.rect.centery-16, 40, 32)

    def apply_gravity(self):
        self.vy += GRAVITY

    def update(self, dt, tiles):
        # horizontal movement + collisions
        self.rect.x += int(self.vx * dt)
        self.handle_horizontal_collisions(tiles)
        # vertical
        self.apply_gravity()
        self.rect.y += int(self.vy * dt)
        self.handle_vertical_collisions(tiles)
        # update projectiles
        self.projectiles.update(dt, tiles)

    def handle_horizontal_collisions(self, tiles):
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vx > 0:
                    self.rect.right = tile.rect.left
                elif self.vx < 0:
                    self.rect.left = tile.rect.right

    def handle_vertical_collisions(self, tiles):
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vy > 0:
                    self.rect.bottom = tile.rect.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = tile.rect.bottom
                    self.vy = 0
