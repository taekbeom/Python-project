import pygame
from sys import exit
from game import Build
import enum
import settings


class GameStates(enum.IntEnum):
    MAIN_MENU = 0
    PLAYING = 1


class GameProcess:
    def __init__(self):
        pygame.init()

        # window settings
        self.screen = pygame.display.set_mode((960, 640))
        pygame.display.set_caption("Imagine your own name")
        pygame.display.set_icon(pygame.image.load('graphics/ic32.png'))

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 50)
        self.game_state = GameStates.MAIN_MENU
        self.selected = 'start'

        self.build = None

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if self.game_state == GameStates.PLAYING:
                    if event.type == pygame.MOUSEBUTTONUP:
                        settings.mouse_button_up = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if not settings.pause_mode:
                                settings.pause_mode = True
                            else:
                                settings.pause_mode = False
                    if event.type == pygame.KEYUP:
                        settings.dialogue = True
                elif self.game_state == GameStates.MAIN_MENU:
                    self.main_menu(event)
            if self.build: self.build.start()

            pygame.display.update()
            self.clock.tick(60)

    def main_menu(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.selected == 'start':
                    self.game_state = GameStates.PLAYING
                    self.loading_screen()
                    self.build = Build()
                elif self.selected == 'exit':
                    pygame.quit()
                    exit()
            elif event.key == pygame.K_UP:
                if self.selected == 'start':
                    self.selected = 'exit'
                else:
                    self.selected = 'start'
            elif event.key == pygame.K_DOWN:
                if self.selected == 'start':
                    self.selected = 'exit'
                else:
                    self.selected = 'start'

        # draw menu
        self.screen.fill((0, 0, 0))
        if self.selected == 'start':
            self.screen.blit(pygame.font.Font(None, 50).render('Start', False, (255, 255, 255)), (440, 300))
        else:
            self.screen.blit(pygame.font.Font(None, 50).render('Exit', False, (100, 100, 100)), (440, 300))
        pygame.display.update()

    def loading_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.font.Font(None, 50).render('Loading...', False, (255, 255, 255)), (410, 300))
        pygame.display.update()


if __name__ == '__main__':
    gameProcess = GameProcess()
    gameProcess.start()
