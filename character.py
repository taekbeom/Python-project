import pygame
import math
from weapon import Sword, Bow


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, groups, object_sprites, all_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/char_sprite.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.overlap_pos = self.rect.inflate(0, -30)

        self.velocity = 5

        self.directionX = 0
        self.directionY = 0

        self.object_sprites = object_sprites
        self.all_sprites = all_sprites

        # delete later
        self.status = ""

        # later for bow
        self.switch_weapon = True
        self.time_switch_weapon = pygame.time.get_ticks()

        self.use_weapon = False
        self.atk_cd = 500
        self.atk_time = None

        self.sword = None
        # self.bow = Bow(self.rect.center, [self.all_sprites])

        # later for heal potion
        self.exist_potion = True
        self.health_restored = 10

        # stats
        self.hp = 60
        self.atk = 5
        self.money = 100

        self.max_hp = 100

        self.weapon_index = 0

        # mb also delete
        self.bar_show = False

    def movement(self):
        # move to delay method
        self.delete_sword()

        # probably remove this and show during fight when losing hp
        self.bar_show = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.directionX = -1
            self.status = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.directionX = 1
            self.status = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.directionY = -1
            self.status = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.directionY = 1
            self.status = "down"

        if keys[pygame.K_LSHIFT]:
            self.directionX /= 2
            self.directionY /= 2

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
            # bow
        elif keys[pygame.K_f]:
            pass
            # talking to npc

        # heal potion
        if keys[pygame.K_e]:
            self.use_potion()

        # move to menu
        if keys[pygame.K_ESCAPE]:
            pass
            # menu pops up

        if keys[pygame.K_SPACE]:
            self.bar_show = True

        if self.directionX != 0 and self.directionY != 0:
            self.directionX = round(self.directionX * math.sqrt(2) / 2, 1)
            self.directionY = round(self.directionY * math.sqrt(2) / 2, 1)

        self.overlap_pos.x += self.directionX * self.velocity
        self.collision('horizontal')
        self.overlap_pos.y += self.directionY * self.velocity
        self.collision('vertical')
        self.rect = self.overlap_pos

        self.directionX = 0
        self.directionY = 0

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

    def use_potion(self):
        if self.exist_potion:
            self.hp = min(self.hp + self.health_restored, self.max_hp)
            print(self.hp)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.use_weapon:
            if current_time - self.atk_time >= self.atk_cd:
                self.use_weapon = False

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.object_sprites:
                if sprite.overlap_pos.colliderect(self.overlap_pos):
                    if self.directionX > 0:
                        self.overlap_pos.right = sprite.overlap_pos.left
                    if self.directionX < 0:
                        self.overlap_pos.left = sprite.overlap_pos.right

        if direction == 'vertical':
            for sprite in self.object_sprites:
                if sprite.overlap_pos.colliderect(self.overlap_pos):
                    if self.directionY > 0:
                        self.overlap_pos.bottom = sprite.overlap_pos.top
                    if self.directionY < 0:
                        self.overlap_pos.top = sprite.overlap_pos.bottom

    def update(self):
        self.movement()
        self.cooldown()
