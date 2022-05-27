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

        self.final_rect = pygame.Rect((x + 7, y + 15, 10, 10))
        self.sprite_type = 'player'

        self.overlap_pos = self.final_rect

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
        self.potion_count = 10
        self.health_restored = 10
        self.heal_cd = 5000
        self.heal_time = None
        self.can_use_potion = True
        self.bar_healed_cd = 500

        # stats
        self.hp = 100
        self.atk = 1
        self.weapon_atk = 7
        self.arrow_atk = 2
        self.arrow_speed = 1
        self.exp = 0
        self.lvl = 0
        self.velocity = 4
        self.atk_dmg = None

        self.max_hp = 100

        self.weapon_index = 0

        # for npc interactions
        self.start_dialogue = False
        self.get_item = False
        self.quest_list = []
        self.get_quest = None
        self.quests = []
        for i in range(5):
            self.quests.append(False)
        self.quest_book = []
        self.show_quests = False
        self.quest_cd = 400
        self.quest_time = pygame.time.get_ticks()

        self.npc_release = True
        self.npc_status = 'none'
        self.current_npc = None
        self.target_npc = None
        self.npc_cd = 500
        self.npc_time = None
        self.distances = []
        for i in range(5):
            self.distances.append(100)

        # for attack
        self.get_attacked = False
        self.hit_cd = 700
        self.hit_time = None

        self.chased = False

        self.killed = False

    def movement(self):
        # probably remove this and show during fight when losing hp
        self.bar_show = False
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
            self.velocity = 6
        else:
            self.velocity = 4

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
        # heal potion
        if keys[pygame.K_e] and self.can_use_potion:
            self.heal_time = pygame.time.get_ticks()
            self.use_potion()
        # talking to npc
        if keys[pygame.K_f] and not self.npc_status == 'complete':
            if not self.chased:
                for distance in self.distances:
                    if distance <= 80:
                        self.start_dialogue = True
        elif keys[pygame.K_RETURN] and self.start_dialogue:
            self.get_item = True
            self.start_dialogue = False
            self.can_move = True
            if self.npc_status != 'complete':
                self.npc_status = 'none'
            self.npc_time = pygame.time.get_ticks()
        elif keys[pygame.K_RETURN] and self.npc_status == 'complete':
            current_time = pygame.time.get_ticks()
            if current_time - self.npc_time >= self.npc_cd:
                self.can_move = True
                self.npc_status = 'none'

        if keys[pygame.K_q]:
            current_time = pygame.time.get_ticks()
            if not self.show_quests and current_time - self.quest_time >= self.quest_cd:
                self.quest_time = pygame.time.get_ticks()
                self.show_quests = True
                self.can_move = False
            elif self.show_quests and current_time - self.quest_time >= self.quest_cd:
                self.quest_time = pygame.time.get_ticks()
                self.show_quests = False
                self.can_move = True

    def animations(self):
        if self.get_attacked:
            self.bar_show = True
            alpha = self.flicker()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def full_atk(self):
        if self.weapon_index == 0:
            attack = self.weapon_atk
        else:
            attack = self.arrow_atk * self.arrow_speed
        self.atk_dmg = attack + self.atk

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
        self.sword.final_rect = self.rect.copy()

    def delete_sword(self):
        if self.sword:
            self.can_move = True
            self.sword.kill()
        self.sword = None

    def create_arrow(self):
        Projectile(self.rect.center, self.object_sprites, [self.all_sprites, self.attack_sprites])

    def use_potion(self):
        if self.potion_count and self.can_use_potion:
            self.can_use_potion = False
            self.hp = min(self.hp + self.health_restored, self.max_hp)
            self.potion_count -= 1

    def cooldown(self):
        current_time = pygame.time.get_ticks()

        if self.use_weapon:
            if current_time - self.atk_time >= self.atk_cd:
                self.delete_sword()
                self.use_weapon = False

        if self.get_attacked:
            if current_time - self.hit_time >= self.hit_cd:
                self.get_attacked = False

        if not self.can_use_potion:
            if current_time - self.heal_time >= self.heal_cd:
                self.can_use_potion = True
            elif current_time - self.heal_time <= self.bar_healed_cd:
                self.bar_show = True

    def check_quest(self):
        if self.get_quest:
            self.quest_list.append(self.get_quest)
            self.get_quest = None

    def check_health(self):
        if self.hp <= 0:
            settings.pause_mode = True
            self.killed = True

    def check_lvl(self):
        if self.exp >= 100:
            self.exp -= 100
            self.lvl += 1
            self.atk += 1

    def update(self):
        if not settings.pause_mode:
            if self.bar_show:
                self.show_hp_bar(self.rect.centerx, self.rect.centery, self.hp,
                                 self.rect.centerx, self.rect.centery, 'green')
            self.movement()
            self.direction_move(self.velocity)
            self.animations()
            self.cooldown()
            self.check_health()
            self.check_lvl()
