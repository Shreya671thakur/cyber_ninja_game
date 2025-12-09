# ui.py - HUD / Professional clean UI
import pygame
from settings import WHITE, BLACK, UI_BG, UI_ACCENT

def draw_hud(screen, player, current_level, font):
    # top-left panel
    panel_rect = pygame.Rect(12, 12, 240, 68)
    pygame.draw.rect(screen, UI_BG, panel_rect)
    pygame.draw.rect(screen, UI_ACCENT, panel_rect, 2)

    health_text = font.render(f"Health: {player.health}", True, WHITE)
    level_text = font.render(f"Level: {current_level+1}", True, WHITE)
    proj_text = font.render(f"Ammo: {len(player.projectiles)}", True, WHITE)

    screen.blit(health_text, (22, 20))
    screen.blit(level_text, (22, 40))
    screen.blit(proj_text, (140, 40))

    # bottom center: instruction small text
    w = screen.get_width()
    inst = font.render("Arrows / A D = Move   Space = Jump   J = Shoot   K = Melee", True, WHITE)
    inst_bg = pygame.Surface((inst.get_width()+12, inst.get_height()+8))
    inst_bg.set_alpha(180)
    inst_bg.fill(UI_BG)
    screen.blit(inst_bg, (w//2 - inst.get_width()//2 - 6, screen.get_height()-48))
    screen.blit(inst, (w//2 - inst.get_width()//2, screen.get_height()-44))
