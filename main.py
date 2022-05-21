import pygame
from sys import exit
from game import Build
import settings


class GameProcess:
    def __init__(self):
        pygame.init()

        # window settings
        self.screen = pygame.display.set_mode((960, 640), pygame.RESIZABLE)
        pygame.display.set_caption("Imagine your own name")
        pygame.display.set_icon(pygame.image.load('graphics/ic32.png'))

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 50)

        self.test_surf = pygame.image.load('graphics/map.png')

        self.build = Build()

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    settings.mouse_button_up = True

            self.screen.blit(self.test_surf, (0, 0))
            self.build.start()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    gameProcess = GameProcess()
    gameProcess.start()
