import pygame
import math


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.direction_x = 0
        self.direction_y = 0

        self.display_surf = pygame.display.get_surface()
        self._scale_pos()
        self.bar_show = False

    def direction_move(self, entity_velocity):
        if self.direction_x != 0 and self.direction_y != 0:
            self.direction_x = round(self.direction_x * math.sqrt(2) / 2, 1)
            self.direction_y = round(self.direction_y * math.sqrt(2) / 2, 1)

        self.overlap_pos.x += self.direction_x * entity_velocity
        self.collision('horizontal')
        self.overlap_pos.y += self.direction_y * entity_velocity
        self.collision('vertical')
        if self.sprite_type == 'player':
            self.rect.centerx = self.overlap_pos.centerx
            self.rect.centery = self.overlap_pos.centery - 1
        else:
            self.rect = self.overlap_pos
            self.final_rect = self.rect

        self.direction_x = 0
        self.direction_y = 0

    def show_hp_bar(self, self_x, self_y, self_hp, player_x, player_y, color):
        hp_bar = pygame.Rect(self_x, self_y + 60, 100, 5)

        pygame.draw.rect(self.display_surf, 'black', hp_bar)
        width = hp_bar.width * (self_hp / 100)
        current_rect = hp_bar.copy()
        current_rect.width = width

        pygame.draw.rect(self.display_surf, color, current_rect)

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
            return 0

    def _scale_pos(self):
        scaled_surf = pygame.transform.scale(self.display_surf, pygame.math.Vector2(self.display_surf.get_size())*2.8)
        self.display_surf.blit(scaled_surf, scaled_surf.get_rect(center=self.display_surf.get_rect().center))
