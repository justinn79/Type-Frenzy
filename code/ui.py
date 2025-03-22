from settings import *
from support import *
from bg_particles import *


# ------------------------------------------------- MAIN MENU UI ------------------------------------------------------------------------------------
class MainMenu:
    def __init__(self, display_surface):
        
        self.display_surface = display_surface
        self.title_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 45)
        self.font = pygame.font.Font('fonts/Bungee-Regular.ttf', 20)

        self.bg_particles = [BgParticles(self.display_surface) for _ in range(100)] # create 50 instances of the BgParticles() class and put each one in the list "self.bg_particles"

        # ------------------------------ IMAGES FOR THE MAIN MENU ------------------------------------------------------------
        self.main_menu_bg = pygame.image.load('images/assets/main_menu_background.png').convert_alpha()
        self.main_menu_game_title_border = pygame.image.load('images/assets/game_title_border.png').convert_alpha()
        self.menu_selection_box_img = pygame.image.load('images/assets/menu_selection_box.png').convert_alpha()
        self.menu_button_img = pygame.image.load('images/assets/menu_button.png').convert_alpha()

        # ----------------------------------------------------------------------------------------------------------

        # Home menu control
        self.home_menu_options = ['START', 'HOW TO PLAY', 'SETTINGS', 'QUIT']
        self.home_menu_index = 0
        self.home_menu_option_count = len(self.home_menu_options)

        self.main_menu_screen_state = 'MAIN MENU' # initial main menu screen state
        self.original_main_menu_screen_state =  self.main_menu_screen_state # storing the initial main_menu_screen_state

    def reset_main_menu_screen_state(self):
        self.main_menu_screen_state = self.original_main_menu_screen_state
        self.home_menu_index = 0

    def input(self):
        keys = pygame.key.get_just_pressed()
        # navigating the menu with keys
        # handle input for menu navigation within the home main menu menu
        if keys[pygame.K_DOWN]:
            self.home_menu_index += 1
        elif keys[pygame.K_UP]:
            self.home_menu_index -= 1

        # wrap around the index
        self.home_menu_index %= self.home_menu_option_count
        if keys[pygame.K_SPACE]:
            # when the player selects one of the options, change the current state of the ui to whatever the player selects.

            if self.home_menu_options[self.home_menu_index] == 'START': # if the option that the player chooses is "START" it will bring the user to the 'PRE GAME SELECT' state. so we will just change that string to PRE GAME SELECT
                self.main_menu_screen_state = 'PRE GAME SELECT'
            else:
                self.main_menu_screen_state = self.home_menu_options[self.home_menu_index]
            
        if keys[pygame.K_ESCAPE]:
            self.main_menu_screen_state = 'MAIN MENU'
            self.home_menu_index = 0
    
    def draw_bg(self):
        # SCALING
        self.scaled_main_menu_bg = pygame.transform.scale(self.main_menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.scaled_main_menu_bg_rect = self.scaled_main_menu_bg.get_frect(topleft=(0,0))
        self.display_surface.blit(self.scaled_main_menu_bg, self.scaled_main_menu_bg_rect)
    
    def draw_particle_bg(self):
        # drawing the particles in the background
        for bg_particle in self.bg_particles:
            bg_particle.update()

    def draw_game_title(self):
        title_x = WINDOW_WIDTH // 2
        title_y = WINDOW_HEIGHT // 4

        title_surf = self.title_font.render('xType', True, COLORS['white'])
        title_rect = title_surf.get_frect(center=(title_x, title_y))

        # scaling the main menu game title border to align with the width and height of the game title
        main_menu_game_title_border_scaled = pygame.transform.scale(self.main_menu_game_title_border, (title_rect.width * 3, title_rect.height * 5))
        main_menu_game_title_border_scaled_rect = main_menu_game_title_border_scaled.get_frect(center=(title_x, title_y))

        self.display_surface.blit(main_menu_game_title_border_scaled, main_menu_game_title_border_scaled_rect)
        self.display_surface.blit(title_surf, title_rect)
        
    def main_menu_selection(self, main_menu_bg_rect, index, options):
        main_menu_bg_rect = main_menu_bg_rect

        # menu selection box coordinates
        menu_selection_box_img_x = main_menu_bg_rect.width // 2 # x coordinate for the center of the background
        menu_selection_box_img_y = WINDOW_HEIGHT - (main_menu_bg_rect.height // 3) # y coordinate for 2/3 of the height of the background

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

            # if the current option is the one that the player is currently hovering over, then change the color to GRAY
            if optionIndex == index:
                color = COLORS['midpurple']
            else:
                color = COLORS['white']


            # blitting the text on the buttom
            text_surf = self.font.render(options[optionIndex], True, color) # render(text, antialias, color)
            text_rect = text_surf.get_frect(center = (x,y))

            # creating the button location for the text
            menu_button_img_scaled = pygame.transform.scale(self.menu_button_img, (text_rect.width * 1.5, text_rect.height * 2))
            button_rect = menu_button_img_scaled.get_frect(center = (x,y))

            # blitting the button image first then the text surf on top
            self.display_surface.blit(menu_button_img_scaled, button_rect)
            self.display_surface.blit(text_surf, text_rect) # blit(source, dest)

    def how_to_play_screen(self):
        pass

    def settings_screen(self):
        pass

    def draw_menu(self):
        match self.main_menu_screen_state:
            case 'MAIN MENU':
                self.main_menu_selection(self.scaled_main_menu_bg_rect, self.home_menu_index, self.home_menu_options)
            case 'PRE GAME SELECT':
                pygame.time.delay(50) # temporary bug fix for a stutter look when clicking "PLAY" from the main menu to play the game
                # THIS STATE IS HANDLED WITHIN main.py (under 'MAIN MENU' match case)
                pass
            case 'HOW TO PLAY':
                self.how_to_play_screen()
            case 'SETTINGS':
                self.settings_screen()
            case 'QUIT':
                # THIS STATE IS HANDLED WITHIN main.py (under 'MAIN MENU' match case)
                pass

    def update(self):
        self.input()
        self.draw_bg()
        self.draw_particle_bg()
        self.draw_game_title()
        self.draw_menu()

# ------------------------------------------------- PAUSED GAME UI ------------------------------------------------------------------------------------
class PauseGameMenu:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        self.title_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 30)
        self.font = pygame.font.Font('fonts/Bungee-Regular.ttf', 20)

        # ------------------------------ IMAGES FOR THE MAIN MENU ------------------------------------------------------------
        self.menu_selection_box_img = pygame.image.load('images/assets/menu_selection_box.png').convert_alpha()
        self.menu_button_img = pygame.image.load('images/assets/menu_button.png').convert_alpha()

        # pause menu control
        self.pause_menu_options = ['CONTINUE', 'RESTART', 'MAIN MENU']
        self.pause_menu_index = 0
        self.pause_menu_option_count = len(self.pause_menu_options)

        self.pause_menu_screen_state = '' # initial pause menu screen state
        self.original_pause_menu_screen_state = self.pause_menu_screen_state # storing the initial pause_menu_screen_state

    def reset_pause_menu_screen_state(self):
        self.pause_menu_screen_state = self.original_pause_menu_screen_state
        self.pause_menu_index = 0

    def input(self):
        keys = pygame.key.get_just_pressed()
        # navigating the menu with keys
        # handle input for menu navigation within the pause menu
        if keys[pygame.K_DOWN]:
            self.pause_menu_index += 1
        elif keys[pygame.K_UP]:
            self.pause_menu_index -= 1

        # wrap around the index
        self.pause_menu_index %= self.pause_menu_option_count
        if keys[pygame.K_SPACE]:
            # when the player selects one of the options, change the current state of the ui to whatever the player selects.
            self.pause_menu_screen_state = self.pause_menu_options[self.pause_menu_index]
            
        if keys[pygame.K_ESCAPE]:
            # CONTINUE THE GAME
            pass
    
    def draw(self, index, options):
        # menu selection box coordinates
        menu_selection_box_img_x = WINDOW_WIDTH // 2 # x coordinate for the center of the window
        menu_selection_box_img_y = WINDOW_HEIGHT // 2 # y coordinate for the center of the window

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

            # if the current option is the one that the player is currently hovering over, then change the color to GRAY
            if optionIndex == index:
                color = COLORS['midpurple']
            else:
                color = COLORS['white']


            # blitting the text on the buttom
            text_surf = self.font.render(options[optionIndex], True, color) # render(text, antialias, color)
            text_rect = text_surf.get_frect(center = (x,y))

            # creating the button location for the text
            menu_button_img_scaled = pygame.transform.scale(self.menu_button_img, (text_rect.width * 1.5, text_rect.height * 2))
            button_rect = menu_button_img_scaled.get_frect(center = (x,y))

            # blitting the button image first then the text surf on top
            self.display_surface.blit(menu_button_img_scaled, button_rect)
            self.display_surface.blit(text_surf, text_rect) # blit(source, dest)

    def update(self):
        self.input()
        self.draw(self.pause_menu_index, self.pause_menu_options)

# ------------------------------------------------- GAME OVER UI ------------------------------------------------------------------------------------
class GameOverMenu:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        self.bg_particles = [BgParticles(self.display_surface) for _ in range(100)] # create 100 instances of the BgParticles() class and put each one in the list "self.bg_particles"

        self.title_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 30)
        self.font2 = pygame.font.Font('fonts/Bungee-Regular.ttf', 30)
        self.score_font = pygame.font.Font('fonts/Bungee-Regular.ttf', 25)
        self.font = pygame.font.Font('fonts/Bungee-Regular.ttf', 20)

        # ------------------------------ IMAGES FOR THE MAIN MENU ------------------------------------------------------------
        self.main_menu_bg = pygame.image.load('images/assets/main_menu_background.png').convert_alpha()
        self.menu_selection_box_img = pygame.image.load('images/assets/menu_selection_box.png').convert_alpha()
        self.menu_button_img = pygame.image.load('images/assets/menu_button.png').convert_alpha()

        # game over menu control
        self.game_over_menu_options = ['TRY AGAIN', 'MAIN MENU']
        self.game_over_menu_index = 0
        self.game_over_menu_option_count = len(self.game_over_menu_options)

        self.game_over_menu_screen_state = '' # initial game_over menu screen state
        self.original_game_over_menu_screen_state = self.game_over_menu_screen_state # storing the initial game_over_menu_screen_state

        # game_over_reason being either "out of lives" or "out of time"
        self.game_over_reason = 'testing 123' # initial game_over_reason state
        self.original_game_over_reason = self.game_over_reason

        # game modifier icon images
        self.icon_scale = 1
        # double time mod icon
        self.double_time_icon = pygame.image.load('images/game_mod_icons/double_time_icon.png').convert_alpha()
        self.double_time_icon = pygame.transform.scale(self.double_time_icon, (self.double_time_icon.get_width() * self.icon_scale, self.double_time_icon.get_height() * self.icon_scale))

        # hidden mod icon
        self.hidden_icon = pygame.image.load('images/game_mod_icons/hidden_icon.png').convert_alpha()
        self.hidden_icon = pygame.transform.scale(self.hidden_icon, (self.hidden_icon.get_width() * self.icon_scale, self.hidden_icon.get_height() * self.icon_scale))

        # perfect mod icon
        self.perfect_icon = pygame.image.load('images/game_mod_icons/perfect_icon.png').convert_alpha()
        self.perfect_icon = pygame.transform.scale(self.perfect_icon, (self.perfect_icon.get_width() * self.icon_scale, self.perfect_icon.get_height() * self.icon_scale))

        # score value variable to display
        self.score_value = 0

        # game modifier list to display
        self.game_modifiers = []

    def draw_bg(self):
        # SCALING
        self.scaled_main_menu_bg = pygame.transform.scale(self.main_menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.scaled_main_menu_bg_rect = self.scaled_main_menu_bg.get_frect(topleft=(0,0))
        self.display_surface.blit(self.scaled_main_menu_bg, self.scaled_main_menu_bg_rect)

    def draw_particle_bg(self):
        # drawing the particles in the background
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

    def fetch_game_modifiers(self, game_modifier_list):
        self.game_modifiers = game_modifier_list

    def input(self):
        keys = pygame.key.get_just_pressed()
        # navigating the menu with keys
        # handle input for menu navigation within the game_over menu
        if keys[pygame.K_DOWN]:
            self.game_over_menu_index += 1
        elif keys[pygame.K_UP]:
            self.game_over_menu_index -= 1

        # wrap around the index
        self.game_over_menu_index %= self.game_over_menu_option_count
        if keys[pygame.K_SPACE]:
            # when the player selects one of the options, change the current state of the ui to whatever the player selects.
            self.game_over_menu_screen_state = self.game_over_menu_options[self.game_over_menu_index]

    # def update_game_over_reason(self, game_over_reason):
    #     self.game_over_reason = game_over_reason
    
    def draw(self, index, options):
        
        # ---------------- GAME OVER TEXT -------------------
        # game over text coordinates
        game_over_text_x = WINDOW_WIDTH // 2
        game_over_text_y = WINDOW_HEIGHT // 7

        game_over_text = self.title_font.render('GAME OVER' , True, COLORS['white'])
        game_over_text_rect = game_over_text.get_frect(center=(game_over_text_x, game_over_text_y))

        self.display_surface.blit(game_over_text, game_over_text_rect)

        # ---------------- SCORE DISPLAY TEXT -------------------
        score_text = self.score_font.render('Score: ' + str(self.score_value), True, COLORS['white'])
        score_text_rect = score_text.get_frect(center=(game_over_text_x, game_over_text_y + 40))

        self.display_surface.blit(score_text, score_text_rect)

        # ---------------- GAME MODIFIERS DISPLAY TEXT -------------------
        game_modifier_text = self.font.render('Game Modifiers used: ', True, COLORS['white'])
        game_modifier_text_rect = game_modifier_text.get_frect(center=(score_text_rect.centerx, score_text_rect.y + 55))

        self.display_surface.blit(game_modifier_text, game_modifier_text_rect)

        icon_spacing = 35
        for i in range(len(self.game_modifiers)):
            if self.game_modifiers[i] == 'Double Time':
                icon_surf = self.double_time_icon
            if self.game_modifiers[i] == 'Hidden':
                icon_surf = self.hidden_icon
            if self.game_modifiers[i] == 'Perfect':
                icon_surf = self.perfect_icon

            x_loc = game_modifier_text_rect.right + (i * icon_spacing) # getting the horizontal distance of the current icon (same x location as the title of the game modifier that is being displayed)
            y_loc = game_modifier_text_rect.y # adding x amount of pixels under the text title of the modifier (displaying it under the modifier title)
            
            self.display_surface.blit(icon_surf, (x_loc, y_loc))

        # ----------------- MENU SELECTION BOX ---------------------------
        # menu selection box coordinates
        menu_selection_box_img_x = WINDOW_WIDTH // 2 # x coordinate for the center of the window
        menu_selection_box_img_y = WINDOW_HEIGHT // 2 # y coordinate for the center of the window

        # menu selection box scaling
        self.menu_selection_box_img_scaled = pygame.transform.scale(self.menu_selection_box_img, (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 1.75))

        # creating a rect of the newly scaled menu selection box image after it is scaled and blitting it onto the screen
        self.menu_selection_box_img_rect = self.menu_selection_box_img_scaled.get_frect(center=(menu_selection_box_img_x, menu_selection_box_img_y + 80))
        self.display_surface.blit(self.menu_selection_box_img_scaled, self.menu_selection_box_img_rect)

        # ---------------- GAME OVER REASON TEXT -------------------
        # game over reason coordinates
        # game_over_reason_text_x = game_over_text_x
        # game_over_reason_text_y = game_over_text_y + 50

        game_over_reason_text = self.font2.render(str(self.game_over_reason), True, COLORS['black'])
        game_over_reason_text_rect = game_over_reason_text.get_frect(center=(self.menu_selection_box_img_rect.centerx, self.menu_selection_box_img_rect.y + 75))

        self.display_surface.blit(game_over_reason_text, game_over_reason_text_rect)

        # MENU SELECTION OPTIONS
        for optionIndex in range(len(options)):
            # x and y are the center points for each option
            x = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width / 2)
            y = self.menu_selection_box_img_rect.top + (self.menu_selection_box_img_rect.height / (len(options) + 2)) * (optionIndex + 1.5)

            # if the current option is the one that the player is currently hovering over, then change the color to GRAY
            if optionIndex == index:
                color = COLORS['midpurple']
            else:
                color = COLORS['white']

            # blitting the text on the buttom
            text_surf = self.font.render(options[optionIndex], True, color) # render(text, antialias, color)
            text_rect = text_surf.get_frect(center = (x,y))

            # creating the button location for the text
            menu_button_img_scaled = pygame.transform.scale(self.menu_button_img, (text_rect.width * 1.5, text_rect.height * 2))
            button_rect = menu_button_img_scaled.get_frect(center = (x,y))

            # blitting the button image first then the text surf on top
            self.display_surface.blit(menu_button_img_scaled, button_rect)
            self.display_surface.blit(text_surf, text_rect) # blit(source, dest)

    def update(self):
        self.draw_bg()
        self.draw_particle_bg()
        self.input()
        self.draw(self.game_over_menu_index, self.game_over_menu_options)

