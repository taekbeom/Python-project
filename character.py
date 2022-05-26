import pygame
import math

import settings
from weapon import Sword, Projectile
from entity import Entity
from npc import Questobject


class Character(Entity):
    def __init__(self, x, y, groups, object_sprites, all_sprites, attack_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/char_sprite2.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.overlap_pos = self.rect.inflate(-10, -36)

        self.object_sprites = object_sprites
        self.all_sprites = all_sprites
        self.attack_sprites = attack_sprites

        # delete later
        self.status = ""

        # later for bow
        self.can_move = True
        self.switch_weapon = True
        self.time_switch_weapon = pygame.time.get_ticks()

        self.use_weapon = False
        self.atk_cd = 700
        self.atk_time = None
        self.button_released = False

        self.sword = None
        # self.bow = Bow(self.rect.center, [self.all_sprites])

        # later for heal potion
        self.exist_potion = True
        self.health_restored = 10

        # stats
        self.hp = 60
        self.atk = 5
        self.money = 100
        self.lvl = 0
        self.velocity = 4

        self.max_hp = 100

        self.weapon_index = 0

        # mb also delete
        self.bar_show = False

        # for npc interactions
        self.start_dialogue = False
        self.get_item = False
        self.quest_list = []
        self.get_quest = None

        # for attack
        self.get_attacked = False
        self.hit_cd = 700
        self.hit_time = None

        self.chased = False

    def movement(self):
        # move to delay method

        # probably remove this and show during fight when losing hp
        self.bar_show = False
        self.running = False
        self.get_item = False

        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction_x = -1
                self.status = "left"
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction_x = 1
                self.status = "right"
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction_y = -1
                self.status = "up"
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction_y = 1
                self.status = "down"
        # create statement for not status

        if keys[pygame.K_LSHIFT]:
            if not self.running:
                self.direction_x *= 1.5
                self.direction_y *= 1.5

        # move to attack
        if pygame.mouse.get_pressed()[0] and not self.use_weapon:
            self.can_move = False
            self.use_weapon = True
            self.atk_time = pygame.time.get_ticks()
            self.weapon_index = 0
            self.create_sword()
            # sword
        elif pygame.mouse.get_pressed()[2] and not self.use_weapon:
            self.can_move = False
            self.use_weapon = True
            self.atk_time = pygame.time.get_ticks()
            self.weapon_index = 1
            self.button_released = True
            # bow
        if settings.mouse_button_up and self.button_released:
            self.can_move = True
            self.create_arrow()
            settings.mouse_button_up = False
            self.button_released = False
        # talking to npc
        if keys[pygame.K_f]:
            if not self.chased:
                self.start_dialogue = True
                self.can_move = False
                # show dialogue
        elif keys[pygame.K_RETURN] and self.start_dialogue:
            self.get_item = True
            self.start_dialogue = False
            self.can_move = True

        # heal potion
        if keys[pygame.K_e]:
            self.use_potion()

    def animations(self):
        if self.get_attacked:
            self.bar_show = True
            alpha = self.flicker()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def create_sword(self):
        self.sword = Sword(self.rect.center, [self.all_sprites, self.attack_sprites])
        if self.status == "right":
            self.sword.image = pygame.Surface((50, 10))
            self.sword.rect = self.sword.image.get_rect(midleft=self.rect.midright)
        elif self.status == "left":
            self.sword.image = pygame.Surface((50, 10))
            self.sword.rect = self.sword.image.get_rect(midright=self.rect.midleft)
        elif self.status == "down":
            self.sword.image = pygame.Surface((10, 50))
            self.sword.rect = self.sword.image.get_rect(midtop=self.rect.midbottom)
        else:
            self.sword.image = pygame.Surface((10, 50))
            self.sword.rect = self.sword.image.get_rect(midbottom=self.rect.midtop)

    def delete_sword(self):
        if self.sword:
            self.can_move = True
            self.sword.kill()
        self.sword = None

    def create_arrow(self):
        Projectile(self.rect.center, self.object_sprites, [self.all_sprites, self.attack_sprites])

    def use_potion(self):
        if self.exist_potion:
            self.hp = min(self.hp + self.health_restored, self.max_hp)
            print(self.hp)

    def cooldown(self):
        current_time = pygame.time.get_ticks()

        if self.use_weapon:
            if current_time - self.atk_time >= self.atk_cd:
                self.delete_sword()
                self.use_weapon = False

        if self.get_attacked:
            if current_time - self.hit_time >= self.hit_cd:
                self.get_attacked = False

    def check_quest(self):
        if self.get_quest:
            self.quest_list.append(self.get_quest)
            self.get_quest = None

    def update(self):
        if not settings.pause_mode:
            self.movement()
            self.direction_move(self.velocity)
            self.animations()
            self.cooldown()
            self.check_quest()
