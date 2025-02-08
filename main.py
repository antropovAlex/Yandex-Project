import pygame
import random
import sys
import time
import math
from dungeon_generator import generate_dungeon

SCORE = 0
kill_count = 0  # Переменная для отслеживания убитых врагов

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Soul Knight Clone")

damage_taken = pygame.mixer.Sound("./sounds/uh-steve-minecraft-online-audio-converter.mp3")
shoot = pygame.mixer.Sound("./sounds/mixkit-game-gun-shot-1662.mp3")
pygame.mixer.music.load('./sounds/Dark Dungeon.mp3')

backgr = pygame.image.load("preview.png")
defeat = pygame.image.load("deshiro-defeat-screen-png.jpg")

# FPS
FPS = 60
clock = pygame.time.Clock()

# Загрузка текстур
room_texture = pygame.image.load("room.png")
room_texture = pygame.transform.scale(room_texture, (WIDTH, HEIGHT))
trap_image = pygame.image.load("./sprites/trap_inactive.png")
trap_image2 = pygame.image.load("./sprites/trap_active.png")
player_image = pygame.image.load("./sprites/skp.gif")
bullet_image = pygame.image.load("./sprites/skb.png")
bullet1_image = pygame.image.load("./sprites/1skb.png")
bullet2_image = pygame.image.load("./sprites/2skb.png")
bullet3_image = pygame.image.load("./sprites/3skb.png")
enemy1_image = pygame.image.load("./sprites/ske.gif")
enemy2_image = pygame.image.load("./sprites/Mount_boar.gif")
enemy3_image = pygame.image.load("./sprites/Mount_gentle_snow_ape.gif")
boss_image = pygame.image.load("./sprites/RF_Boss_Warden.gif")
box_blue_image = pygame.image.load("./sprites/blue.png")
box_yellow_image = pygame.image.load("./sprites/yellow.png")
box_red_image = pygame.image.load("./sprites/red.png")
bullet3_image = pygame.transform.rotate(bullet3_image, 90)

# Масштабирование изображений
player_image = pygame.transform.scale(player_image, (50, 50))
bullet_image = pygame.transform.scale(bullet_image, (30, 20))
bullet1_image = pygame.transform.scale(bullet1_image, (30, 20))
bullet2_image = pygame.transform.scale(bullet2_image, (30, 20))
bullet3_image = pygame.transform.scale(bullet3_image, (30, 20))
enemy1_image = pygame.transform.scale(enemy1_image, (50, 50))
enemy2_image = pygame.transform.scale(enemy2_image, (50, 50))
enemy3_image = pygame.transform.scale(enemy3_image, (50, 50))
boss_image = pygame.transform.scale(boss_image, (70, 70))
trap_image = pygame.transform.scale(trap_image, (50, 50))
trap_image2 = pygame.transform.scale(trap_image2, (50, 50))
box_blue_image = pygame.transform.scale(box_blue_image, (50, 50))
box_yellow_image = pygame.transform.scale(box_yellow_image, (50, 50))
box_red_image = pygame.transform.scale(box_red_image, (50, 50))

bullet1_icon = pygame.transform.scale(bullet1_image, (240, 160))
bullet2_icon = pygame.transform.scale(bullet2_image, (240, 160))
bullet3_icon = pygame.transform.scale(bullet3_image, (240, 160))

icon = {
    "red": bullet1_icon,
    "blue": bullet2_icon,
    "yellow": bullet3_icon,
}

bullet_damage = 0.75
# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Размеры карты и комнаты
ROOM_WIDTH, ROOM_HEIGHT = 800, 600
BOX = {"red": box_red_image,
       "yellow": box_yellow_image,
       "blue": box_blue_image,
       }

start_point, boss_room, rooms = generate_dungeon()


def chest_rooms_selection():
    rooms_list = list(rooms.keys())

    red_box_room = random.choice(rooms_list)
    idx1 = rooms_list.index(red_box_room)
    del rooms_list[idx1]

    blue_box_room = random.choice(rooms_list)
    idx2 = rooms_list.index(blue_box_room)
    del rooms_list[idx2]

    yellow_box_room = random.choice(rooms_list)
    idx3 = rooms_list.index(yellow_box_room)
    del rooms_list[idx3]

    return [red_box_room, blue_box_room, yellow_box_room]


placement = chest_rooms_selection()

MAP_LAYOUT = {
    "start": start_point,
    "rooms": rooms,
    "box": {
        placement[0]: "red",
        placement[1]: "blue",
        placement[2]: "yellow"
    }
}

