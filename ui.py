import pygame
import settings


class UI:
    def __init__(self, quest_sprites):
        self.display_surf = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        # self.barX = self.display_surf.get_size()[0] // 2 - 25
        # self.barY = self.display_surf.get_size()[1] // 2 + 60

        # self.hp_bar = pygame.Rect(self.barX, self.barY, 50, 5)

        self.weapon_list = []
        self.weapon_list.append(pygame.image.load('graphics/sword.png').convert_alpha())
        self.weapon_list.append(pygame.image.load('graphics/bow.png').convert_alpha())
        self.potion = pygame.image.load('graphics/health_potion.png').convert_alpha()

        self.pause_sign = settings.Pause((40, 40))
        self.status = 'continue'
        self.color_exit = 100
        self.color_continue = 255

        self.show_exclamation_mark = False
        self.show_approve_mark = False

        self.quest_sprites = quest_sprites

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

    def show_potion(self, player):
        bg_rect = pygame.Rect(650, 25, 62, 62)
        potion_surf = self.potion
        potion_rect = potion_surf.get_rect(center=bg_rect.center)
        pygame.draw.rect(self.display_surf, 'black', bg_rect)
        self.display_surf.blit(potion_surf, potion_rect)
        pygame.draw.rect(self.display_surf, 'gray', bg_rect, 2)
        text_surf = self.font.render('x' + str(player.potion_count), False, 'white')
        text_rect = text_surf.get_rect(center=(704, 84))
        self.display_surf.blit(text_surf, text_rect)

    def show_pause(self):
        pause_rect = pygame.Rect(0, 0, 200, 640)
        pygame.draw.rect(self.display_surf, 'black', pause_rect)
        shadow_surf = pygame.Surface((960, 640))
        shadow_surf.set_alpha(70)
        self.display_surf.blit(shadow_surf, (0, 0))
        self.display_surf.blit(self.pause_sign.image, self.pause_sign.rect)
        cont_surf = self.font.render('Continue', False, 'white')
        exit_surf = self.font.render('Exit', False, 'white')
        if self.status == 'exit':
            self.color_exit = 255
            self.color_continue = 100
        else:
            self.color_exit = 100
            self.color_continue = 255
        cont_surf.set_alpha(self.color_continue)
        exit_surf.set_alpha(self.color_exit)
        cont_rect = cont_surf.get_rect(topleft=(40, 400))
        exit_rect = cont_surf.get_rect(topleft=(40, 450))
        self.display_surf.blit(cont_surf, cont_rect)
        self.display_surf.blit(exit_surf, exit_rect)

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

    def show_dialogue(self, player):
        player.can_move = False
        if player.npc_status == 'give':
            text = 'Giving ' + player.current_npc
        elif player.npc_status == 'complete':
            text = 'Quest of ' + player.current_npc + ' completed'
            self.show_approve_mark = True
            if len(player.quest_list) == 0 and len(player.quest_book) > 0:
                self.show_exclamation_mark = False
        elif player.npc_status == 'quest':
            text = 'Give ' + player.target_npc + ' ' + player.current_npc
            self.show_exclamation_mark = True
        else:
            text = settings.npc_quests.get(player.current_npc)
        bg_rect = pygame.Rect(330, 270, 300, 100)
        pygame.draw.rect(self.display_surf, 'black', bg_rect)
        text_surf = self.font.render(text, False, 'white')
        text_rect = text_surf.get_rect(center=(480, 320))
        self.display_surf.blit(text_surf, text_rect)

    def show_book(self):
        book_surf = pygame.image.load('graphics/book_icon.png').convert_alpha()
        book_rect = book_surf.get_rect(topleft=(20, 40))
        self.display_surf.blit(book_surf, book_rect)
        if self.show_exclamation_mark:
            mark = pygame.image.load('graphics/exclamation_mark_image.png').convert_alpha()
        elif self.show_approve_mark:
            mark = pygame.image.load('graphics/approve_mark_image.png').convert_alpha()
        else:
            mark = None
        if mark:
            mark_rect = mark.get_rect(topleft=(64, 40))
            self.display_surf.blit(mark, mark_rect)

    def show_quest_list(self, player):
        self.show_exclamation_mark = False

        shadow_surf = pygame.Surface((960, 640))
        shadow_surf.set_alpha(70)
        self.display_surf.blit(shadow_surf, (0, 0))
        book_surf = pygame.image.load('graphics/book.png').convert_alpha()
        book_rect = book_surf.get_rect(topleft=(180, 40))
        self.display_surf.blit(book_surf, book_rect)
        pos_x = 240
        pos_y = 90
        for quest in player.quest_book:
            text_surf = self.font.render(quest[1], False, 'black')
            text_rect = text_surf.get_rect(topleft=(pos_x, pos_y))
            self.display_surf.blit(text_surf, text_rect)
            if player.quests[quest[0]]:
                pos_x_sign = 660
                complete_sign = pygame.image.load('graphics/complete_image.png')
                complete_rect = complete_sign.get_rect(topleft=(pos_x_sign, pos_y))
                self.display_surf.blit(complete_sign, complete_rect)
            pos_y += 40

    def show_lvl(self, self_exp, self_lvl):
        exp_bar = pygame.Rect(700, 600, 200, 16)
        pygame.draw.rect(self.display_surf, 'black', exp_bar)

        current_exp = self_exp
        width = exp_bar.width * current_exp / 100
        current_rect = exp_bar.copy()
        current_rect.width = width

        current_lvl = str(self_lvl) + ' lvl'
        lvl_surf = self.font.render(current_lvl, False, 'white')
        lvl_rect = lvl_surf.get_rect(topleft=(710, 570))
        self.display_surf.blit(lvl_surf, lvl_rect)

        pygame.draw.rect(self.display_surf, 'blue', current_rect)
        pygame.draw.rect(self.display_surf, 'black', current_rect, 3)

    def show_hp(self, player):
        hp_bar = pygame.Rect(50, 600, 200, 16)
        pygame.draw.rect(self.display_surf, 'black', hp_bar)

        current_hp = player.hp
        width = hp_bar.width * current_hp / 100
        current_rect = hp_bar.copy()
        current_rect.width = width

        current_hp = str(player.hp) + ' hp'
        hp_surf = self.font.render(current_hp, False, 'white')
        hp_rect = hp_surf.get_rect(topleft=(60, 570))
        self.display_surf.blit(hp_surf, hp_rect)

        pygame.draw.rect(self.display_surf, 'red', current_rect)
        pygame.draw.rect(self.display_surf, 'black', current_rect, 3)

    def display(self, player):
        self.choose_weapon(player.weapon_index)
        self.show_potion(player)
        self.show_inventory(player.quest_list)
        self.show_book()
        self.show_lvl(player.exp, player.lvl)
        self.show_hp(player)
        if player.npc_status != 'none':
            self.show_dialogue(player)
        if settings.pause_mode:
            self.show_pause()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w] and not player.killed:
                self.status = 'continue'
            if keys[pygame.K_DOWN] or keys[pygame.K_s] or player.killed:
                self.status = 'exit'
            if keys[pygame.K_RETURN]:
                if self.status == 'continue':
                    settings.pause_mode = False
                else:
                    pygame.quit()
                    exit()
        elif player.show_quests:
            self.show_quest_list(player)

