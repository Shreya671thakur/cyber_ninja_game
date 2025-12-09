# utils.py - load images and sounds (updated)
import os
import pygame
from settings import ASSETS_DIR

def asset_path(*parts):
    """
    Build path relative to ASSETS_DIR (e.g. "bg_mid/bg_mid.png" -> "assets/bg_mid/bg_mid.png")
    """
    return os.path.join(ASSETS_DIR, *parts)

def load_image(subpath, fallback_size=(64,64)):
    """
    subpath e.g. "sprites/player.png" or "bg_mid/bg_mid.png"
    """
    path = asset_path(subpath)
    try:
        img = pygame.image.load(path).convert_alpha()
        return img
    except Exception:
        # safe fallback - semi-transparent gray
        surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surf.fill((150,150,150,255))
        print(f"⚠ load_image: missing {path} — using fallback")
        return surf

def load_sound(subpath):
    """
    subpath e.g. "sounds/hit.wav"
    returns pygame.mixer.Sound or None if missing
    """
    path = asset_path(subpath)
    if not os.path.exists(path):
        print(f"⚠ load_sound: missing {path}")
        return None
    try:
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"⚠ load_sound: could not load {path} -> {e}")
        return None

def play_music(subpath, volume=0.5):
    """
    Plays background music (loop). Tries the exact subpath, then tries
    to replace '_' <-> ' ' if needed (to match filenames).
    subpath is relative to ASSETS_DIR, e.g. "music/background_music.mp3"
    """
    # candidate paths
    candidates = []
    candidates.append(asset_path(subpath))
    # also try replacing underscores / spaces both ways
    candidates.append(asset_path(subpath.replace("_", " ")))
    candidates.append(asset_path(subpath.replace(" ", "_")))

    for full in candidates:
        if os.path.exists(full):
            try:
                pygame.mixer.music.load(full)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)
                print(f"▶ Playing music: {full}")
                return True
            except Exception as e:
                print(f"⚠ play_music: failed to play {full} -> {e}")
                return False

    print(f"⚠ play_music: no music file found among candidates: {candidates}")
    return False