wearpon = {
    1: "red",
    2: ""
}

switch = 1

wall_patterns = {
    1: [(282, 280), (488, 280)]
}

# Словарь для отслеживания состояния комнат
room_enemy_status = {room: True for room in MAP_LAYOUT["rooms"].keys()}

# Начальная комната
current_room = MAP_LAYOUT["start"]

SCORE = 0

time_shoot = 10

Bullet_now = "red"

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.score = 0
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
        self.health = 10  # Здоровье игрока
        self.weapon = ""

    def update(self, keys):
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def shoot(self, direction):
        Bullet_now = wearpon[switch]
        rt = False
        if Bullet_now == "red":
            Bullet1 = Bullet(self.rect.centerx, self.rect.centery, direction, bullet2_image, 1)
        elif Bullet_now == "yellow":
            Bullet1 = Bullet(self.rect.centerx, self.rect.centery, direction, bullet3_image, 1.5)
        elif Bullet_now == "blue":
            Bullet1 = Bullet(self.rect.centerx, self.rect.centery, direction - 45, bullet1_image, 0.5)
            all_sprites.add(Bullet1)
            bullets.add(Bullet1)
            Bullet1 = Bullet(self.rect.centerx, self.rect.centery, direction, bullet1_image, 0.5)
            all_sprites.add(Bullet1)
            bullets.add(Bullet1)
            Bullet1 = Bullet(self.rect.centerx, self.rect.centery, direction + 45, bullet1_image, 0.5)
        else:
            rt = True
        if rt is False:
            shoot.play()
            all_sprites.add(Bullet1)
            bullets.add(Bullet1)

    def open(self):
        global current_room
        if room_enemy_status[current_room]:
            return
        if current_room in list(MAP_LAYOUT["box"].keys()):
            box_loot(MAP_LAYOUT["box"][current_room])

    def inventory(self, cell):
        print(cell)


