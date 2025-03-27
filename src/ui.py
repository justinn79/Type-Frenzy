from src.settings import *
from src.support import *
from src.bg_particles import *
from src.timer import Timer

from src.audio_manager import *

class AllImageImports():
    def __init__(self):
        # ------------------------------ IMAGES FOR THE MAIN MENU ------------------------------------------------------------
        self.main_menu_bg = pygame.image.load('assets/images/ui/main_menu_background.png').convert_alpha()
        self.game_title_banner = pygame.image.load('assets/images/ui/game_title_banner.png').convert_alpha()
        self.menu_selection_box_img = pygame.image.load('assets/images/ui/menu_selection_box.png').convert_alpha()
        self.menu_button_img = pygame.image.load('assets/images/ui/menu_button.png').convert_alpha()

        # icons for the game modifiers
        self.double_time_icon = pygame.image.load('assets/images/game_mod_icons/double_time_icon.png').convert_alpha()
        self.hidden_icon = pygame.image.load('assets/images/game_mod_icons/hidden_icon.png').convert_alpha()
        self.perfect_icon = pygame.image.load('assets/images/game_mod_icons/perfect_icon.png').convert_alpha()

        # buttons for the game modifiers
        self.menu_game_modifier_button_img = pygame.image.load('assets/images/ui/menu_game_modifier_button.png').convert_alpha()
        self.unselected_box_img = pygame.image.load('assets/images/ui/unselected_box.png').convert_alpha()
        self.selected_box_img = pygame.image.load('assets/images/ui/selected_box.png').convert_alpha()

