import pygame
import math


class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups, all_sprites):
        super().__init__(groups)
        # display
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=pos)
        self.sprite_type = 'npc'

        # dialogue icon
        emblem_pos = (pos[0], pos[1] - 40)
        self.emblem = Emblem(emblem_pos, all_sprites)

        # for collisions
        self.overlap_pos = self.rect.inflate(0, -5)

        # for interaction
        self.notice_rad = 250
        self.has_quest = True

    def get_player(self, player):
        direction_x = player.rect.centerx - self.rect.centerx
        direction_y = player.rect.centery - self.rect.centery
        distance = math.sqrt(direction_x**2 + direction_y**2)

        if distance <= self.notice_rad and not player.start_dialogue:
            self.emblem.image = pygame.image.load('graphics/dialogue.png').convert_alpha()
        else:
            self.emblem.image = pygame.Surface((20, 20))
            self.emblem.image.set_alpha(0)

    def npc_update(self, player):
        self.get_player(player)


class Emblem(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((20, 20))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center=pos)
