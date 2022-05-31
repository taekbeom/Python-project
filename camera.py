import pygame


class SpritesCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.x_pos = 0
        self.y_pos = 0
        self.offset = pygame.math.Vector2()

        # creating the lowest surface
        self.earth_surface = pygame.image.load('graphics/TileMap/lowestsurface.png').convert()
        self.earth_rect = self.earth_surface.get_rect(topleft=(0, 0))
        self.internal_surface = pygame.Surface(self.earth_rect.size)
        self.internal_surface_vector = pygame.math.Vector2(self.earth_rect.size)

    def sprite_build(self, player):
        self.offset = pygame.math.Vector2(self.x_pos, self.y_pos)

        # drawing the lowest surface
        earth_position = self.earth_rect.topleft - self.offset
        self.internal_surface.blit(self.earth_surface, earth_position)

        for sprite in sorted(self.sprites(), key=lambda sprite_elem: sprite_elem.rect.centery):
            position_x = sprite.rect.centerx - self.x_pos
            position_y = sprite.rect.centery - self.y_pos
            position_rect = sprite.image.get_rect(center=(position_x, position_y))
            self.internal_surface.blit(sprite.image, position_rect)

        # Crop the internal surface to the display surface
        display_rect = self.display_surface.get_rect()
        cropped_internal_surface = self.display_surface.copy()
        cropped_internal_surface.blit(self.internal_surface, display_rect, display_rect)
        self.x_pos = player.rect.centerx - cropped_internal_surface.get_size()[0] // 2
        self.y_pos = player.rect.centery - cropped_internal_surface.get_size()[1] // 2
        scaled_surf = pygame.transform.scale(cropped_internal_surface, pygame.math.Vector2(cropped_internal_surface.get_size()) * 2.8)
        self.display_surface.blit(scaled_surf, scaled_surf.get_rect(center=self.display_surface.get_rect().center))

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
        # for projectile_sprite in projectile_sprites:
            # projectile_sprite.projectile_move_x(player.status)