# ------------------------------------------------- MAIN MENU UI ------------------------------------------------------------------------------------
class MainMenu(AllImageImports):
    def __init__(self, display_surface, audio_manager):

        super().__init__()

        #----------------AUDIO-------------------------
        self.audio_manager = audio_manager
        self.sound_volume = 0.2

        self.display_surface = display_surface
        self.title_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 45)
        self.menu_box_title_font = pygame.font.Font('assets/fonts/Bungee-Regular.ttf', 35)
        self.menu_box_description_font = pygame.font.Font('assets/fonts/SpaceGrotesk-Medium.ttf', 15)
        self.font = pygame.font.Font('assets/fonts/Bungee-Regular.ttf', 25)

        self.bg_particles = [BgParticles(self.display_surface) for _ in range(100)]

        # ----------------------------------------------------------------------------------------------------------

        # Home menu control
        self.home_menu_options = ['START', 'HOW TO PLAY', 'QUIT']
        self.home_menu_index = 0
        self.home_menu_option_count = len(self.home_menu_options)

        self.main_menu_screen_state = 'MAIN MENU'
        self.original_main_menu_screen_state =  self.main_menu_screen_state

        # how to play text descriptions
        self.how_to_play_description_text = ' - Type and match the prompted words on the screen.\n\n' \
        ' - Lives are shown at the top left of the screen and are lost when submitting an incorrect word.\n\n' \
        ' - There is a typing meter at the bottom that depletes overtime but resets after every correct input. \n\n' \
        ' - Game modifiers can be selected before you start the game which can increase your combo multiplier. \n\n\n' \
        ' - Press ESCAPE on your keyboard to return to the MAIN MENU'

    def reset_main_menu_screen_state(self):
        self.main_menu_screen_state = self.original_main_menu_screen_state
        self.home_menu_index = 0

    def input(self):
        keys = pygame.key.get_just_pressed()
        # navigating the menu with keys
        # handle input for menu navigation within the home main menu menu
        if keys[pygame.K_DOWN]:
            self.home_menu_index += 1
            self.audio_manager.play_sound_effect('menu_nav_sound', self.sound_volume)
        elif keys[pygame.K_UP]:
            self.home_menu_index -= 1
            self.audio_manager.play_sound_effect('menu_nav_sound', self.sound_volume)

        # wrap around the index
        self.home_menu_index %= self.home_menu_option_count
        if keys[pygame.K_SPACE]:
            self.audio_manager.play_sound_effect('menu_select_sound', self.sound_volume)

            if self.home_menu_options[self.home_menu_index] == 'START':
                self.main_menu_screen_state = 'PRE GAME SELECT'
            else:
                self.main_menu_screen_state = self.home_menu_options[self.home_menu_index]
            
        if keys[pygame.K_ESCAPE]:
            self.main_menu_screen_state = 'MAIN MENU'
            self.home_menu_index = 0
    
    def draw_bg(self):
        self.scaled_main_menu_bg = pygame.transform.scale(self.main_menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.scaled_main_menu_bg_rect = self.scaled_main_menu_bg.get_frect(topleft=(0,0))
        self.display_surface.blit(self.scaled_main_menu_bg, self.scaled_main_menu_bg_rect)
    
    def draw_particle_bg(self):
        for bg_particle in self.bg_particles:
            bg_particle.update()

    def draw_game_title(self):
        title_x = WINDOW_WIDTH // 2
        title_y = WINDOW_HEIGHT // 5

        game_title_banner_scaled = pygame.transform.scale(self.game_title_banner, (self.game_title_banner.width * 1.5,self.game_title_banner.height * 1.5))
        game_title_banner_rect = game_title_banner_scaled.get_frect(center=(title_x, title_y))

        self.display_surface.blit(game_title_banner_scaled, game_title_banner_rect)
        
    def main_menu_selection(self, main_menu_bg_rect, index, options):
        main_menu_bg_rect = main_menu_bg_rect

        # menu selection box coordinates
        menu_selection_box_img_x = main_menu_bg_rect.width // 2
        menu_selection_box_img_y = WINDOW_HEIGHT - (main_menu_bg_rect.height // 3)

        # menu selection box scaling
        self.menu_selection_box_img_scaled = pygame.transform.scale(self.menu_selection_box_img, (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 1.75))

        # creating a rect of the newly scaled menu selection box image after it is scaled and blitting it onto the screen
        self.menu_selection_box_img_rect = self.menu_selection_box_img_scaled.get_frect(center=(menu_selection_box_img_x, menu_selection_box_img_y))
        self.display_surface.blit(self.menu_selection_box_img_scaled, self.menu_selection_box_img_rect)

        # MENU SELECTION OPTIONS
        for optionIndex in range(len(options)):
            # x and y are the center points for each option
            x = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width / 2)
            y = self.menu_selection_box_img_rect.top + (self.menu_selection_box_img_rect.height / (len(options) + 2)) * (optionIndex + 1.5)

            if optionIndex == index:
                color = COLORS['midpurple']
            else:
                color = COLORS['white']

            # blitting the text on the button
            text_surf = self.font.render(options[optionIndex], True, color)
            text_rect = text_surf.get_frect(center = (x,y))

            # creating the button location for the text
            menu_button_img_scaled = pygame.transform.scale(self.menu_button_img, (text_rect.width * 1.5, text_rect.height * 2))
            button_rect = menu_button_img_scaled.get_frect(center = (x,y))

            self.display_surface.blit(menu_button_img_scaled, button_rect)
            self.display_surface.blit(text_surf, text_rect)

    def how_to_play_screen(self, main_menu_bg_rect):
        main_menu_bg_rect = main_menu_bg_rect

        # menu selection box coordinates
        menu_selection_box_img_x = main_menu_bg_rect.width // 2
        menu_selection_box_img_y = WINDOW_HEIGHT - (main_menu_bg_rect.height // 3)

        # menu selection box scaling
        self.menu_selection_box_img_scaled = pygame.transform.scale(self.menu_selection_box_img, (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 1.75))

        # creating a rect of the newly scaled menu selection box image after it is scaled and blitting it onto the screen
        self.menu_selection_box_img_rect = self.menu_selection_box_img_scaled.get_frect(center=(menu_selection_box_img_x, menu_selection_box_img_y))
        self.display_surface.blit(self.menu_selection_box_img_scaled, self.menu_selection_box_img_rect)

        # --------------- HOW TO PLAY TITLE TEXT ------------------
        title_x = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width / 2)
        title_y = self.menu_selection_box_img_rect.top + 60

        how_to_play_title_text = self.menu_box_title_font.render('HOW TO PLAY', True, COLORS['black'])
        how_to_play_title_text_rect = how_to_play_title_text.get_frect(center=(title_x, title_y))

        self.display_surface.blit(how_to_play_title_text, how_to_play_title_text_rect)

        # --------------- HOW TO PLAY TEXT DESCRIPTION ------------------
        description_text_x = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width / 2)
        description_text_y = how_to_play_title_text_rect.top + 180

        description_text_text = self.menu_box_description_font.render(self.how_to_play_description_text, True, COLORS['black'])
        description_text_rect = description_text_text.get_frect(center=(description_text_x, description_text_y))

        self.display_surface.blit(description_text_text, description_text_rect)

    def draw_menu(self):
        match self.main_menu_screen_state:
            case 'MAIN MENU':
                self.main_menu_selection(self.scaled_main_menu_bg_rect, self.home_menu_index, self.home_menu_options)
            case 'PRE GAME SELECT':
                pygame.time.delay(50)
                pass
            case 'HOW TO PLAY':
                self.how_to_play_screen(self.scaled_main_menu_bg_rect)

    def update(self):
        self.input()
        self.draw_bg()
        self.draw_particle_bg()
        self.draw_game_title()
        self.draw_menu()

