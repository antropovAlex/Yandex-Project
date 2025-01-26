import pygame
import sys
import os


def load_image(name):
    filename = os.path.join("data", name)
    try:
        image = pygame.image.load(filename)
    except Exception:
        print(f"Ничего не найдено{filename}")
        pygame.quit()
        sys.exit()
    return image
