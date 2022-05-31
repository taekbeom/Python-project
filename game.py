import pygame

from block import Block
from character import Character
from camera import SpritesCameraGroup
from suppoty import import_csv_layout, import_folder, import_csv_main
from ui import UI
from enemy import Enemy
from npc import NPC, Questobject


class Build:
    def __init__(self):
        # surface
        self.screen = pygame.display.get_surface()
        self.size = 16

        # sprites group
        self.all_sprites = SpritesCameraGroup()
        self.object_sprites = pygame.sprite.Group()

        self.attack_sprites = pygame.sprite.Group()
        self.can_attack_sprites = pygame.sprite.Group()

        self.quest_sprites = pygame.sprite.Group()

        self.enemy_spawn_points = [[1301, 247], [1215, 415], [1230, 705], [1500, 390], [1650, 766]]

        self.map_build()

        self.ui = UI(self.quest_sprites)

    def map_build(self, name=None):

        types, pathsCSV, pathsgraphics = import_csv_main('graphics/TileMap/CSV/MAINCSV.csv')

        for i in range(46):
            type, pathCSV, pathgraphics = types[i], pathsCSV[i], pathsgraphics[i]
            layout = import_csv_layout(pathCSV)
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * self.size
                        y = row_index * self.size
                        if type == 'boundary':
                            Block((x, y), [self.object_sprites], 'invisible')
                        else:
                            surf = import_folder(pathgraphics, col)
                            Block((x, y), [self.all_sprites, self.object_sprites], type, surf)

        #        Block(x, 0, [self.all_sprites, self.object_sprites])

        # self.player = Character(self.screen.get_size()[0] // 2, self.screen.get_size()[1] // 2,
        #                         [self.all_sprites], self.object_sprites, self.all_sprites, self.attack_sprites)

        self.player = Character(384, 290, [self.all_sprites], self.object_sprites, self.all_sprites,
                                self.attack_sprites)

        for i in range(len(self.enemy_spawn_points)):
            x, y = self.enemy_spawn_points[i]
            Enemy((x, y), [self.all_sprites, self.can_attack_sprites], self.object_sprites)
        NPC((800, 500), [self.all_sprites, self.object_sprites], 'graphics/pesosus_greenov.png', self.all_sprites,
            'apple', 1, 'string', 'npc5', 0, 'npc1')
        NPC((550, 540), [self.all_sprites, self.object_sprites], 'graphics/pesosus_greenov.png', self.all_sprites,
            'string', 3, 'snake', 'npc1', 1, 'npc2')
        NPC((1070, 710), [self.all_sprites, self.object_sprites], 'graphics/pesosus_greenov.png', self.all_sprites,
            'melon', 4, 'pen', 'npc4', 2, 'npc3')
        NPC((1000, 900), [self.all_sprites, self.object_sprites], 'graphics/pesosus_greenov.png', self.all_sprites,
            'snake', 2, 'melon', 'npc2', 3, 'npc4')
        NPC((380, 880), [self.all_sprites, self.object_sprites], 'graphics/pesosus_greenov.png', self.all_sprites,
            'pen', 0, 'apple', 'npc3', 4, 'npc5')
        Questobject('apple', [self.quest_sprites])
        Questobject('string', [self.quest_sprites])
        Questobject('melon', [self.quest_sprites])
        Questobject('snake', [self.quest_sprites])
        Questobject('pen', [self.quest_sprites])

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
