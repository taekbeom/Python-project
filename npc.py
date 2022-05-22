import pygame
import math


class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups, all_sprites, quest_type, quest_text, name):
        super().__init__(groups)
        # display
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=pos)
        self.sprite_type = 'npc'
        self.name = name

        # dialogue icon
        emblem_pos = (pos[0], pos[1] - 40)
        self.emblem = Emblem(emblem_pos, all_sprites)

        # for collisions
        self.overlap_pos = self.rect.inflate(0, -5)

        # for interaction
        self.notice_rad = 250
        self.talk_rad = 60

        # for quests
        self.has_quest = True
        self.quest_type = quest_type
        self.quest_text = quest_text
        self.npc_next = False
        self.quest_complete = False

    def get_player(self, player):
        direction_x = player.rect.centerx - self.rect.centerx
        direction_y = player.rect.centery - self.rect.centery
        distance = math.sqrt(direction_x**2 + direction_y**2)

        if distance <= self.talk_rad and 'apple1' in player.quest_list \
                and self.name == 'npc2' and player.start_dialogue:
            player.quest_list.remove('apple1')
            self.quest_complete = True
        elif self.has_quest and player.get_item and self.npc_next:
            # print('has quest')
            player.get_quest = self.quest_type
            self.has_quest = False
            self.npc_next = False
        else:
            pass
            # print('no quest')
        if distance <= self.talk_rad and player.start_dialogue:
            self.npc_next = True
            self.emblem.image.set_alpha(0)
        elif distance <= self.notice_rad:
            if self.has_quest:
                self.emblem.image = pygame.image.load('graphics/quest.png').convert_alpha()
            elif self.quest_complete:
                self.emblem.image = pygame.image.load('graphics/complete.png').convert_alpha()
            else:
                self.emblem.image = pygame.image.load('graphics/dialogue.png').convert_alpha()
        else:
            self.emblem.image.set_alpha(0)

    def npc_update(self, player):
        self.get_player(player)


class Emblem(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/quest.png').convert_alpha()
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center=pos)


class Questobject(pygame.sprite.Sprite):
    def __init__(self, image, quest_type, groups):
        super().__init__(groups)
        self.image = pygame.image.load(image).convert_alpha()

        self.quest_type = quest_type
