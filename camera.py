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
            position_x = sprite.rect.centerx - self.x_pos
            position_y = sprite.rect.centery - self.y_pos
            position_rect = sprite.image.get_rect(center=(position_x, position_y))
            self.display_surf.blit(sprite.image, position_rect)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type')
                         and sprite.sprite_type == 'enemy']
        for enemy_sprite in enemy_sprites:
            enemy_sprite.enemy_update(player)

        npc_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type')
                       and sprite.sprite_type == 'npc']
        for npc_sprite in npc_sprites:
            npc_sprite.npc_update(player)

        projectile_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type')
                              and sprite.sprite_type == 'projectile']
        for projectile_sprite in projectile_sprites:
            projectile_sprite.projectile_move_x(player.status)
