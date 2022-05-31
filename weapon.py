import pygame

import settings


class Sword(pygame.sprite.Sprite):
    def __init__(self, player_center, groups, status):
        super().__init__(groups)
        self.sprite_type = 'sword'
        direction_x = 0
        direction_y = 0
        if 'up' in status:
            self.image = pygame.Surface((20, 30))
            direction_y = -1
        elif 'down' in status:
            self.image = pygame.Surface((20, 30))
            direction_y = 1
        elif 'left' in status:
            self.image = pygame.Surface((30, 20))
            direction_x = -1
        elif 'right' in status:
            self.image = pygame.Surface((30, 20))
            direction_x = 1
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center=player_center)
        self.rect.move_ip(direction_x * 15, direction_y * 15)
        self.overlap_pos = self.rect.copy()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player_center, object_sprites, groups, direction):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/ItemsAssets/arrow.png')

        self.position = player_center
        self.rect = self.image.get_rect(center=self.position)

        self.overlap_pos = self.rect.copy()

        self.object_sprites = object_sprites

        self.sprite_type = 'projectile'

        self.velocity = 15

        self.direction_x, self.direction_y = self.choose_direction(direction)

        self.fall_down = True
        self.fall_time = 0
        self.fall_cd_x = 70
        self.fall_cd_y = 250
        self.ttl_cd = 1000
        self.ttl_time = None
        self.collide_object = False

    def update(self):
        if settings.pause_mode: return

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
        if self.direction_y != 0:
            self.collision('vertical')
            if not self.collide_object:
                print(self.direction_y)
                self.rect.y += self.velocity * self.direction_y
                self.cooldown(self.fall_cd_y)
                if self.fall_down:
                    self.fall_time = pygame.time.get_ticks()
                    self.rect.y += 1
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

    def choose_direction(self, status):
        direction_x = direction_y = 0
        if 'right' in status:
            direction_x = 1
        elif 'left' in status:
            direction_x = -1
            self.image = pygame.transform.rotate(self.image, 180)
        if 'down' in status:
            direction_y = 1
            self.image = pygame.transform.rotate(self.image, -90)
        elif 'up' in status:
            direction_y = -1
            self.image = pygame.transform.rotate(self.image, 90)
        return direction_x, direction_y

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