# ------------------------------------------------- PRE GAME SELECT UI ------------------------------------------------------------------------------------
class PreGameSelectMenu:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        self.bg_particles = [BgParticles(self.display_surface) for _ in range(100)] # create 100 instances of the BgParticles() class and put each one in the list "self.bg_particles"

        self.font = pygame.font.Font('fonts/Bungee-Regular.ttf', 20)

        self.title_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 30)
        self.play_button_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 20)
        self.game_modifier_title_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 25)
        self.game_modifier_text_font = pygame.font.Font('fonts/SpaceGrotesk-Medium.ttf', 15)

        # ------------------------------ IMAGES FOR THE PRE GAME MENU ------------------------------------------------------------
        self.main_menu_bg = pygame.image.load('images/assets/main_menu_background.png').convert_alpha()
        self.menu_selection_box_img = pygame.image.load('images/assets/menu_selection_box.png').convert_alpha()
        self.menu_button_img = pygame.image.load('images/assets/menu_button.png').convert_alpha()
        self.menu_game_modifier_button_img = pygame.image.load('images/assets/menu_game_modifier_button.png').convert_alpha()

        self.unselected_box_img = pygame.image.load('images/assets/unselected_box.png').convert_alpha()
        self.selected_box_img = pygame.image.load('images/assets/selected_box.png').convert_alpha()

        # selection box scaling
        self.unselected_box_surf = pygame.transform.scale(self.unselected_box_img, (self.unselected_box_img.width * 2, self.unselected_box_img.height * 2))
        self.selected_box_surf = pygame.transform.scale(self.selected_box_img, (self.selected_box_img.width * 2, self.selected_box_img.height * 2))

        # pre_game_select menu control
        self.pre_game_select_menu_options = ['Double Time', 'Hidden', 'Perfect', 'PLAY']
        self.pre_game_select_menu_index = 0
        self.pre_game_select_menu_option_count = len(self.pre_game_select_menu_options)

        self.pre_game_select_menu_screen_state = '' # initial pre_game_select menu screen state
        self.original_pre_game_select_menu_screen_state = self.pre_game_select_menu_screen_state # storing the initial pre_game_select_menu_screen_state

        self.modifier_selected_bool = False
        self.modifier_selection = [] # a list containing all the modifiers the user has selected

        # get the current menu option that the user is currently hovering on
        self.user_current_option_index = 0

        # game modifier icon images
        self.icon_scale = 1.5
        # double time mod icon
        self.double_time_icon = pygame.image.load('images/game_mod_icons/double_time_icon.png').convert_alpha()
        self.double_time_icon = pygame.transform.scale(self.double_time_icon, (self.double_time_icon.get_width() * self.icon_scale, self.double_time_icon.get_height() * self.icon_scale))

        # hidden mod icon
        self.hidden_icon = pygame.image.load('images/game_mod_icons/hidden_icon.png').convert_alpha()
        self.hidden_icon = pygame.transform.scale(self.hidden_icon, (self.hidden_icon.get_width() * self.icon_scale, self.hidden_icon.get_height() * self.icon_scale))

        # perfect mod icon
        self.perfect_icon = pygame.image.load('images/game_mod_icons/perfect_icon.png').convert_alpha()
        self.perfect_icon = pygame.transform.scale(self.perfect_icon, (self.perfect_icon.get_width() * self.icon_scale, self.perfect_icon.get_height() * self.icon_scale))

        # game modifier text description
        self.double_time_text = 'The typing countdown meter is twice as fast. Type the current word quickly before the timer runs out'
        self.hidden_text = 'The current queued text will not be displayed. Remember that word before it comes into queue.'
        self.perfect_text = ' You only have one life. Once you submit an incorrect word, it is game over!'

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

            x_loc = modifier_text_rect.centerx - 30 # getting the horizontal distance of the current icon (same x location as the title of the game modifier that is being displayed)
            y_loc = modifier_text_rect.y + 40 # adding x amount of pixels under the text title of the modifier (displaying it under the modifier title)
            
            self.display_surface.blit(icon_surf, (x_loc, y_loc))
        
    def draw_bg(self):
        # SCALING
        self.scaled_main_menu_bg = pygame.transform.scale(self.main_menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.scaled_main_menu_bg_rect = self.scaled_main_menu_bg.get_frect(topleft=(0,0))
        self.display_surface.blit(self.scaled_main_menu_bg, self.scaled_main_menu_bg_rect)

    def draw_particle_bg(self):
        # drawing the particles in the background
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
        elif keys[pygame.K_UP]:
            self.pre_game_select_menu_index -= 1

        # wrap around the index
        self.pre_game_select_menu_index %= self.pre_game_select_menu_option_count
        if keys[pygame.K_SPACE]:
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
            # RETURN TO THE MAIN MENU
            self.pre_game_select_menu_screen_state = 'MAIN MENU'

    def draw_faded_background_for_text_desc(self):
        # faded background for text desc coordinates (right half of the menu selection box image)
        # x_left_center_of_menu_selection_box = (self.menu_selection_box_img_rect.width // 6) * 2
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
                # if the word fits, add it to the current line
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
            # Render each line of wrapped text inside the rectangle
            y_offset = self.faded_background_rect.top + self.faded_background_rect.height - 230
            for line in text_lines:
                line_surface = text_font.render(line, True, COLORS['black'])
                self.display_surface.blit(line_surface, (self.faded_background_rect.left + 2, y_offset))
                y_offset += line_surface.get_height()

        if current_user_option == 'Hidden':
            text_lines = self.wrap_text(self.hidden_text, text_font, self.faded_background_rect.width)
            # Render each line of wrapped text inside the rectangle
            y_offset = self.faded_background_rect.top + self.faded_background_rect.height - 230
            for line in text_lines:
                line_surface = text_font.render(line, True, COLORS['black'])
                self.display_surface.blit(line_surface, (self.faded_background_rect.left + 2, y_offset))
                y_offset += line_surface.get_height()

        if current_user_option == 'Perfect':
            text_lines = self.wrap_text(self.perfect_text, text_font, self.faded_background_rect.width)
            # Render each line of wrapped text inside the rectangle
            y_offset = self.faded_background_rect.top + self.faded_background_rect.height - 230
            for line in text_lines:
                line_surface = text_font.render(line, True, COLORS['black'])
                self.display_surface.blit(line_surface, (self.faded_background_rect.left + 2, y_offset))
                y_offset += line_surface.get_height()

        # if current_user_option == 'PLAY':
        #     option_description_text_surf = self.font.render('', True, COLORS['black'])

        # return option_description_text_surf

    def draw_menu_options(self, index, options):
        # x and y cord for the 'PLAY' button
        x_center = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width / 2)
        y_under_rect = self.menu_selection_box_img_rect.bottom + 75


        x_left_center_of_menu_selection_box = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width // 4)

        for optionIndex in range(len(options)):
            # x and y are the coordinates for each option
            x = x_left_center_of_menu_selection_box
            y = self.menu_selection_box_img_rect.top + (self.menu_selection_box_img_rect.height / (len(options) + 2)) * (optionIndex + 1.5)

            # if the current option is the one that the player is currently hovering over, then change the color to GRAY
            if optionIndex == index:
                color = COLORS['midpurple']
                self.user_current_option_index = index # gets the current index that the user is currently hovering on and updates it onto this variable
            else:
                color = COLORS['white']

            text_surf = self.font.render(options[optionIndex], True, color) # render(text, antialias, color)
            
            # if the menu option is 'PLAY', then put that TEXT option at the center of the screen under the menu box rect
            if options[optionIndex] == 'PLAY':
                text_surf = self.play_button_font.render(options[optionIndex], True, color) # render(text, antialias, color)
                text_rect = text_surf.get_frect(center = (x_center, y_under_rect))
            else:
                text_surf = self.font.render(options[optionIndex], True, color) # render(text, antialias, color)
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
            self.display_surface.blit(text_surf, text_rect) # blit(source, dest)
            
            # blitting the checkboxes beside each option
            self.display_surface.blit(selection_box_surf, selection_box_rect)
            
    def draw_option_description(self):
        # -------------- THE OPTION HEADER ----------------------
        # the coordinates are blitted at their center points 
        option_header_x = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width // 4) * 3 # second half of the menu selection box rect (center)
        option_header_y = self.menu_selection_box_img_rect.top + 125

        current_user_option = self.pre_game_select_menu_options[self.user_current_option_index] # gets the current string of the option that the user is currently hovering on and updates it onto this variable
        
        option_header_text_surf = self.game_modifier_title_font.render(current_user_option, True, COLORS['black'])
        option_header_text_rect = option_header_text_surf.get_frect(center = (option_header_x, option_header_y))
        
        # draws the current user options' icon if the current user is not hovering over "PLAY"
        if current_user_option != 'PLAY':
            self.draw_game_modifier_icon(current_user_option, option_header_text_rect)

        self.display_surface.blit(option_header_text_surf, option_header_text_rect) # blit(source, dest)

        # -------------- THE OPTION DESCRIPTION ----------------------
        # this function handles the display of the current user option description
        self.current_user_option_description(current_user_option, self.game_modifier_text_font)
        # # the coordinates are blitted under the option header
        # option_description_x = self.menu_selection_box_img_rect.left + (self.menu_selection_box_img_rect.width // 4) * 3 # second half of the menu selection box rect
        # option_description_y = option_header_y + 30

        # option_description_text_surf = self.current_user_option_description(current_user_option)
        # option_description_text_rect = option_description_text_surf.get_frect(midtop = (option_description_x, option_description_y))

        # self.display_surface.blit(option_description_text_surf, option_description_text_rect) # blit(source, dest)

    def draw(self, index, options):

        # menu selection box coordinates ( whole screen at the center of the screen )
        menu_selection_box_img_x = WINDOW_WIDTH // 2 # x coordinate for the center of the window
        menu_selection_box_img_y = WINDOW_HEIGHT / 2.5 # y coordinate for the center of the window

        # menu selection box scaling
        self.menu_selection_box_img_scaled = pygame.transform.scale(self.menu_selection_box_img, (WINDOW_WIDTH / 1.5, WINDOW_HEIGHT // 1.5))

        # creating a rect of the newly scaled menu selection box image after it is scaled and blitting it onto the screen
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