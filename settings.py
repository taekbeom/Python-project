import pygame


mouse_button_up = False
pause_mode = False


class Pause(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('graphics/pause_sign.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
