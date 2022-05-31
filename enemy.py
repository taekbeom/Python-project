import random

import pygame

import settings
from entity import Entity
from suppoty import import_folder_animation
import math


class Enemy(Entity):
    def __init__(self, pos, groups, object_sprites):
        super().__init__(groups)
        # for map
        self.sprite_type = 'enemy'

        # display
        self.image = pygame.Surface((16, 16))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center=pos)
        self.final_rect = self.rect.copy()
        self.position_return = pos

        # animation
        self.animation_keys = {"up": [], "down": [], "left": [], "right": []}
        character_assets_path = "graphics/EnemyAssets/"
        for animation in self.animation_keys.keys():
            path = character_assets_path + animation
            self.animation_keys[animation] = import_folder_animation(path)
        self.animation_speed = 0.3
        self.frame_index = 0

        # for movement
        self.overlap_pos = self.rect.inflate(0, -10)
        self.object_sprites = object_sprites
        self.status = ''

        # stats
        self.hp = 50
        self.velocity = 2
        self.atk = 5
        self.knock_back = 1
        self.fight_rad = self.rect.width

        # for appearing
        self.notice_rad = 400
        self.trigger_rad = 200
        self.visible = False

        # for returning
        self.return_cd = 5000
        self.return_time = None

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
            self.bar_show = True
            alpha = self.flicker()
            self.image.set_alpha(alpha)
        elif self.visible:
            self.bar_show = False
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
        distance_from_start = self.get_player_distance(self.position_return[0], self.position_return[1])[0]
        if distance_from_start >= 400:
            self.visible = False
            self.check_location()
            self.return_time = pygame.time.get_ticks()
        elif self.rect.center == self.position_return and not self.visible and distance <= self.trigger_rad: # and not self.going home
            self.status = 'appear'
            self.image.set_alpha(255)
            self.visible = True
        if self.visible:
            if distance <= self.fight_rad and self.can_attack:
                self.status = 'attack'
            elif distance <= self.notice_rad:
                self.status = 'move'
            else:
                self.visible = False
                self.status = 'idle'

    def action(self, player):
        if self.visible: # and not self.going_home:
            if self.status == 'attack':
                self.check_location()
                self.return_time = pygame.time.get_ticks()
                self.damage_player(player)
                self.atk_time = pygame.time.get_ticks()
                # move to frame section
                self.can_attack = False
                player.chased = True
            elif self.status == 'move':
                self.check_location()
                self.return_time = pygame.time.get_ticks()
                player.chased = True
                self.direction_x = self.get_player_distance(player.rect.centerx, player.rect.centery)[1]
                self.direction_y = self.get_player_distance(player.rect.centerx, player.rect.centery)[2]
        else:
            self.direction_x = self.get_player_distance(self.position_return[0], self.position_return[1])[1]
            self.direction_y = self.get_player_distance(self.position_return[0], self.position_return[1])[2]
            player.chased = False
            self.check_location()

    def animate(self):
        status = ''
        if self.direction_x == 1:
            status = 'right'
        elif self.direction_x == -1:
            status = 'left'
        elif self.direction_y == 1:
            status = 'down'
        elif self.direction_y == -1:
            status = 'up'
        if status not in self.animation_keys: return
        animation = self.animation_keys[status]

        self.frame_index += self.animation_speed
        self.frame_index %= len(animation)

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.overlap_pos.center)

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

            player.full_atk()
            self.hp = max(self.hp - player.atk_dmg, 0)

            self.hit_time = pygame.time.get_ticks()
            self.get_attacked = True

    def check_health(self, player):
        if self.hp <= 0:
            player.chased = False
            player.exp += random.randint(10, 20)
            player.potion_count += 1
            self.kill()

    def hit_react(self):
        if self.get_attacked:
            self.direction_x *= - self.knock_back
            self.direction_y *= - self.knock_back

    def damage_player(self, player):
        if player.get_attacked: return

        player.hp = max(player.hp - self.atk, 0)
        player.get_attacked = True
        player.hit_time = pygame.time.get_ticks()

    def set_invisible(self):
        if not self.visible:
            self.image.set_alpha(0)

    def check_location(self):
        pos_x = self.rect.centerx - self.position_return[0]
        pos_y = self.rect.centery - self.position_return[1]
        distance = self.get_player_distance(self.position_return[0], self.position_return[1])[0]
        # print(pos_x, pos_y, distance)
        if distance <= 3.0 and not self.visible:
            self.set_invisible()
            self.direction_x = 0
            self.direction_y = 0
            if self.rect.center != self.position_return:
                self.rect.center = self.position_return
        elif not self.visible:
            current_time = pygame.time.get_ticks()
            if current_time - self.return_time >= self.return_cd:
                self.set_invisible()
                self.rect.center = self.position_return
                self.direction_x = 0
                self.direction_y = 0

    def update(self):
        if settings.pause_mode: return

        self.hit_react()
        self.direction_move(self.velocity)
        self.animations()
        self.cooldown()

    def enemy_update(self, player):
        if self.bar_show:
            self.show_hp_bar(self.rect.centerx, self.rect.centery, self.hp,
                             player.rect.centerx, player.rect.centery, 'red')
        self.get_player(player)
        self.action(player)
        self.animate()
        self.check_health(player)
