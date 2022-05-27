import pygame

import settings


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player_center, groups):
        super().__init__(groups)
        self.image = pygame.Surface((50, 10))
        # self.rect = self.image.get_rect(center=player_center)


class Sword(Weapon):
    def __init__(self, player_center, groups):
        super().__init__(player_center, groups)
        self.sprite_type = 'sword'


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player_center, object_sprites, groups):
        super().__init__(groups)
        self.image = pygame.Surface((20, 10))

        self.position = player_center
        self.rect = self.image.get_rect(center=self.position)

        self.final_rect = self.rect.copy()

        self.object_sprites = object_sprites

        self.sprite_type = 'projectile'

        self.velocity = 15

        self.direction_x = 0
        self.direction_y = 0
        self.direction_get = False

        self.fall_down = True
        self.fall_time = None
        self.fall_cd_x = 70
        self.fall_cd_y = 250
        self.ttl_cd = 1000
        self.ttl_time = None
        self.collide_object = False

    def update(self):
        if not settings.pause_mode:
            if self.direction_x != 0:
                self.collision('horizontal')
                if not self.collide_object:
                    self.rect.x += self.velocity * self.direction_x
                    self.cooldown(self.fall_cd_x)
                    if self.fall_down:
                        self.fall_time = pygame.time.get_ticks()
                        self.rect.y += 1
                        self.fall_down = False
                    if self.rect.x >= self.position[0] + 400 \
                            or self.rect.x <= self.position[0] - 400:
                        self.kill()
            elif self.direction_y != 0:
                self.collision('vertical')
                if not self.collide_object:
                    self.rect.y += self.velocity * self.direction_y
                    self.cooldown(self.fall_cd_y)
                    if self.fall_down:
                        self.fall_time = pygame.time.get_ticks()
                        self.velocity -= 1
                        self.fall_down = False
                    if self.rect.y >= self.position[1] + 300 \
                            or self.rect.y <= self.position[1] - 300:
                        self.kill()

    def cooldown(self, cd):
        if not self.fall_down:
            current_time = pygame.time.get_ticks()
            if current_time - self.fall_time >= cd:
                self.fall_down = True

    def cooldown_ttl(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.fall_time >= self.ttl_cd:
            self.kill()

    def projectile_move_x(self, status):
        if not self.direction_get:
            if status == "right":
                self.direction_x = 1
            elif status == "left":
                self.direction_x = -1
            elif status == "down":
                self.direction_y = 1
            else:
                self.direction_y = -1
            self.direction_get = True

    def collision(self, direction):
        self.ttl_time = pygame.time.get_ticks()

        if direction == 'horizontal':
            for sprite in self.object_sprites:
                if sprite.overlap_pos.colliderect(self.rect):
                    self.collide_object = True
                    if self.direction_x > 0:
                        self.rect.right = sprite.overlap_pos.left
                    if self.direction_x < 0:
                        self.rect.left = sprite.overlap_pos.right

        if direction == 'vertical':
            for sprite in self.object_sprites:
                if sprite.overlap_pos.colliderect(self.rect):
                    self.collide_object = True
                    if self.direction_y > 0:
                        self.rect.bottom = sprite.overlap_pos.top
                    if self.direction_y < 0:
                        self.rect.top = sprite.overlap_pos.bottom

        if self.collide_object:
            self.cooldown_ttl()
