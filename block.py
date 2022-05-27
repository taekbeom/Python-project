import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((16, 16))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.final_rect = self.rect.copy()
        self.overlap_pos = self.rect.inflate(0, -7)
