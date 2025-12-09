# level_manager.py – UPDATED (enemy group logic + transitions fixed)
import pygame
from utils import play_music, load_image
from level import load_level
from settings import SCREEN_HEIGHT

class LevelManager:
    def __init__(self, screen, player, levels):
        self.screen = screen
        self.player = player
        self.levels = levels
        self.current_level_index = 0

        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.goal_rect = None

        # Load backgrounds (fallback-safe)
        self.bg_far = load_image("bg_far/bg_far.png", fallback_size=(800, 600))
        self.bg_mid = load_image("bg_mid/bg_mid.png", fallback_size=(800, 600))

    def load_level(self, index):
        """Loads a level from CSV and resets player state."""
        self.current_level_index = index

        tiles, player_start, enemies, goal_rect = load_level(self.levels[index])

        self.tiles = tiles
        self.enemies = enemies
        self.goal_rect = goal_rect

        # reset player state
        if hasattr(self.player, "reset_state"):
            self.player.reset_state()

        self.player.rect.x, self.player.rect.y = player_start

        # play background music
        play_music("music/background_music.mp3", volume=0.7)

    def update(self, player_rect):
        """Checks level events and returns transition state if needed."""
        # Player fell
        if player_rect.y > SCREEN_HEIGHT + 200:
            return "GAME OVER"

        # Reached goal rectangle
        if self.goal_rect and player_rect.colliderect(self.goal_rect):
            self.current_level_index += 1
            if self.current_level_index >= len(self.levels):
                return "YOU WIN"
            return "NEXT LEVEL"

        # All enemies dead → next level
        if not any(e.alive() for e in self.enemies):
            self.current_level_index += 1
            if self.current_level_index >= len(self.levels):
                return "YOU WIN"
            return "NEXT LEVEL"

        return None

    def draw(self, screen, camera_x):
        """Draws backgrounds, tiles, enemies with parallax effect."""
        # Far background
        if self.bg_far:
            w = self.bg_far.get_width()
            x = (-camera_x * 0.15) % w
            screen.blit(self.bg_far, (x - w, 0))
            screen.blit(self.bg_far, (x, 0))

        # Mid background
        if self.bg_mid:
            w2 = self.bg_mid.get_width()
            x2 = (-camera_x * 0.30) % w2
            screen.blit(self.bg_mid, (x2 - w2, 0))
            screen.blit(self.bg_mid, (x2, 0))

        # Tiles & enemies
        for tile in self.tiles:
            screen.blit(tile.image, (tile.rect.x - camera_x, tile.rect.y))

        for enemy in self.enemies:
            screen.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y))
