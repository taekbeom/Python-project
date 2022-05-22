import pygame

from block import Block
from character import Character
from camera import SpritesCameraGroup
from ui import UI
from enemy import Enemy
from npc import NPC, Questobject


class Build:
    def __init__(self):
        # surface
        self.screen = pygame.display.get_surface()
        self.size = 64

        # sprites group
        self.all_sprites = SpritesCameraGroup()
        self.object_sprites = pygame.sprite.Group()

        self.attack_sprites = pygame.sprite.Group()
        self.can_attack_sprites = pygame.sprite.Group()

        self.quest_sprites = pygame.sprite.Group()

        self.map_build()

        self.ui = UI(self.quest_sprites)

    def map_build(self):
        for i in range(15):
            x = i * self.size
            Block(x, 0, [self.all_sprites, self.object_sprites])
        self.player = Character(self.screen.get_size()[0] // 2, self.screen.get_size()[1] // 2,
                                [self.all_sprites], self.object_sprites, self.all_sprites, self.attack_sprites)
        Enemy((100, 200), [self.all_sprites, self.can_attack_sprites], self.object_sprites)
        NPC((800, 500), [self.all_sprites, self.object_sprites], self.all_sprites, 'apple1', '', 'npc1')
        NPC((500, 500), [self.all_sprites, self.object_sprites], self.all_sprites, 'apple2', '', 'npc2')
        Questobject('graphics/apple.png', 'apple1', [self.quest_sprites])
        Questobject('graphics/apple.png', 'apple2', [self.quest_sprites])

    def player_attack(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.can_attack_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite)

    def start(self):
        self.all_sprites.sprite_build(self.player)
        self.all_sprites.update()
        self.all_sprites.enemy_update(self.player)
        self.player_attack()
        self.ui.display(self.player)
