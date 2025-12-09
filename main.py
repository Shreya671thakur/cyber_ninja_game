# main.py – FULL WORKING VERSION WITH SHOOT / MELEE / LEVEL SWITCH
import pygame, sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from level_manager import LevelManager
from player import Player
from ui import draw_hud
from utils import load_sound

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyber Ninja Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 28)

# Player
player = Player(100, 100)

# Levels
levels = ["level1.csv", "level2.csv", "level3.csv"]

manager = LevelManager(screen, player, levels)
manager.load_level(0)

hit_snd = load_sound("sounds/hit.wav")

transition_text = None
transition_start = 0

def show_transition(text):
    global transition_text, transition_start
    transition_text = text
    transition_start = pygame.time.get_ticks()

while True:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if transition_text:
                continue

            if event.key == pygame.K_SPACE:
                player.jump()

            if event.key == pygame.K_j:
                player.shoot()

            if event.key == pygame.K_k:
                hb = player.melee()
                if hb:
                    for enemy in manager.enemies:
                        if hb.colliderect(enemy.rect):
                            enemy.take_damage(2)

    # Transition Screen
    if transition_text:
        screen.fill((0, 0, 0))
        txt = font.render(transition_text, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        pygame.display.update()

        if pygame.time.get_ticks() - transition_start > 2000:
            if transition_text == "YOU WIN":
                pygame.quit()
                sys.exit()

            manager.load_level(manager.current_level_index)
            transition_text = None
        continue

    # Gameplay
    keys = pygame.key.get_pressed()
    player.handle_input(keys)

    player.update(dt/16, manager.tiles)
    manager.enemies.update(dt/16, manager.tiles, player)

    # Projectile vs Enemy
    for proj in list(player.projectiles):
        for enemy in manager.enemies:
            if proj.rect.colliderect(enemy.rect):
                enemy.take_damage(1)
                proj.kill()
                if hit_snd:
                    hit_snd.play()

    # Check Level Transitions
    state = manager.update(player.rect)
    if state:
        show_transition(state)
        continue

    # Camera
    camera_x = max(0, player.rect.centerx - SCREEN_WIDTH//2)

    # Draw
    manager.draw(screen, camera_x)

    screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))

    for proj in player.projectiles:
        screen.blit(proj.image, (proj.rect.x - camera_x, proj.rect.y))

    draw_hud(screen, player, manager.current_level_index + 1, font)

    pygame.display.flip()