def box_loot(type):
    global Bullet_now
    if type == "red":
        wearpon[switch] = "red"
    elif type == "yellow":
        wearpon[switch] = "yellow"
    elif type == "blue":
        wearpon[switch] = "blue"


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image, damage):
        super().__init__()
        self.damage = damage
        self.direction = direction
        image = pygame.transform.rotate(image, self.direction)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = direction

    def update(self):
        self.rect.x += self.speed * round(math.cos(self.direction * 3.14 / 180))
        self.rect.y += self.speed * round(math.sin(self.direction * 3.14 / 180)) * -1
        if (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = random.choice([enemy1_image, enemy2_image, enemy3_image])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.is_moving = True
        self.stop_timer = 0
        self.stop_duration = 120  # 1 секунда в FPS
        self.next_stop_time = random.randint(100, 200)  # 100-200 кадров до остановки
        self.health = 7  # Здоровье врага

    def update(self):
        if self.stop_timer > 0:
            self.stop_timer -= 1
            self.avoid_bullets(bullet_counter)
            return  # Если таймер остановки активен, не двигаться

        # Проверка на уклонение от пуль
        self.avoid_bullets(bullet_counter)

        # Простая логика ИИ: враг преследует игрока
        if player.rect.x > self.rect.x:
            self.rect.x += self.speed
        elif player.rect.x < self.rect.x:
            self.rect.x -= self.speed

        if player.rect.y > self.rect.y:
            self.rect.y += self.speed
        elif player.rect.y < self.rect.y:
            self.rect.y -= self.speed

        # Проверка времени для остановки
        self.next_stop_time -= 1
        if self.next_stop_time <= 0:
            self.stop_timer = self.stop_duration
            self.next_stop_time = random.randint(100, 200)  # Сброс таймера

        # Не выходить за границы комнаты
        self.rect.x = max(0, min(self.rect.x, ROOM_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ROOM_HEIGHT - self.rect.height))

    def avoid_bullets(self, bullet_counter):
        global bullet_damage
        for bullet in bullets:
            bullet_counter += 1
            if bullet_counter % 7 == 0 and self.rect.colliderect(bullet.rect):
                # Уклоняемся от пули
                if bullet.direction == 180:
                    # Уходим вниз или вверх
                    if random.random() < 4:
                        self.rect.y += self.speed * 4  # Уходим вниз
                    else:
                        self.rect.y -= self.speed * 4  # Уходим вверх
                elif bullet.direction == 0:
                    # Уходим вниз или вверх
                    if random.random() < 4:
                        self.rect.y += self.speed * 4  # Уходим вниз
                    else:
                        self.rect.y -= self.speed * 4  # Уходим вверх
                elif bullet.direction == 90:
                    # Уходим влево или вправо
                    if random.random() < 4:
                        self.rect.x -= self.speed * 4  # Уходим влево
                    else:
                        self.rect.x += self.speed * 4  # Уходим вправо
                elif bullet.direction == 270:
                    # Уходим влево или вправо
                    if random.random() < 4:
                        self.rect.x -= self.speed * 4  # Уходим влево
                    else:
                        self.rect.x += self.speed * 4  # Уходим вправо
                return True
            if self.rect.colliderect(bullet.rect):
                self.health -= bullet.damage  # Уменьшаем здоровье врага при попадании
                bullet.kill()  # Уничтожаем пулю
                if self.health <= 0:
                    global kill_count  # Добавьте эту строку
                    kill_count += 1  # Увеличиваем счетчик убитых врагов
                    self.kill()  # Уничтожаем врага, если здоровье равно нулю
                return True
        return False


class Boss(pygame.sprite.Sprite):
    def __init__(self, room):
        super().__init__()
        self.image = boss_image
        self.rect = self.image.get_rect()
        self.room = room
        self.rect.x = 300
        self.rect.y = 300
        self.speed = 4
        self.is_moving = True
        self.stop_timer = 0
        self.stop_duration = 120
        self.next_stop_time = random.randint(100, 200)  # 100-200 кадров до остановки
        self.health = 150
        self.last_shot_time = pygame.time.get_ticks()  # Время последнего выстрела
        self.shoot_interval = 3000  # Интервал между выстрелами (3 секунды)

    def update(self):
        if self.stop_timer > 0:
            self.stop_timer -= 1
            return  # Если таймер остановки активен, не двигаться

        # Простая логика ИИ: враг преследует игрока
        if player.rect.x > self.rect.x:
            self.rect.x += self.speed
        elif player.rect.x < self.rect.x:
            self.rect.x -= self.speed

        if player.rect.y > self.rect.y:
            self.rect.y += self.speed
        elif player.rect.y < self.rect.y:
            self.rect.y -= self.speed

        # Проверка времени для остановки
        self.next_stop_time -= 1
        if self.next_stop_time <= 0:
            self.stop_timer = self.stop_duration
            self.next_stop_time = random.randint(100, 200)  # Сброс таймера

        # Проверка времени для стрельбы
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_interval:
            self.shoot()
            self.last_shot_time = current_time  # Обновляем время последнего выстрела

        # Не выходить за границы комнаты
        self.rect.x = max(0, min(self.rect.x, ROOM_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ROOM_HEIGHT - self.rect.height))

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Уничтожаем босса, если здоровье равно нулю
            victory_screen()  # Вызываем экран победы
    def shoot(self):
        # Стреляем в сторону игрока
        direction = math.degrees(math.atan2(player.rect.centery - self.rect.centery,
                                            player.rect.centerx - self.rect.centerx))
        bullet = BossBullet(self.rect.centerx, self.rect.centery, direction)
        all_sprites.add(bullet)
        boss_bullets.add(bullet)


class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = bullet_image  # Используем изображение пули игрока или создаем новое
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = direction

    def update(self):
        self.rect.x += self.speed * round(math.cos(self.direction * 3.14 / 180))
        self.rect.y += self.speed * round(math.sin(self.direction * 3.14 / 180)) * -1
        if (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()


class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.active = True
        self.image = trap_image2
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_moving = False
        self.health = 10000000000000


# Миникарта
class MiniMap:
    def __init__(self):
        self.size = 150
        self.margin = 10
        self.surface = pygame.Surface((self.size, self.size))

    def draw(self):
        self.surface.fill(BLACK)
        room_size = self.size // 5
        for room, connections in MAP_LAYOUT["rooms"].items():
            x, y = room[1], room[0]
            rect = pygame.Rect(x * room_size, y * room_size, room_size, room_size)
            if room == current_room:
                color = WHITE
            elif room == boss_room:
                color = (255, 0, 0)
            else:
                color = (100, 100, 100)
            pygame.draw.rect(self.surface, color, rect)
        screen.blit(self.surface, (self.margin, self.margin))


class MiniInventory:
    def __init__(self):
        self.size = 150
        self.margin = 10
        self.rect = pygame.Rect((500, 500, 300, 100))
        self.rect1 = pygame.Rect((520, 520, 110, 90))
        self.rect2 = pygame.Rect((660, 520, 110, 90))

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        if switch == 1:
            c2 = (100, 100, 100)
            c1 = (200, 200, 200)
        else:
            c2 = (200, 200, 200)
            c1 = (100, 100, 100)
        pygame.draw.rect(screen, c1, self.rect1)
        pygame.draw.rect(screen, c2, self.rect2)
        i1 = icon[wearpon[1]]
        screen.blit(i1, (450, 485))
        if wearpon[2] != "":
            i2 = icon[wearpon[2]]
            screen.blit(i2, (600, 485))

def check_room_transition():
    global current_room

    if room_enemy_status[current_room]:  # Если враги остались, не позволяем игроку выйти из комнаты
        return

    # Проверяем, если игрок находится в комнате босса
    if current_room == boss_room and len(bosses) > 0:
        return  # Не позволяем игроку выйти из комнаты босса, если босс еще жив

    if player.rect.left <= 5:  # Влево
        new_room = (current_room[0], current_room[1] - 1)
        if new_room in MAP_LAYOUT["rooms"].get(current_room, []):
            current_room = new_room
            player.rect.right = WIDTH - 50
            load_enemies()
            load_boss()
        else:
            player.rect.left = 5

    if player.rect.right >= WIDTH - 5:  # Вправо
        new_room = (current_room[0], current_room[1] + 1)
        if new_room in MAP_LAYOUT["rooms"].get(current_room, []):
            current_room = new_room
            player.rect.left = 50
            load_enemies()
            load_boss()
        else:
            player.rect.right = WIDTH - 5

    if player.rect.top <= 5:  # Вверх
        new_room = (current_room[0] - 1, current_room[1])
        if new_room in MAP_LAYOUT["rooms"].get(current_room, []):
            current_room = new_room
            player.rect.bottom = HEIGHT - 50
            load_enemies()
            load_boss()
        else:
            player.rect.top = 5

    if player.rect.bottom >= HEIGHT - 5:  # Вниз
        new_room = (current_room[0] + 1, current_room[1])
        if new_room in MAP_LAYOUT["rooms"].get(current_room, []):
            current_room = new_room
            player.rect.top = 50
            load_enemies()
            load_boss()
        else:
            player.rect.bottom = HEIGHT - 5



boss_room = random.choice(list(MAP_LAYOUT["rooms"].keys()))


# Загрузка врагов в комнате

def load_enemies():
    global enemies
    enemies.empty()
    if room_enemy_status[current_room] and current_room != boss_room:  # Проверка, были ли враги убиты
        for _ in range(3):  # Три врага на комнату
            x = random.randint(50, ROOM_WIDTH - 50)
            y = random.randint(50, ROOM_HEIGHT - 50)
            enemy = Enemy(x, y)
            all_sprites.add(enemy)
            enemies.add(enemy)
    else:
        # Если враги уже были убиты, просто оставляем enemies пустым
        pass


def load_boss():
    if current_room == boss_room and len(bosses) == 0:  # Проверка, чтобы не создавать нескольких боссов
        boss = Boss(boss_room)
        all_sprites.add(boss)
        bosses.add(boss)


def load_traps():
    global traps
    traps.empty()
    pattern = random.choice(list(wall_patterns.keys()))
    length = len(wall_patterns[pattern])
    for i in range(length):
        x = wall_patterns[pattern][i][0]
        y = wall_patterns[pattern][i][1]
        trap = Trap(x, y)
        all_sprites.add(trap)
        traps.add(trap)


boss_bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
traps = pygame.sprite.Group()
bosses = pygame.sprite.Group()
load_enemies()
load_traps()
load_boss()

# Миникарта
mini_map = MiniMap()
mini_inventory = MiniInventory()

# Переменная для подсчета пуль
bullet_counter = 0

# Установка таймера для удара врага
last_hit_time = pygame.time.get_ticks()


def draw_with_camera_offset():
    camera_offset = (WIDTH // 2 - player.rect.centerx, HEIGHT // 2 - player.rect.centery)

    # Отрисовка комнаты (фон)
    screen.blit(room_texture, camera_offset)
    if current_room in MAP_LAYOUT["box"].keys():
        screen.blit(BOX[MAP_LAYOUT["box"][current_room]],
                    (WIDTH // 2 + camera_offset[0] - 15, HEIGHT // 2 + camera_offset[1] - 15))

    # Отрисовка всех спрайтов с учетом смещения камеры
    for sprite in all_sprites:
        offset_rect = sprite.rect.move(camera_offset)
        screen.blit(sprite.image, offset_rect)

    # Отрисовка миникарты поверх
    mini_map.draw()
    mini_inventory.draw()


pygame.mixer.music.play()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["MOVEMENT: WASD",
                  "LOOT CHESTS: E",
                  "SHOOT: ARROW KEYS",
                  "",
                  "PRESS SPACE TO START",
                  "",
                  "GOOD LUCK!"]

    fon = pygame.transform.scale(backgr, (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(score):
    global MAP_LAYOUT
    global start_point, boss_room, rooms

    intro_text = [
        "OH NO! LOOKS LIKE YOU HAVE",
        "BEEN DEFEATED!",
        "",
        f"YOUR SCORE: {kill_count}",
        "",
        "PRESS ESC TO EXIT",
        "PRESS R TO RESTART"
    ]

    fon = pygame.transform.scale(defeat, (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 350
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player.health = 10
                    main()  # Выход из игры по ESC
                elif event.key == pygame.K_r:
                    player.health = 10
                    return  # Вернуться в основной цикл (вызов main())

        pygame.display.flip()
        clock.tick(FPS)


def victory_screen():
    intro_text = [
        "CONGRATULATIONS!",
        "YOU HAVE DEFEATED THE BOSS!",
        "",
        f"YOUR SCORE: {kill_count}",
        "",
        "PRESS ESC TO EXIT"
    ]

    fon = pygame.transform.scale(defeat, (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 350
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player.health = 10
                    main()  # Выход из игры по ESC

        pygame.display.flip()
        clock.tick(FPS)


def main():
    global SCORE, kill_count
    global last_hit_time  # Declare last_hit_time as global
    SCORE = 0
    kill_count = 0
    last_hit_time = pygame.time.get_ticks()  # Initialize last_hit_time
    start_screen()
    global switch
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.shoot(180)
                elif event.key == pygame.K_RIGHT:
                    player.shoot(0)
                elif event.key == pygame.K_UP:
                    player.shoot(90)
                elif event.key == pygame.K_DOWN:
                    player.shoot(270)
                elif event.key == pygame.K_e:
                    player.open()
                elif event.key == pygame.K_1:
                    switch = 1
                elif event.key == pygame.K_2:
                    switch = 2

        boss_bullets.update()  # Обновляем пули босса

        # Проверка столкновения пуль босса с игроком
        for bullet in boss_bullets:
            if player.rect.colliderect(bullet.rect):
                player.health -= 1  # Уменьшаем здоровье игрока
                bullet.kill()  # Уничтожаем пулю
                # Проверка столкновения пуль игрока с боссом
        for bullet in bullets:
            if len(bosses) > 0:  # Проверяем, есть ли босс
                for boss in bosses:
                    if boss.rect.colliderect(bullet.rect):
                        boss.take_damage(bullet.damage)  # Уменьшаем здоровье босса
                        bullet.kill()  # Уничтожаем пулю

        keys = pygame.key.get_pressed()
        player.update(keys)
        bullets.update()
        enemies.update()
        bosses.update()
        check_room_transition()

        # Проверка на столкновение игрока с врагами
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                current_time = pygame.time.get_ticks()
                if current_time - last_hit_time > 2000:  # Каждые 2 секунды
                    player.health -= 1
                    last_hit_time = current_time
                    damage_taken.play()
                    if player.health <= 0:
                        end_screen(0)
        for enemy in traps:
            if player.rect.colliderect(enemy.rect):
                current_time = pygame.time.get_ticks()
                if current_time - last_hit_time > 2000:
                    player.health -= 1
                    last_hit_time = current_time
                    damage_taken.play()
                    if player.health <= 0:
                        end_screen(0)

        if player.health <= 1:  # Проверка на здоровье игрока
            end_screen(0)

        # Проверка, все ли враги убиты в комнате
        if len(enemies) == 0:
            room_enemy_status[current_room] = False  # Устанавливаем статус комнаты как "враги убиты"

        # Отрисовка
        mini_map.draw()
        all_sprites.draw(screen)
        screen.fill(BLACK)
        draw_with_camera_offset()

        # Отображение полосы здоровья игрока
        health_bar_length = 200
        health_bar_height = 20
        pygame.draw.rect(screen, RED, (10, HEIGHT - 30, health_bar_length, health_bar_height))
        pygame.draw.rect(screen, WHITE, (10, HEIGHT - 30, health_bar_length * (player.health / 5), health_bar_height))

        pygame.display.flip()


if __name__ == "__main__":
    while True:
        main()

pygame.quit()
sys.exit()