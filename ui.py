import pygame
import settings


class UI:
    def __init__(self, quest_sprites):
        self.display_surf = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.barX = self.display_surf.get_size()[0] // 2 - 25
        self.barY = self.display_surf.get_size()[1] // 2 + 60

        self.hp_bar = pygame.Rect(self.barX, self.barY, 50, 5)

        self.weapon_list = []
        self.weapon_list.append(pygame.image.load('graphics/sword.png').convert_alpha())
        self.weapon_list.append(pygame.image.load('graphics/bow.png').convert_alpha())
        self.potion = pygame.image.load('graphics/health_potion.png').convert_alpha()

        self.pause_sign = settings.Pause((40, 40))

        self.quest_sprites = quest_sprites

    def colourful_bar(self, current_hp):
        pygame.draw.rect(self.display_surf, 'black', self.hp_bar)

        width = self.hp_bar.width * current_hp / 100
        current_rect = self.hp_bar.copy()
        current_rect.width = width

        pygame.draw.rect(self.display_surf, 'green', current_rect)

    def show_money(self, money):
        text_surf = self.font.render(str(int(money)), False, 'white')
        x = self.display_surf.get_size()[0] - 30
        y = 30
        text_rect = text_surf.get_rect(topright=(x, y))

        pygame.draw.rect(self.display_surf, 'black', text_rect.inflate(10, 10))
        self.display_surf.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surf, 'gray', text_rect.inflate(10, 10), 2)

    def show_weapon(self, index, x_pos, y_pos, alpha_lvl):
        bg_rect = pygame.Rect(x_pos, y_pos, 62, 62)
        weapon_surf = self.weapon_list[index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        pygame.draw.rect(self.display_surf, 'black', bg_rect)
        self.display_surf.blit(weapon_surf, weapon_rect)

        fg_surf = pygame.Surface((62, 62))
        fg_surf.set_alpha(alpha_lvl)
        fg_surf.fill('gray')
        self.display_surf.blit(fg_surf, (x_pos, y_pos))

        pygame.draw.rect(self.display_surf, 'gray', bg_rect, 2)

    def choose_weapon(self, index):
        if index == 0:
            self.show_weapon(index + 1, 780, 25, 100)
            self.show_weapon(index, 800, 40, 0)
        else:
            self.show_weapon(index - 1, 800, 25, 100)
            self.show_weapon(index, 780, 40, 0)

    def show_potion(self):
        bg_rect = pygame.Rect(650, 25, 62, 62)
        potion_surf = self.potion
        potion_rect = potion_surf.get_rect(center=bg_rect.center)
        pygame.draw.rect(self.display_surf, 'black', bg_rect)
        self.display_surf.blit(potion_surf, potion_rect)
        pygame.draw.rect(self.display_surf, 'gray', bg_rect, 2)

    def show_pause(self):
        pause_rect = pygame.Rect(0, 0, 200, 640)
        pygame.draw.rect(self.display_surf, 'black', pause_rect)
        shadow_surf = pygame.Surface((960, 640))
        shadow_surf.set_alpha(70)
        self.display_surf.blit(shadow_surf, (0, 0))
        self.display_surf.blit(self.pause_sign.image, self.pause_sign.rect)

    def show_inventory(self, quest_list):
        inventory_surf = pygame.Surface((260, 60))
        inventory_rect = inventory_surf.get_rect(topleft=(350, 560))
        self.display_surf.blit(inventory_surf, inventory_rect)

        inventory_case_surf = pygame.Surface((40, 40))
        inventory_case_surf.fill('gray')

        x = 360
        for i in range(5):
            inventory_rect = inventory_case_surf.get_rect(topleft=(x, 570))
            self.display_surf.blit(inventory_case_surf, inventory_rect)
            if len(quest_list) >= i+1:
                for quest_sprite in self.quest_sprites:
                    if quest_sprite.quest_type == quest_list[i]:
                        quest_sprite.rect = quest_sprite.image.get_rect(topleft=(x, 570))
                        self.display_surf.blit(quest_sprite.image, quest_sprite.rect)
            x += 50

    def display(self, player):
        if player.bar_show:
            self.colourful_bar(player.hp)
        self.show_money(player.money)
        self.choose_weapon(player.weapon_index)
        self.show_potion()
        self.show_inventory(player.quest_list)
        if settings.pause_mode:
            self.show_pause()
