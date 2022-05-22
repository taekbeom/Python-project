import pygame
import math


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.direction_x = 0
        self.direction_y = 0

    def direction_move(self, entity_velocity):
        if self.direction_x != 0 and self.direction_y != 0:
            self.direction_x = round(self.direction_x * math.sqrt(2) / 2, 1)
            self.direction_y = round(self.direction_y * math.sqrt(2) / 2, 1)

        self.overlap_pos.x += self.direction_x * entity_velocity
        self.collision('horizontal')
        self.overlap_pos.y += self.direction_y * entity_velocity
        self.collision('vertical')
        self.rect = self.overlap_pos

        self.direction_x = 0
        self.direction_y = 0

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.object_sprites:
                if sprite.overlap_pos.colliderect(self.overlap_pos):
                    if self.direction_x > 0:
                        self.overlap_pos.right = sprite.overlap_pos.left
                    if self.direction_x < 0:
                        self.overlap_pos.left = sprite.overlap_pos.right

        if direction == 'vertical':
            for sprite in self.object_sprites:
                if sprite.overlap_pos.colliderect(self.overlap_pos):
                    if self.direction_y > 0:
                        self.overlap_pos.bottom = sprite.overlap_pos.top
                    if self.direction_y < 0:
                        self.overlap_pos.top = sprite.overlap_pos.bottom

    def flicker(self):
        value = math.sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return  0
