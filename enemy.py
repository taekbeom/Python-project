import pygame
from entity import Entity
import math


class Enemy(Entity):
    def __init__(self, pos, groups, object_sprites):
        super().__init__(groups)
        # for map
        self.sprite_type = 'enemy'

        # display
        self.image = pygame.Surface((40, 40))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center=pos)
        self.position_return = pos

        # for movement
        self.overlap_pos = self.rect.inflate(0, -10)
        self.object_sprites = object_sprites
        self.status = ''

        # stats
        self.hp = 50
        self.velocity = 4
        self.atk = 3
        self.knock_back = 2
        self.fight_rad = 64

        # for appearing
        self.notice_rad = 300
        self.trigger_rad = 200
        self.visible = False

        # for interaction
        self.can_attack = True
        self.atk_cd = 400
        self.atk_time = None

    def get_player_distance(self, pos_x, pos_y):
        direction_x = pos_x - self.rect.centerx
        direction_y = pos_y - self.rect.centery
        distance = math.sqrt(direction_x**2 + direction_y**2)

        if distance == 0:
            return 0, 0, 0

        if direction_x != 0:
            if direction_x > 0:
                direction_x = 1
            else:
                direction_x = -1
        if direction_y != 0:
            if direction_y > 0:
                direction_y = 1
            else:
                direction_y = -1

        return distance, direction_x, direction_y

    def get_player(self, player):
        distance = self.get_player_distance(player.rect.centerx, player.rect.centery)[0]
        if not self.visible and distance <= self.trigger_rad:
            self.status = 'appear'
            self.image.set_alpha(255)
            self.visible = True
        if self.visible:
            if distance <= self.fight_rad and self.can_attack:
                self.status = 'attack'
            elif distance <= self.notice_rad:
                self.status = 'move'
            else:
                self.image.set_alpha(0)
                self.visible = False
                self.status = 'idle'

    def action(self, player):
        if self.status == 'attack':
            print(self.status)
            self.atk_time = pygame.time.get_ticks()
            # move to frame section
            self.can_attack = False
        elif self.status == 'move':
            self.direction_x = self.get_player_distance(player.rect.centerx, player.rect.centery)[1]
            self.direction_y = self.get_player_distance(player.rect.centerx, player.rect.centery)[2]
        else:
            self.direction_x = 0
            self.direction_y = 0
            self.rect.center = self.position_return

    def cooldown(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.atk_time >= self.atk_cd:
                self.can_attack = True

    def update(self):
        self.direction_move(self.velocity)
        self.cooldown()

    def enemy_update(self, player):
        self.get_player(player)
        self.action(player)
