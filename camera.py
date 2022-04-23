import pygame


class SpritesCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surf = pygame.display.get_surface()
        self.x_pos = 0
        self.y_pos = 0

    def sprite_build(self, player):
        self.x_pos = player.rect.centerx - self.display_surf.get_size()[0] // 2
        self.y_pos = player.rect.centery - self.display_surf.get_size()[1] // 2

        for sprite in sorted(self.sprites(), key=lambda sprite_elem: sprite_elem.rect.centery):
            position_x = sprite.rect.x - self.x_pos
            position_y = sprite.rect.y - self.y_pos
            self.display_surf.blit(sprite.image, (position_x, position_y))
