from load_file import load_image
import pygame

title_size = 500
go_size = 25

title_image = {
    "room": load_image("room.png"),
    "vertical": load_image("vertical.png"),
    "horizontal": load_image("horizontal.png"),
    "start": load_image("room.png"),
    "finish": load_image("room.png"),
}

player_image = load_image("mar.png")


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


tail_sprite = SpriteGroup()
hero_sprite = SpriteGroup()
all_sprite = SpriteGroup()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tail_sprite, all_sprite)
        self.image = title_image[tile_type]
        self.rect = self.image.get_rect().move(
            title_size * pos_x,
            title_size * pos_y
        )


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_sprite, all_sprite)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            go_size * pos_x,
            go_size * pos_y
        )
        self.pos = (pos_x, pos_y)
        print(self.pos)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect.topleft = (
            go_size * self.pos[0],
            go_size * self.pos[1]
        )
