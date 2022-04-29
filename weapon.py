import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player_center, groups):
        super().__init__(groups)
        self.image = pygame.Surface((40, 10))
        # self.rect = self.image.get_rect(center=player_center)


class Sword(Weapon):
    def __init__(self, player_center, groups):
        super().__init__(player_center, groups)


class Bow(Weapon):
    def __init__(self, player_center, groups):
        super().__init__(player_center, groups)
