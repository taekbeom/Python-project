import pygame
import math


class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups, image, all_sprites, quest_type, quest_target, quest_target_type, quest_npc, id, name):
        super().__init__(groups)
        # display
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center=pos)
        self.final_rect = self.rect.copy()
        self.sprite_type = 'npc'
        self.id = id
        self.name = name
        self.quest_target = quest_target
        self.quest_target_type = quest_target_type

        # dialogue icon
        emblem_pos = (pos[0], pos[1] - 28)
        self.emblem = Emblem(emblem_pos, all_sprites)

        # for collisions
        self.overlap_pos = self.rect.inflate(0, -5)

        # for interaction
        self.notice_rad = 250
        self.talk_rad = 80

        # for quests
        self.has_quest = True
        self.quest_type = quest_type
        self.quest_npc = quest_npc
        self.npc_next = False
        self.quest_complete = False

    def get_player(self, player, distance):
        player.distances[self.id] = distance

        self.check_quest_completion(player, distance)
        if not self.quest_complete:
            self.check_quests(player)

        if self.has_quest and player.get_item and self.npc_next:
            player.quest_list.append(self.quest_type)
            player.quest_book.append((self.id, self.name + ': Give ' + self.quest_npc + ' ' + self.quest_type))
            self.has_quest = False
            self.npc_next = False
        elif distance <= self.talk_rad and player.start_dialogue:
            if self.quest_target_type in player.quest_list:
                player.npc_status = 'give'
                player.current_npc = self.quest_target_type
            elif self.has_quest and player.npc_status != 'complete':
                player.target_npc = self.quest_npc
                player.current_npc = self.quest_type
                player.npc_status = 'quest'
            elif player.npc_status != 'complete' and not self.has_quest:
                player.current_npc = self.quest_type
                player.npc_status = 'talk'
            player.can_move = False
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

    def check_quests(self, player):
        if player.quests[self.id]:
            self.quest_complete = True

    def check_quest_completion(self, player, distance):
        if distance <= self.talk_rad and self.quest_target_type in player.quest_list and player.get_item:
            player.quest_list.remove(self.quest_target_type)
            player.quests[self.quest_target] = True
            player.get_item = False
            player.current_npc = self.quest_target_type
            player.npc_status = 'complete'

    def npc_update(self, player):
        direction_x = player.rect.centerx - self.rect.centerx
        direction_y = player.rect.centery - self.rect.centery
        distance = math.sqrt(direction_x**2 + direction_y**2)
        self.get_player(player, distance)


class Emblem(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/quest.png').convert_alpha()
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center=pos)
        self.final_rect = self.rect.copy()


class Questobject(pygame.sprite.Sprite):
    def __init__(self, quest_type, groups):
        super().__init__(groups)
        self.image = pygame.image.load(f'graphics/{quest_type}.png').convert_alpha()

        self.quest_type = quest_type
