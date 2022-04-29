import pygame
from block import Block
from character import Character
from camera import SpritesCameraGroup


class Build:
    def __init__(self):
        # surface
        self.screen = pygame.display.get_surface()
        self.size = 64

        # sprites group
        self.all_sprites = SpritesCameraGroup()
        self.object_sprites = pygame.sprite.Group()

        self.map_build()

    def map_build(self):
        for i in range(15):
            x = i * self.size
            Block(x, 0, [self.all_sprites, self.object_sprites])
        self.player = Character(self.screen.get_size()[0] // 2, self.screen.get_size()[1] // 2,
                                [self.all_sprites], self.object_sprites, self.all_sprites)

    def start(self):
        self.all_sprites.sprite_build(self.player)
        self.all_sprites.update()

