from src.settings import *
from src.support import *

from src.fade_transition import *
from src.audio_manager import *

from src.ui import *
from src.game import *

class Main:
    def __init__(self):

        # windowed screen
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # fullscreen
        # self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)

        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.running = True

        #----------------AUDIO-------------------------
        self.audio_manager = AudioManager()
        self.background_music_active = False
        self.background_music_volume = 0.1
        self.sound_volume = 0.2

        self.main_screen_state = 'MAIN MENU' # this is the initial main_screen_state state
    
        # instances for game states
        self.game = Game(self.display_surface, self.audio_manager)
        self.main_menu = MainMenu(self.display_surface, self.audio_manager)
        self.pause_game_menu = PauseGameMenu(self.display_surface, self.audio_manager)
        self.game_over_menu = GameOverMenu(self.display_surface, self.audio_manager)
        self.pre_game_select_menu = PreGameSelectMenu(self.display_surface, self.audio_manager)

        # ------------ FADE TRANSITION-------------------
        self.fade_transition = FadeTransition(self.display_surface)

        self.fade_initiated = False 
        #------------------------------------------------

        self.game_variables_updated = False

    def fade_out_transition(self):
        self.fade_transition.fade_out(fade=True)
        self.fade_initiated = True

    def fade_in_transition(self, display_surface):
        if self.fade_initiated:
            self.fade_transition.fade_in(display_surface, fade=True)
            self.fade_initiated = False

    def reset_all_menu_states(self): 
        self.main_menu.reset_main_menu_screen_state()
        self.pause_game_menu.reset_pause_menu_screen_state()
        self.game_over_menu.reset_game_over_menu_screen_state()
        self.game.reset_pause_game_state()
        self.pre_game_select_menu.reset_pre_game_select_menu_screen_state()

    def change_states(self, state_name, continue_from_pause=False):
        self.reset_all_menu_states()

        if state_name == 'MAIN MENU' or state_name == 'PLAY' or state_name == 'GAMEOVER' and not continue_from_pause:
            self.audio_manager.stop_background_music()
            self.background_music_active = False

        if self.main_screen_state != 'PAUSEGAME':
            self.game_variables_updated = False 
        else:
            self.game_variables_updated = True
        
        self.main_screen_state = str(state_name) # changing the main screen state of the game

        if continue_from_pause:
            return
            
        if self.main_screen_state != 'PAUSEGAME':
            self.fade_out_transition()
            return True # having this function return True so that this function can be called within an if statement to call "continue" (used for fade transition)
            
    def update_game_variables(self, reset_game_modifiers=False):
        if reset_game_modifiers:
            self.pre_game_select_menu.modifier_selection = []
            self.game.game_modifiers = []

        self.game.game_modifiers = self.pre_game_select_menu.modifier_selection
        if not self.game_variables_updated:
            self.game.load_game()
            self.game_variables_updated = True

    # --------------------------------- MAIN GAME LOOP -----------------------------------------------------#

    def run(self):
        while self.running:
                
            match self.main_screen_state:
                case 'MAIN MENU':
                    # checking if background music is not currently playing. if not, then play the assigned track for that state.
                    if not self.background_music_active:
                        self.audio_manager.play_background_music('menu_track', self.background_music_volume)
                        self.background_music_active = True
                    
                    # when we go back into the main menu screen, reset all the game modifiers
                    self.update_game_variables(reset_game_modifiers=True)
                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------------------------

                    # repeatedly getting the updated screen state from the main menu if it changes through the player input
                    self.main_menu_screen_state = self.main_menu.main_menu_screen_state

                    # ----- PRE GAME SELECT CHECK ------------
                    if self.main_menu_screen_state == 'PRE GAME SELECT':
                        if self.change_states('PRE GAME SELECT'):
                            continue

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

                    self.fade_in_transition(self.display_surface)

                case 'PLAY':
                    # checking if background music is not currently playing. if not, then play the assigned track for that state.
                    if not self.background_music_active:
                        self.audio_manager.play_background_music('in_game_track', self.background_music_volume)
                        self.background_music_active = True

                    # ensuring that the game modifiers that are selected or unselected are on/off accordingly when the game begins
                    self.update_game_variables()
                    
                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------

                    # ------- GAME OVER CHECK ----------
                    # TWO STATES FOR GAME OVER
                    #
                    # ------- ONE: when the player runs out of lives --------------
                    #
                    self.game_over_out_of_lives_check = self.game.out_of_lives
                    if self.game_over_out_of_lives_check:
                        self.game_over_menu.fetch_score_value(self.game.score)
                        self.game_over_menu.fetch_game_modifiers(self.game.game_modifiers)
                        self.game_over_menu.fetch_highest_combo_value(self.game.highest_combo_value)
                        self.game_over_menu.out_of_lives_game_over()
                        self.audio_manager.play_sound_effect('game_over_sound', self.sound_volume)
                        if self.change_states('GAMEOVER'):
                            continue

                    # ----- TWO: when the player runs out of time --------------
                    #
                    self.game_over_out_of_time_check = self.game.out_of_time
                    if self.game_over_out_of_time_check:
                        self.game_over_menu.fetch_score_value(self.game.score)
                        self.game_over_menu.fetch_game_modifiers(self.game.game_modifiers)
                        self.game_over_menu.fetch_highest_combo_value(self.game.highest_combo_value)
                        self.game_over_menu.out_of_time_game_over()
                        self.audio_manager.play_sound_effect('game_over_sound', self.sound_volume)
                        if self.change_states('GAMEOVER'):
                            continue

                    # ------------------------------------------------------------------------------------------------------------

                    # ------- PAUSE GAME CHECK ------------
                    self.pause_game = self.game.pause_game
                    if self.pause_game: # checks if the player paused the game (this bool is handled within game.py under the typing_input function)
                        if self.change_states('PAUSEGAME'):
                            continue
                    
                    # dt
                    dt = self.clock.tick(60)
            
                    # event loop
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            self.running = False

                        self.game.typing_input(event)

                    # draw
                    # ------- IN GAME --------
                    self.game.display_surface.fill(COLORS['background'])
                        
                    self.game.draw_game()
                    self.game.game_logic()

                    self.fade_in_transition(self.display_surface)
            
                case 'PRE GAME SELECT':
                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------------------------

                    # repeatedly getting the updated screen state from the main menu if it changes through the player input
                    self.pre_game_select_menu_screen_state = self.pre_game_select_menu.pre_game_select_menu_screen_state

                    # -------------- MAIN MENU CHECK ------------------
                    if self.pre_game_select_menu_screen_state == 'MAIN MENU':
                        self.game.reset_game(self.display_surface, self.audio_manager)
                        if self.change_states('MAIN MENU'):
                            continue

                    # ----- PLAY CHECK ------------
                    if self.pre_game_select_menu_screen_state == 'PLAY':
                        if self.change_states('PLAY'):
                            continue

                    # dt
                    dt = self.clock.tick(60)
            
                    # event loop
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            self.running = False

                    # pre game select visual
                    self.pre_game_select_menu.update()

                    self.fade_in_transition(self.display_surface)

                case 'PAUSEGAME':
                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------------------------

                    # repeatedly getting the updated screen state from the paused game menu if it changes through the player input
                    self.pause_menu_screen_state = self.pause_game_menu.pause_menu_screen_state

                    # ---------- MAIN MENU CHECK -------------
                    if self.pause_menu_screen_state == 'MAIN MENU':
                        self.game.reset_game(self.display_surface, self.audio_manager) # going to the main menu will restart the game
                        if self.change_states('MAIN MENU'):
                            continue

                    # ---------- RESTART CHECK -------------
                    if self.pause_menu_screen_state == 'RESTART':
                        self.game.reset_game(self.display_surface, self.audio_manager)
                        if self.change_states('PLAY'):
                            continue

                    # ---------- CONTINUE CHECK ------------
                    if self.pause_menu_screen_state == 'CONTINUE':
                        if self.change_states('PLAY', continue_from_pause=True):
                            continue

                    # event loop
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            self.running = False

                    # main menu visual
                    self.pause_game_menu.update()

                    self.fade_in_transition(self.display_surface)

                case 'GAMEOVER':
                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------------------------

                    # repeatedly getting the updated screen state from the game_over game menu if it changes through the player input
                    self.game_over_menu_screen_state = self.game_over_menu.game_over_menu_screen_state

                    # -------------- MAIN MENU CHECK ------------------
                    if self.game_over_menu_screen_state == 'MAIN MENU':
                        self.game.reset_game(self.display_surface, self.audio_manager) # going to the main menu will restart the game
                        if self.change_states('MAIN MENU'):
                            continue

                    # -------------- TRY AGAIN CHECK -------------------
                    if self.game_over_menu_screen_state == 'TRY AGAIN':
                        self.game.reset_game(self.display_surface, self.audio_manager)
                        if self.change_states('PLAY'):
                            continue
                    
                    # dt
                    dt = self.clock.tick(60)
            
                    # event loop
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            self.running = False

                    # main menu visual
                    self.game_over_menu.update()

                    self.fade_in_transition(self.display_surface)

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    main = Main()
    main.run()