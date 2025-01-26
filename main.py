import pygame
import sys

# Импортируем необходимые модули
from pl import *
from load_file import load_image

# Инициализация Pygame
pygame.init()
WINDOW_SIZE = width, height = 750, 600
FPS = 50
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

player = None
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


class Camera:
    def init(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        x, y = target.pos
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2) - 125
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2) - 50
        target.move(x + self.dx//25, y + self.dy//25)
        print(self.dx, self.dy)



camera = Camera()


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
        hero.move(x, y - 1)
    elif movement == "down":
        hero.move(x, y + 1)
    elif movement == "left":
        hero.move(x - 1, y)
    elif movement == "right":
        hero.move(x + 1, y)


def main_game():
    global player
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
        camera.update(player)
        for sprite in tail_sprite:
            camera.apply(sprite)
        tail_sprite.draw(screen)
        hero_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


start_screen()
main_game()


if __name__ == "__main__":
    main()
