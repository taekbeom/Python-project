import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/object.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.overlap_pos = self.rect.inflate(0, -20)

        # for map
        self.sprite_type = 'block'