# ------------------------------------------------- PAUSED GAME UI ------------------------------------------------------------------------------------
class PauseGameMenu(AllImageImports):
    def __init__(self, display_surface, audio_manager):

        super().__init__()

        #----------------AUDIO-------------------------
        self.audio_manager = audio_manager
        self.sound_volume = 0.2

        self.display_surface = display_surface

        self.title_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 30)
        self.font = pygame.font.Font('assets/fonts/Bungee-Regular.ttf', 25)

        # pause menu control
        self.pause_menu_options = ['CONTINUE', 'RESTART', 'MAIN MENU']
        self.pause_menu_index = 0
        self.pause_menu_option_count = len(self.pause_menu_options)

        self.pause_menu_screen_state = ''
        self.original_pause_menu_screen_state = self.pause_menu_screen_state

    def reset_pause_menu_screen_state(self):
        self.pause_menu_screen_state = self.original_pause_menu_screen_state
        self.pause_menu_index = 0

    def input(self):
        keys = pygame.key.get_just_pressed()
        # navigating the menu with keys
        # handle input for menu navigation within the pause menu
        if keys[pygame.K_DOWN]:
            self.pause_menu_index += 1
            self.audio_manager.play_sound_effect('menu_nav_sound', self.sound_volume)
        elif keys[pygame.K_UP]:
            self.pause_menu_index -= 1
            self.audio_manager.play_sound_effect('menu_nav_sound', self.sound_volume)

        # wrap around the index
        self.pause_menu_index %= self.pause_menu_option_count
        if keys[pygame.K_SPACE]:
            self.audio_manager.play_sound_effect('menu_select_sound', self.sound_volume)
            # when the player selects one of the options, change the current state of the ui to whatever the player selects.
            self.pause_menu_screen_state = self.pause_menu_options[self.pause_menu_index]
            
        if keys[pygame.K_ESCAPE]:
            # CONTINUE THE GAME
            pass
    
    def draw(self, index, options):
        # menu selection box coordinates
        menu_selection_box_img_x = WINDOW_WIDTH // 2
        menu_selection_box_img_y = WINDOW_HEIGHT // 2

        # menu selection box scaling
        self.menu_selection_box_img_scaled = pygame.transform.scale(self.menu_selection_box_img, (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 1.75))

        # creating a rect of the newly scaled menu selection box image after it is scaled and blitting it onto the screen
        self.menu_selection_box_img_rect = self.menu_selection_box_img_scaled.get_frect(center=(menu_selection_box_img_x, menu_selection_box_img_y))
        self.display_surface.blit(self.menu_selection_box_img_scaled, self.menu_selection_box_img_rect)

        pause_game_text = self.title_font.render('PAUSED', True, COLORS['white'])
        pause_game_text_rect = pause_game_text.get_frect(center=(self.menu_selection_box_img_rect.centerx, WINDOW_HEIGHT // 7))

        self.display_surface.blit(pause_game_text, pause_game_text_rect)

        # MENU SELECTION OPTIONS
        for optionIndex in range(len(options)):
            # x and y are the center points for each option
            x = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width / 2)
            y = self.menu_selection_box_img_rect.top + (self.menu_selection_box_img_rect.height / (len(options) + 2)) * (optionIndex + 1.5)

            if optionIndex == index:
                color = COLORS['midpurple']
            else:
                color = COLORS['white']


            # blitting the text on the button
            text_surf = self.font.render(options[optionIndex], True, color)
            text_rect = text_surf.get_frect(center = (x,y))

            # creating the button location for the text
            menu_button_img_scaled = pygame.transform.scale(self.menu_button_img, (text_rect.width * 1.5, text_rect.height * 2))
            button_rect = menu_button_img_scaled.get_frect(center = (x,y))

            # blitting the button image first then the text surf on top
            self.display_surface.blit(menu_button_img_scaled, button_rect)
            self.display_surface.blit(text_surf, text_rect)

    def update(self):
        self.input()
        self.draw(self.pause_menu_index, self.pause_menu_options)

# ------------------------------------------------- GAME OVER UI ------------------------------------------------------------------------------------
class GameOverMenu(AllImageImports):
    def __init__(self, display_surface, audio_manager):

        super().__init__()

        #----------------AUDIO-------------------------
        self.audio_manager = audio_manager
        self.sound_volume = 0.2

        self.display_surface = display_surface

        self.bg_particles = [BgParticles(self.display_surface) for _ in range(100)]

        self.title_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 40)
        self.score_font = pygame.font.Font('assets/fonts/Bungee-Regular.ttf', 30)
        self.font = pygame.font.Font('assets/fonts/Bungee-Regular.ttf', 25)
        self.font1 = pygame.font.Font('assets/fonts/Bungee-Regular.ttf', 25)
        self.font2 = pygame.font.Font('assets/fonts/Bungee-Regular.ttf', 30)

        # game over menu control
        self.game_over_menu_options = ['TRY AGAIN', 'MAIN MENU']
        self.game_over_menu_index = 0
        self.game_over_menu_option_count = len(self.game_over_menu_options)

        self.game_over_menu_screen_state = ''
        self.original_game_over_menu_screen_state = self.game_over_menu_screen_state

        # game_over_reason being either "out of lives" or "out of time"
        self.game_over_reason = 'testing 123'
        self.original_game_over_reason = self.game_over_reason

        # game modifier icon images
        self.icon_scale = 1
        # double time mod icon
        self.double_time_icon = pygame.transform.scale(self.double_time_icon, (self.double_time_icon.get_width() * self.icon_scale, self.double_time_icon.get_height() * self.icon_scale))
        # hidden mod icon
        self.hidden_icon = pygame.transform.scale(self.hidden_icon, (self.hidden_icon.get_width() * self.icon_scale, self.hidden_icon.get_height() * self.icon_scale))
        # perfect mod icon
        self.perfect_icon = pygame.transform.scale(self.perfect_icon, (self.perfect_icon.get_width() * self.icon_scale, self.perfect_icon.get_height() * self.icon_scale))

        self.score_value = 0

        self.highest_combo_value = 0

        self.game_modifiers = []

        # ignore player input timer
        self.ignore_input_timer = Timer(3000, autostart=True)

    def draw_bg(self):
        self.scaled_main_menu_bg = pygame.transform.scale(self.main_menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.scaled_main_menu_bg_rect = self.scaled_main_menu_bg.get_frect(topleft=(0,0))
        self.display_surface.blit(self.scaled_main_menu_bg, self.scaled_main_menu_bg_rect)

    def draw_particle_bg(self):
        for bg_particle in self.bg_particles:
            bg_particle.update()

    def out_of_lives_game_over(self):
        self.game_over_reason = 'You ran out of lives'

    def out_of_time_game_over(self):
        self.game_over_reason = 'You ran out of time'

    def reset_game_over_menu_screen_state(self):
        self.game_over_menu_screen_state = self.original_game_over_menu_screen_state
        self.game_over_menu_index = 0

    def fetch_score_value(self, score_value):
        self.score_value = score_value

    def fetch_highest_combo_value(self, highest_combo_value):
        self.highest_combo_value = highest_combo_value

    def fetch_game_modifiers(self, game_modifier_list):
        self.game_modifiers = game_modifier_list

    def input(self):
        keys = pygame.key.get_just_pressed()
        # navigating the menu with keys
        # handle input for menu navigation within the game_over menu
        if keys[pygame.K_DOWN]:
            self.game_over_menu_index += 1
            self.audio_manager.play_sound_effect('menu_nav_sound', self.sound_volume)
        elif keys[pygame.K_UP]:
            self.game_over_menu_index -= 1
            self.audio_manager.play_sound_effect('menu_nav_sound', self.sound_volume)

        # wrap around the index
        self.game_over_menu_index %= self.game_over_menu_option_count
        if keys[pygame.K_SPACE]:
            self.audio_manager.play_sound_effect('menu_select_sound', self.sound_volume)
            # when the player selects one of the options, change the current state of the ui to whatever the player selects.
            self.game_over_menu_screen_state = self.game_over_menu_options[self.game_over_menu_index]
    
    def draw(self, index, options):
        
        # ---------------- GAME OVER TEXT -------------------
        game_over_text_x = WINDOW_WIDTH // 2
        game_over_text_y = WINDOW_HEIGHT // 7

        game_over_text = self.title_font.render('GAME OVER' , True, COLORS['white'])
        game_over_text_rect = game_over_text.get_frect(center=(game_over_text_x, game_over_text_y - 20))

        self.display_surface.blit(game_over_text, game_over_text_rect)

        # ---------------- SCORE DISPLAY TEXT -------------------
        score_text = self.score_font.render('Score: ' + str(self.score_value), True, COLORS['white'])
        score_text_rect = score_text.get_frect(center=(game_over_text_x, game_over_text_y + 30))

        self.display_surface.blit(score_text, score_text_rect)

        # ---------------- COMBO DISPLAY TEXT -------------------
        highest_combo_text = self.font1.render('Highest Combo: ' + str(self.highest_combo_value), True, COLORS['white'])
        highest_combo_text_rect = highest_combo_text.get_frect(center=(score_text_rect.centerx, score_text_rect.y + 60))

        self.display_surface.blit(highest_combo_text, highest_combo_text_rect)

        # ---------------- GAME MODIFIERS DISPLAY TEXT -------------------
        game_modifier_text = self.font1.render('Game Modifiers used: ', True, COLORS['white'])
        game_modifier_text_rect = game_modifier_text.get_frect(center=(highest_combo_text_rect.centerx, highest_combo_text_rect.y + 55))

        self.display_surface.blit(game_modifier_text, game_modifier_text_rect)

        icon_spacing = 35
        for i in range(len(self.game_modifiers)):
            if self.game_modifiers[i] == 'Double Time':
                icon_surf = self.double_time_icon
            if self.game_modifiers[i] == 'Hidden':
                icon_surf = self.hidden_icon
            if self.game_modifiers[i] == 'Perfect':
                icon_surf = self.perfect_icon

            x_loc = game_modifier_text_rect.right + (i * icon_spacing)
            y_loc = game_modifier_text_rect.y
            
            self.display_surface.blit(icon_surf, (x_loc, y_loc))

        # if there are no game modifiers selected, then just display the text "None" beside "Game Modifiers used:"
        if not self.game_modifiers:
            no_game_modifiers_text = self.font1.render('None', True, COLORS['white'])
            self.display_surface.blit(no_game_modifiers_text, (game_modifier_text_rect.right + 5, game_modifier_text_rect.y))

        # ----------------- MENU SELECTION BOX ---------------------------
        # menu selection box coordinates
        menu_selection_box_img_x = WINDOW_WIDTH // 2
        menu_selection_box_img_y = WINDOW_HEIGHT // 2

        # menu selection box scaling
        self.menu_selection_box_img_scaled = pygame.transform.scale(self.menu_selection_box_img, (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 1.75))

        # creating a rect of the newly scaled menu selection box image after it is scaled and blitting it onto the screen
        self.menu_selection_box_img_rect = self.menu_selection_box_img_scaled.get_frect(center=(menu_selection_box_img_x, menu_selection_box_img_y + 90))
        self.display_surface.blit(self.menu_selection_box_img_scaled, self.menu_selection_box_img_rect)

        # ---------------- GAME OVER REASON TEXT -------------------

        game_over_reason_text = self.font2.render(str(self.game_over_reason), True, COLORS['white'])
        game_over_reason_text_rect = game_over_reason_text.get_frect(center=(self.menu_selection_box_img_rect.centerx, self.menu_selection_box_img_rect.y + 75))

        game_over_reason_bg_surf = pygame.Surface((game_over_reason_text_rect.width + 50, game_over_reason_text_rect.height + 10), pygame.SRCALPHA)
        game_over_reason_bg_surf.fill((0, 0, 0, 0)) # black with full opacity
        pygame.draw.rect(game_over_reason_bg_surf, COLORS['black'], game_over_reason_bg_surf.get_rect(), border_radius=10)

        game_over_reason_bg_rect = game_over_reason_bg_surf.get_frect(center=(game_over_reason_text_rect.center))

        self.display_surface.blit(game_over_reason_bg_surf, game_over_reason_bg_rect)
        self.display_surface.blit(game_over_reason_text, game_over_reason_text_rect)

        # MENU SELECTION OPTIONS
        for optionIndex in range(len(options)):
            x = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width / 2)
            y = self.menu_selection_box_img_rect.top + (self.menu_selection_box_img_rect.height / (len(options) + 2)) * (optionIndex + 1.5)

            if optionIndex == index:
                color = COLORS['midpurple']
            else:
                color = COLORS['white']

            # blitting the text on the button
            text_surf = self.font.render(options[optionIndex], True, color)
            text_rect = text_surf.get_frect(center = (x,y))

            # creating the button location for the text
            menu_button_img_scaled = pygame.transform.scale(self.menu_button_img, (text_rect.width * 1.5, text_rect.height * 2))
            button_rect = menu_button_img_scaled.get_frect(center = (x,y))

            # blitting the button image first then the text surf on top
            self.display_surface.blit(menu_button_img_scaled, button_rect)
            self.display_surface.blit(text_surf, text_rect)

    def update(self):
        self.draw_bg()
        self.draw_particle_bg()
        if not self.ignore_input_timer.active: # once the ignore_input_timer is not active anymore, allow player input
            self.input()
        self.draw(self.game_over_menu_index, self.game_over_menu_options)
        self.ignore_input_timer.update()

