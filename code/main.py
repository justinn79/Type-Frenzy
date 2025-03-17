from settings import *
from support import *

from ui import *
from game import *

class Main:
    def __init__(self):

        # windowed screen
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # fullscreen
        # self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)

        self.clock = pygame.time.Clock()
        self.running = True

        self.main_screen_state = 'PLAY' # this is the initial main_screen_state state
    
        # instances for game states
        self.game = Game(self.display_surface)
        self.main_menu = MainMenu(self.display_surface)
        self.pause_game_menu = PauseGameMenu(self.display_surface)
        self.game_over_menu = GameOverMenu(self.display_surface)

    def reset_all_menu_states(self):
        self.main_menu.reset_main_menu_screen_state()
        self.pause_game_menu.reset_pause_menu_screen_state()
        self.game_over_menu.reset_game_over_menu_screen_state()

    # --------------------------------- MAIN GAME LOOP -----------------------------------------------------#

    def run(self):
        while self.running:

            match self.main_screen_state:
                case 'MAIN MENU':
                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------------------------

                    # repeatedly getting the updated screen state from the main menu if it changes through the player input
                    self.main_menu_screen_state = self.main_menu.main_menu_screen_state

                    # ----- PLAY CHECK ------------
                    # if the main_menu_screen_state in ui.py becomes 'PLAY', change the main_screen_state variable within THIS file to change the state to PLAY (otherwise, handle the other states within the mainmenu in the main menu class)
                    if self.main_menu_screen_state == 'PLAY':
                        self.main_menu.reset_main_menu_screen_state() # before changing the main_screen_state, call this function to set the main_menu_screen_state from main menu back to its original default value (MAIN MENU) - a reset
                        self.main_screen_state = 'PLAY'

                    # ------ QUIT CHECK -----------
                    if self.main_menu_screen_state == 'QUIT':
                        self.running = False

                    # dt
                    dt = self.clock.tick(60)
            
                    # event loop
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            self.running = False

                    # main menu visual
                    self.main_menu.update()

                case 'PLAY':
                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------

                    # ------- GAME OVER CHECK ----------
                    # TWO STATES FOR GAME OVER
                    #
                    # ------- ONE: when the player runs out of lives --------------
                    #
                    # repeatedly getting the updated out_of_lives bool value from the game screen (if it goes from False to True when the player loses all their lives)
                    self.game_over_out_of_lives_check = self.game.out_of_lives
                    if self.game_over_out_of_lives_check:
                        self.game_over_menu.out_of_lives_game_over() # this function sets the out of lives text before the game over text is displayed
                        self.game_over_menu.reset_game_over_menu_screen_state()
                        self.main_screen_state = 'GAMEOVER'

                    # ----- TWO: when the player runs out of time --------------
                    #
                    # repeatedly getting the updated out_of_time bool value from the game screen (if it goes from False to True when the player does not type the current word on time)
                    self.game_over_out_of_time_check = self.game.out_of_time
                    if self.game_over_out_of_time_check:
                        self.game_over_menu.out_of_time_game_over() # this function sets the out of time text before the game over text is displayed
                        self.game_over_menu.reset_game_over_menu_screen_state()
                        self.main_screen_state = 'GAMEOVER'

                    # ------------------------------------------------------------------------------------------------------------

                    # ------- PAUSE GAME CHECK ------------
                    # repeatedly getting the updated pause_game bool value from the game screen (if it goes from False to True when the player presses the ESCAPE key)
                    self.pause_game = self.game.pause_game
                    if self.pause_game: # checks if the player paused the game (this bool is handled within game.py under the typing_input function)
                        self.game.reset_pause_game_state() # before changing the main_screen_state, call this function to set the boolean back to its original default value (False) - a reset
                        self.main_screen_state = 'PAUSEGAME'
                    
                    # dt
                    dt = self.clock.tick(60)
            
                    # event loop
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            self.running = False

                        self.game.typing_input(event)

                    # update
                    # self.game.all_sprites.update(

                    # draw
                    # ------- IN GAME --------
                    self.game.display_surface.fill(COLORS['background'])
                    # drawing the particles in the background
                    for bg_particle in self.game.bg_particles:
                        bg_particle.update()
                        
                    # self.game.all_sprites.draw(self.display_surface)
                    self.game.draw_game()
                    self.game.game_logic()
            
                case 'PAUSEGAME':
                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------------------------

                    # repeatedly getting the updated screen state from the paused game menu if it changes through the player input
                    self.pause_menu_screen_state = self.pause_game_menu.pause_menu_screen_state

                    # ---------- MAIN MENU CHECK -------------
                    # if the pause_menu_screen_state in ui.py becomes 'MAIN MENU', change the main_screen_state variable within THIS file to change the state to MAIN MENU (otherwise, handle the other states within the ui.py file)
                    if self.pause_menu_screen_state == 'MAIN MENU':
                        self.game.reset_game(self.display_surface) # going to the main menu will restart the game
                        self.pause_game_menu.reset_pause_menu_screen_state() # before changing the main_screen_state, call this function to reset the pause menu's screen state back to its original default value ("") - a reset
                        self.main_screen_state = 'MAIN MENU'

                    # ---------- RESTART CHECK -------------
                    if self.pause_menu_screen_state == 'RESTART':
                        self.game.reset_game(self.display_surface)
                        self.pause_game_menu.reset_pause_menu_screen_state() # before changing the main_screen_state, call this function to reset the pause menu's screen state back to its original default value ("") - a reset
                        self.main_screen_state = 'PLAY'

                    # ---------- CONTINUE CHECK ------------
                    if self.pause_menu_screen_state == 'CONTINUE':
                        self.pause_game_menu.reset_pause_menu_screen_state() # before changing the main_screen_state, call this function to reset the pause menu's screen state back to its original default value ("") - a reset
                        self.main_screen_state = 'PLAY'


                    # event loop
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            self.running = False

                    # main menu visual
                    self.pause_game_menu.update()

                case 'GAMEOVER':
                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------------------------

                    # repeatedly getting the updated screen state from the game_over game menu if it changes through the player input
                    self.game_over_menu_screen_state = self.game_over_menu.game_over_menu_screen_state

                    # -------------- MAIN MENU CHECK ------------------
                    # if the game_over_menu_screen_state in ui.py becomes 'MAIN MENU', change the main_screen_state variable within THIS file to change the state to MAIN MENU (otherwise, handle the other states within the ui.py file)
                    if self.game_over_menu_screen_state == 'MAIN MENU':
                        self.game.reset_game(self.display_surface) # going to the main menu will restart the game
                        self.game_over_menu.reset_game_over_menu_screen_state() # before changing the main_screen_state, call this function to reset the game_over menu's screen state back to its original default value ("") - a reset
                        self.main_screen_state = 'MAIN MENU'

                    # -------------- TRY AGAIN CHECK -------------------
                    if self.game_over_menu_screen_state == 'TRY AGAIN':
                        self.game.reset_game(self.display_surface)
                        self.game_over_menu.reset_game_over_menu_screen_state() # before changing the main_screen_state, call this function to reset the game_over menu's screen state back to its original default value ("") - a reset
                        self.main_screen_state = 'PLAY'

                    
                    # dt
                    dt = self.clock.tick(60)
            
                    # event loop
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            self.running = False

                    # main menu visual
                    self.game_over_menu.update()

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    main = Main()
    main.run()