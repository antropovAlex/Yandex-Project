import pygame
import sys

from pl import *
from load_file import load_image

player = None
pygame.init()
WINDOW_SIZE = 750, 600
FPS = 50
TAIL_SIZE = 500
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
lm = []


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "maps/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        lm.append(level_map)
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('room', x, y)
            elif level[y][x] == '|':
                Tile('vertical', x, y)
            elif level[y][x] == '-':
                Tile('horizontal', x, y)
            elif level[y][x] == '*':
                Tile('start', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '$':
                Tile('finish', x, y)
    return new_player


player = generate_level(load_level("m1.txt"))


def start_screen():
    fon = pygame.transform.scale(load_image("fon.png"), WINDOW_SIZE)
    screen.blit(fon, (0, 0))
    R = True
    while R:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                R = False
                break
        pygame.display.flip()


def move(hero, movement):
    x, y = hero.pos
    if movement == "up":
        print(y)
        if y - 1 >= -15:
            hero.move(x, y - 1)
    elif movement == "down":
        if (y + 1) * 25 < len(lm[0]) * 500:
            hero.move(x, y + 1)
    elif movement == "left":
        if x - 1 >= -15:
            hero.move(x - 1, y)
    elif movement == "right":
        if (x + 1) * 25 < len(lm[0][0]) * 500:
            hero.move(x + 1, y)


def main():
    pygame.display.set_caption("Марио")
    start_screen()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move(player, "up")
                elif event.key == pygame.K_DOWN:
                    move(player, "down")
                elif event.key == pygame.K_LEFT:
                    move(player, "left")
                elif event.key == pygame.K_RIGHT:
                    move(player, "right")

        screen.fill((0, 0, 0))
        tail_sprite.draw(screen)
        hero_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    terminate()


if __name__ == "__main__":
    main()
