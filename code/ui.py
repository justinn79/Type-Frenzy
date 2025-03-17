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
        self.home_menu_options = ['PLAY', 'HOW TO PLAY', 'SETTINGS', 'QUIT']
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
            case 'PLAY':
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

        self.title_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 30)
        self.font = pygame.font.Font('fonts/Bungee-Regular.ttf', 20)

        # ------------------------------ IMAGES FOR THE MAIN MENU ------------------------------------------------------------
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


    def reset_game_over_menu_screen_state(self):
        self.game_over_menu_screen_state = self.original_game_over_menu_screen_state
        self.game_over_menu_index = 0

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

        # game over reason coordinates
        game_over_reason_text_x = game_over_text_x
        game_over_reason_text_y = game_over_text_y + 50

        game_over_reason_text = self.font.render(str(self.game_over_reason), True, COLORS['white'])
        game_over_reason_text_rect = game_over_reason_text.get_frect(center=(game_over_reason_text_x, game_over_reason_text_y))

        self.display_surface.blit(game_over_reason_text, game_over_reason_text_rect)

        # ----------------- MENU SELECTION BOX ---------------------------
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
        self.draw(self.game_over_menu_index, self.game_over_menu_options)
