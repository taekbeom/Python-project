import pygame
import math

import settings
from weapon import Sword, Bow, Projectile
from entity import Entity


class Character(Entity):
    def __init__(self, x, y, groups, object_sprites, all_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/char_sprite.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.overlap_pos = self.rect.inflate(0, -10)

        self.object_sprites = object_sprites
        self.all_sprites = all_sprites

        # delete later
        self.status = ""

        # later for bow
        self.switch_weapon = True
        self.time_switch_weapon = pygame.time.get_ticks()

        self.use_weapon = False
        self.atk_cd = 300
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
        self.velocity = 5

        self.max_hp = 100

        self.weapon_index = 0

        # mb also delete
        self.bar_show = False

        # for npc interactions
        self.start_dialogue = False

    def movement(self):
        # move to delay method
        self.delete_sword()

        # probably remove this and show during fight when losing hp
        self.bar_show = False

        keys = pygame.key.get_pressed()

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
            self.direction_x /= 2
            self.direction_y /= 2

        # move to attack
        if pygame.mouse.get_pressed()[0] and not self.use_weapon:
            self.use_weapon = True
            self.atk_time = pygame.time.get_ticks()
            self.weapon_index = 0
            self.create_sword()
            # sword
        elif pygame.mouse.get_pressed()[2] and not self.use_weapon:
            self.use_weapon = True
            self.atk_time = pygame.time.get_ticks()
            self.weapon_index = 1
            self.create_bow()
            self.button_released = True
            # bow
        if settings.mouse_button_up and self.button_released:
            self.create_arrow()
            settings.mouse_button_up = False
            self.button_released = False
        # talking to npc
        if keys[pygame.K_f]:
            if not self.start_dialogue:
                self.start_dialogue = True
                # show dialogue
        elif keys[pygame.K_RETURN]:
            self.start_dialogue = False

        # heal potion
        if keys[pygame.K_e]:
            self.use_potion()

        # move to menu
        if keys[pygame.K_ESCAPE]:
            pass
            # menu pops up

        if keys[pygame.K_SPACE]:
            self.bar_show = True

    def create_sword(self):
        self.sword = Sword(self.rect.center, [self.all_sprites])
        if self.status == "right":
            self.sword.rect = self.sword.image.get_rect(midleft=self.rect.midright)
        elif self.status == "left":
            self.sword.rect = self.sword.image.get_rect(midright=self.rect.midleft)
        elif self.status == "down":
            self.sword.rect = self.sword.image.get_rect(midtop=self.rect.midbottom)
        else:
            self.sword.rect = self.sword.image.get_rect(midbottom=self.rect.midtop)

    def delete_sword(self):
        if self.sword:
            self.sword.kill()
        self.sword = None

    def create_bow(self):
        pass

    def create_arrow(self):
        Projectile(self.rect.center, self.object_sprites, self.all_sprites)

    def use_potion(self):
        if self.exist_potion:
            self.hp = min(self.hp + self.health_restored, self.max_hp)
            print(self.hp)

    def cooldown(self):
        if self.use_weapon:
            current_time = pygame.time.get_ticks()
            if current_time - self.atk_time >= self.atk_cd:
                self.use_weapon = False

    def update(self):
        self.movement()
        self.direction_move(self.velocity)
        self.cooldown()
