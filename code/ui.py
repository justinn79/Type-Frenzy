from settings import *
from support import *

class MainMenu:
    def __init__(self, display_surface, screen_state):
        
        self.display_surface = display_surface
        self.title_font = pygame.font.Font('fonts/Bungee-Regular.ttf', 30)
        self.font = pygame.font.Font('fonts/Bungee-Regular.ttf', 20)

        # load the images for the main menu
        self.main_menu_bg = pygame.image.load('images/assets/main-menu.png').convert_alpha()

        self.left = 0
        self.top = 0
        # self.play is a boolean value that will always stay False until the player selects 'PLAY' on the home menu screen
        self.play = False
        # self.quit is a boolean value that will always stay False until the player selects 'QUIT' on the home menu screen
        self.quit = False


        # Home menu control
        self.home_menu_options = ['PLAY', 'HOW TO PLAY', 'SETTINGS', 'QUIT']
        self.home_menu_index = 0
        self.home_menu_option_count = len(self.home_menu_options)
        self.screen_state = screen_state

    def input(self):
        keys = pygame.key.get_just_pressed()
        # navigating the menu with keys
        # handle input for menu navigation within the home main menu menu
        if self.screen_state == 'MAIN MENU':
            if keys[pygame.K_DOWN]:
                self.home_menu_index += 1
            elif keys[pygame.K_UP]:
                self.home_menu_index -= 1

            # wrap around the index
            self.home_menu_index %= self.home_menu_option_count
            if keys[pygame.K_SPACE]:
                # when the player selects one of the options, change the current state of the ui to whatever the player selects.
                self.screen_state = self.home_menu_options[self.home_menu_index]
        
        # the state of 'PLAY' is not needed because the input of this state should be handled within the game itself

        # Handle input for menu navigation within the how to play menu
        elif self.screen_state == 'HOW TO PLAY':
            pass

        elif self.screen_state == 'QUIT':
            pass
            
        if keys[pygame.K_ESCAPE]:
            self.screen_state = 'MAIN MENU'
            self.home_menu_index = 0
            self.game_menu_index = 0
    
    def draw_bg(self):
        # bg
        self.scaled_main_menu_bg = pygame.transform.scale(self.main_menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.scaled_main_menu_bg_rect = self.scaled_main_menu_bg.get_frect(topleft=(0,0))
        self.display_surface.blit(self.scaled_main_menu_bg, self.scaled_main_menu_bg_rect)


    def menu_selection(self, main_menu_bg_rect, index, options):
        main_menu_bg_rect = main_menu_bg_rect
        # menu
        for optionIndex in range(len(options)):
            # x and y are the center points for each option
            x = main_menu_bg_rect.left + (main_menu_bg_rect.width / 2)
            y = main_menu_bg_rect.top + (main_menu_bg_rect.height / (len(options) + 2)) * (optionIndex + 1.5)

            # if the current option is the one that the player is currently hovering over, then change the color to GRAY
            if optionIndex == index:
                color = COLORS['yellow']
            else:
                color = COLORS['darkorange']

            text_surf = self.font.render(options[optionIndex], True, color) # render(text, antialias, color)
            text_rect = text_surf.get_frect(center = (x,y))
            self.display_surface.blit(text_surf, text_rect) # blit(source, dest)

    def draw(self):
        pass
        # match self.state:
        #     case 'MAIN MENU': 
        #         self.menu_selection(self.home_menu_index, self.home_menu_options)
        #     case 'HOW TO PLAY':
        #         self.how_to_play_screen()
        #     case 'PLAY': 
        #         self.play = True
        #     case 'QUIT': 
        #         self.quit = True

    def update(self):
        self.input()
        self.draw_bg()
        self.menu_selection(self.scaled_main_menu_bg_rect, self.home_menu_index, self.home_menu_options)
        # self.input()
        # self.draw_bg(self.dt) # continuously draw the parallax background within the home menu


class PauseGameMenu:
    def __init__(self):
        pass
    
    def draw(self):
        pass

    def update(self):
        pass

class GameOverMenu:
    def __init__(self):
        pass
    
    def draw(self):
        pass

    def update(self):
        pass
