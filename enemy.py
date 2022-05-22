import pygame

import settings
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
        self.velocity = 2
        self.atk = 3
        self.knock_back = 1
        self.fight_rad = 64

        # for appearing
        self.notice_rad = 500
        self.trigger_rad = 200
        self.visible = False

        # for interaction
        self.can_attack = True
        self.atk_cd = 600
        self.atk_time = None

        # for attack
        self.get_attacked = False
        self.hit_cd = 700
        self.hit_time = None

    def animations(self):
        if self.get_attacked:
            alpha = self.flicker()
            self.image.set_alpha(alpha)
        elif self.visible:
            self.image.set_alpha(255)

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
                self.set_invisible()
                self.visible = False
                self.status = 'idle'

    def action(self, player):
        if self.status == 'attack':
            self.damage_player(player)
            self.atk_time = pygame.time.get_ticks()
            # move to frame section
            self.can_attack = False
            player.chased = True
        elif self.status == 'move':
            player.chased = True
            self.direction_x = self.get_player_distance(player.rect.centerx, player.rect.centery)[1]
            self.direction_y = self.get_player_distance(player.rect.centerx, player.rect.centery)[2]
        else:
            self.direction_x = 0
            self.direction_y = 0
            player.chased = False
            self.rect.center = self.position_return
            self.set_invisible()

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.atk_time >= self.atk_cd:
                self.can_attack = True

        if self.get_attacked:
            if current_time - self.hit_time >= self.hit_cd:
                self.get_attacked = False

    def get_damage(self, player, attack_sprite):
        if not self.get_attacked and self.visible:
            self.direction_x = self.get_player_distance(player.rect.centerx, player.rect.centery)[1]
            self.direction_y = self.get_player_distance(player.rect.centerx, player.rect.centery)[2]

            if attack_sprite.sprite_type == 'projectile':
                attack_sprite.kill()

            self.hp = max(self.hp - player.atk, 0)

            self.hit_time = pygame.time.get_ticks()
            self.get_attacked = True

    def check_health(self, player):
        if self.hp <= 0:
            player.chased = False
            self.kill()

    def hit_react(self):
        if self.get_attacked:
            self.direction_x *= - self.knock_back
            self.direction_y *= - self.knock_back

    def damage_player(self, player):
        if not player.get_attacked:
            player.hp = max(player.hp - self.atk, 0)
            player.get_attacked = True
            player.hit_time = pygame.time.get_ticks()

    def set_invisible(self):
        if not self.visible:
            self.image.set_alpha(0)

    def update(self):
        if not settings.pause_mode:
            self.hit_react()
            self.direction_move(self.velocity)
            self.animations()
            self.cooldown()

    def enemy_update(self, player):
        self.get_player(player)
        self.action(player)
        self.check_health(player)
