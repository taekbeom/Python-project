import pygame
import math


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, groups, object_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/char_sprite.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.overlap_pos = self.rect.inflate(0, -30)

        self.velocity = 5
        self.directionX = 0
        self.directionY = 0

        self.object_sprites = object_sprites

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.directionX = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.directionX = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.directionY = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.directionY = 1

        if keys[pygame.K_LSHIFT]:
            self.directionX /= 2
            self.directionY /= 2

        if pygame.mouse.get_pressed()[0]:
            pass
            #sword
        elif pygame.mouse.get_pressed()[2]:
            pass
            #bow
        elif keys[pygame.K_e]:
            pass
            #spell
        elif keys[pygame.K_f]:
            pass
            #talking to npc

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