# ------------------------------------------------- PRE GAME SELECT UI ------------------------------------------------------------------------------------
class PreGameSelectMenu(AllImageImports):
    def __init__(self, display_surface, audio_manager):

        super().__init__()
        
        #----------------AUDIO-------------------------
        self.audio_manager = audio_manager
        self.sound_volume = 0.2

        self.display_surface = display_surface

        self.bg_particles = [BgParticles(self.display_surface) for _ in range(100)]

        self.font = pygame.font.Font('assets/fonts/Bungee-Regular.ttf', 20)

        self.title_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 30)
        self.play_button_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 20)
        self.game_modifier_title_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 25)
        self.game_modifier_text_font = pygame.font.Font('assets/fonts/SpaceGrotesk-Medium.ttf', 15)

        # selection box scaling
        self.unselected_box_surf = pygame.transform.scale(self.unselected_box_img, (self.unselected_box_img.width * 2, self.unselected_box_img.height * 2))
        self.selected_box_surf = pygame.transform.scale(self.selected_box_img, (self.selected_box_img.width * 2, self.selected_box_img.height * 2))

        # pre_game_select menu control
        self.pre_game_select_menu_options = ['Double Time', 'Hidden', 'Perfect', 'PLAY']
        self.pre_game_select_menu_index = 0
        self.pre_game_select_menu_option_count = len(self.pre_game_select_menu_options)

        self.pre_game_select_menu_screen_state = ''
        self.original_pre_game_select_menu_screen_state = self.pre_game_select_menu_screen_state

        self.modifier_selected_bool = False
        self.modifier_selection = []

        # get the current menu option that the user is currently hovering on
        self.user_current_option_index = 0

        # game modifier icon images
        self.icon_scale = 1.5

        # double time mod icon
        self.double_time_icon = pygame.transform.scale(self.double_time_icon, (self.double_time_icon.get_width() * self.icon_scale, self.double_time_icon.get_height() * self.icon_scale))

        # hidden mod icon
        self.hidden_icon = pygame.transform.scale(self.hidden_icon, (self.hidden_icon.get_width() * self.icon_scale, self.hidden_icon.get_height() * self.icon_scale))

        # perfect mod icon
        self.perfect_icon = pygame.transform.scale(self.perfect_icon, (self.perfect_icon.get_width() * self.icon_scale, self.perfect_icon.get_height() * self.icon_scale))

        # game modifier text description
        self.double_time_text = 'The typing countdown meter is twice as fast. Type the current word quickly before the timer runs out. \n\n Combo Multiplier Value: 1.25x'
        self.hidden_text = 'The current queued text will not be displayed. Remember that word before it comes into queue. \n\n Combo Multiplier Value: 1.15x'
        self.perfect_text = ' One life. Submit an incorrect word, it is game over! Ensure that your input is correct before submitting. \n\n Combo Multiplier Value: 1.10x'

    def get_modifier_selection(self):
        return self.modifier_selection

    def draw_game_modifier_icon(self, user_modifier_selection, modifier_text_rect):
            # checking what modifier the user is currently hovering over. depending on what it is, change the icon_surf icon to its corresponding game modifier (this function is used within "draw_option_description()")
            if user_modifier_selection == 'Double Time':
                icon_surf = self.double_time_icon
            if user_modifier_selection == 'Hidden':
                icon_surf = self.hidden_icon
            if user_modifier_selection == 'Perfect':
                icon_surf = self.perfect_icon

            x_loc = modifier_text_rect.centerx - 30
            y_loc = modifier_text_rect.y + 40
            
            self.display_surface.blit(icon_surf, (x_loc, y_loc))
        
    def draw_bg(self):
        self.scaled_main_menu_bg = pygame.transform.scale(self.main_menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.scaled_main_menu_bg_rect = self.scaled_main_menu_bg.get_frect(topleft=(0,0))
        self.display_surface.blit(self.scaled_main_menu_bg, self.scaled_main_menu_bg_rect)

    def draw_particle_bg(self):
        for bg_particle in self.bg_particles:
            bg_particle.update()

    def reset_pre_game_select_menu_screen_state(self):
        self.pre_game_select_menu_screen_state = self.original_pre_game_select_menu_screen_state
        self.pre_game_select_menu_index = 0
        self.user_current_option_index = 0

    def input(self):
        keys = pygame.key.get_just_pressed()
        # navigating the menu with keys
        # handle input for menu navigation within the pre_game_select menu
        if keys[pygame.K_DOWN]:
            self.pre_game_select_menu_index += 1
            self.audio_manager.play_sound_effect('menu_nav_sound', self.sound_volume)
        elif keys[pygame.K_UP]:
            self.pre_game_select_menu_index -= 1
            self.audio_manager.play_sound_effect('menu_nav_sound', self.sound_volume)

        # wrap around the index
        self.pre_game_select_menu_index %= self.pre_game_select_menu_option_count
        if keys[pygame.K_SPACE]:
            self.audio_manager.play_sound_effect('menu_select_sound', self.sound_volume)
            user_menu_selection = self.pre_game_select_menu_options[self.pre_game_select_menu_index]
            # only update self.pre_game_select_menu_screen_state when the player selects 'PLAY'
            if user_menu_selection == 'PLAY':
                self.pre_game_select_menu_screen_state = user_menu_selection
            else:
                # otherwise, just store the option that the player selected within this pre_game_select_menu to the "self.modifier_select" variable.
                if (user_menu_selection) not in self.modifier_selection:
                    self.modifier_selection.append(user_menu_selection)
                else:
                    self.modifier_selection.remove(user_menu_selection)
            
        if keys[pygame.K_ESCAPE]:
            self.audio_manager.play_sound_effect('menu_select_sound', self.sound_volume)
            self.pre_game_select_menu_screen_state = 'MAIN MENU'

    def draw_faded_background_for_text_desc(self):
        x_right_center_of_menu_selection_box = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width // 4) * 3
        y_right_center_of_menu_selection_box = self.menu_selection_box_img_rect.height / 1.6

        # faded_background surface
        faded_background_surf = pygame.Surface((self.menu_selection_box_img_rect.width // 2 - 100, self.menu_selection_box_img_rect.height - self.menu_selection_box_img_rect.height / 4.5), pygame.SRCALPHA)
        
        faded_background_surf.fill((0, 0, 0, 0))  # making sure the surface starts transparent
        pygame.draw.rect(faded_background_surf, (128, 128, 128, 128), faded_background_surf.get_rect(), border_radius=10)

        self.faded_background_rect = faded_background_surf.get_rect(center=(x_right_center_of_menu_selection_box, y_right_center_of_menu_selection_box))

        self.display_surface.blit(faded_background_surf, self.faded_background_rect)

    # a function to wrap the text within a rect
    def wrap_text(self, text, font, rect_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            # a test if the current word can be added to the line
            test_line = current_line + (word if current_line == "" else " " + word)
            test_width, _ = font.size(test_line)

            if test_width <= rect_width:
                current_line = test_line
            else:
                # if the word doesnt fit, start a new line
                if current_line != "":
                    lines.append(current_line)
                current_line = word

        # if there is a remaining line, append it to the current line
        if current_line != "":
            lines.append(current_line)

        return lines

    def current_user_option_description(self, current_user_option, text_font):
        if current_user_option == 'Double Time':
            text_lines = self.wrap_text(self.double_time_text, text_font, self.faded_background_rect.width)
            y_offset = self.faded_background_rect.top + self.faded_background_rect.height - 230
            for line in text_lines:
                line_surface = text_font.render(line, True, COLORS['black'])
                self.display_surface.blit(line_surface, (self.faded_background_rect.left + 2, y_offset))
                y_offset += line_surface.get_height()

        if current_user_option == 'Hidden':
            text_lines = self.wrap_text(self.hidden_text, text_font, self.faded_background_rect.width)
            y_offset = self.faded_background_rect.top + self.faded_background_rect.height - 230
            for line in text_lines:
                line_surface = text_font.render(line, True, COLORS['black'])
                self.display_surface.blit(line_surface, (self.faded_background_rect.left + 2, y_offset))
                y_offset += line_surface.get_height()

        if current_user_option == 'Perfect':
            text_lines = self.wrap_text(self.perfect_text, text_font, self.faded_background_rect.width)
            y_offset = self.faded_background_rect.top + self.faded_background_rect.height - 230
            for line in text_lines:
                line_surface = text_font.render(line, True, COLORS['black'])
                self.display_surface.blit(line_surface, (self.faded_background_rect.left + 2, y_offset))
                y_offset += line_surface.get_height()

    def draw_menu_options(self, index, options):
        x_center = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width / 2)
        y_under_rect = self.menu_selection_box_img_rect.bottom + 75


        x_left_center_of_menu_selection_box = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width // 4)

        for optionIndex in range(len(options)):
            x = x_left_center_of_menu_selection_box
            y = self.menu_selection_box_img_rect.top + (self.menu_selection_box_img_rect.height / (len(options) + 2)) * (optionIndex + 1.5)

            if optionIndex == index:
                color = COLORS['midpurple']
                self.user_current_option_index = index # gets the current index that the user is currently hovering on and updates it onto this variable
            else:
                color = COLORS['white']

            text_surf = self.font.render(options[optionIndex], True, color)
            
            if options[optionIndex] == 'PLAY':
                text_surf = self.play_button_font.render(options[optionIndex], True, color)
                text_rect = text_surf.get_frect(center = (x_center, y_under_rect))
            else:
                text_surf = self.font.render(options[optionIndex], True, color)
                text_rect = text_surf.get_frect(midleft = (x,y))
                
                # checking what modifiers were selected by the user. we want to display the selected_box_surf if it is selected and the unselected_box_surf when it is not selected.
                if str(options[optionIndex]) in self.modifier_selection:
                    selection_box_surf = self.selected_box_surf
                    selection_box_rect = self.unselected_box_surf.get_frect(topright = (text_rect.left - 50, text_rect.y))
                else:
                    selection_box_surf = self.unselected_box_surf
                    selection_box_rect = self.unselected_box_surf.get_frect(topright = (text_rect.left - 50, text_rect.y))

            # if the menu option is 'PLAY', then put that BUTTON image at the center of the screen under the menu box rect
            if options[optionIndex] == 'PLAY':
                menu_button_img_scaled = pygame.transform.scale(self.menu_button_img, (text_rect.width * 2, text_rect.height * 3))
                button_rect = menu_button_img_scaled.get_frect(center = (x_center, y_under_rect))
            else:
                menu_button_img_scaled = pygame.transform.scale(self.menu_game_modifier_button_img, (text_rect.width * 1.5, text_rect.height * 2))
                button_rect = menu_button_img_scaled.get_frect(center = (text_rect.centerx, text_rect.centery))

            # blitting the button image first then the text surf on top
            self.display_surface.blit(menu_button_img_scaled, button_rect)
            self.display_surface.blit(text_surf, text_rect)
            
            # blitting the checkboxes beside each option
            self.display_surface.blit(selection_box_surf, selection_box_rect)
            
    def draw_option_description(self):
        # -------------- THE OPTION HEADER ----------------------
        option_header_x = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width // 4) * 3
        option_header_y = self.menu_selection_box_img_rect.top + 125

        current_user_option = self.pre_game_select_menu_options[self.user_current_option_index]
        
        option_header_text_surf = self.game_modifier_title_font.render(current_user_option, True, COLORS['black'])
        option_header_text_rect = option_header_text_surf.get_frect(center = (option_header_x, option_header_y))
        
        # draws the current user options' icon if the current user is not hovering over "PLAY"
        if current_user_option != 'PLAY':
            self.draw_game_modifier_icon(current_user_option, option_header_text_rect)

        self.display_surface.blit(option_header_text_surf, option_header_text_rect)

        # -------------- THE OPTION DESCRIPTION ----------------------
        # this function handles the display of the current user option description
        self.current_user_option_description(current_user_option, self.game_modifier_text_font)

    def draw(self, index, options):

        # menu selection box coordinates ( whole screen at the center of the screen )
        menu_selection_box_img_x = WINDOW_WIDTH // 2 
        menu_selection_box_img_y = WINDOW_HEIGHT / 2.5

        self.menu_selection_box_img_scaled = pygame.transform.scale(self.menu_selection_box_img, (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT // 1.5))

        self.menu_selection_box_img_rect = self.menu_selection_box_img_scaled.get_frect(center=(menu_selection_box_img_x, menu_selection_box_img_y))
        self.display_surface.blit(self.menu_selection_box_img_scaled, self.menu_selection_box_img_rect)

        # ----------------------------------- MENU SELECTION OPTIONS ------------------------------------------------------------
        self.draw_menu_options(index, options)

        # ----------------------------------- MENU SELECTION TEXT DESCRIPTIONS ------------------------------------------------------------
        self.draw_faded_background_for_text_desc()
        self.draw_option_description()
        

    def update(self):
        self.draw_bg()
        self.draw_particle_bg()
        self.input()
        self.draw(self.pre_game_select_menu_index, self.pre_game_select_menu_options)