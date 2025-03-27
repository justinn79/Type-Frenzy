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
        # instance for fade transitions
        self.fade_transition = FadeTransition(self.display_surface)

        self.fade_initiated = False # check if the fade transition has been initiated to prepare for the fade in transition (this bool is used in the main game loop so that the fade does not continuosly occur - we want it to only happen once)

        #------------------------------------------------

        self.game_variables_updated = False

    def fade_out_transition(self):
        self.fade_transition.fade_out(fade=True)
        self.fade_initiated = True

    def fade_in_transition(self, display_surface):
        if self.fade_initiated:
            self.fade_transition.fade_in(display_surface, fade=True)
            self.fade_initiated = False

    # resets all the menu states to its original/initial state
    def reset_all_menu_states(self): 
        self.main_menu.reset_main_menu_screen_state()
        self.pause_game_menu.reset_pause_menu_screen_state()
        self.game_over_menu.reset_game_over_menu_screen_state()
        self.game.reset_pause_game_state()
        self.pre_game_select_menu.reset_pre_game_select_menu_screen_state()

    def change_states(self, state_name, continue_from_pause=False):
        self.reset_all_menu_states() # resets all the menu states to its original/initial state

        # checking if the state that we are transitioning to is either MAIN MENU, PLAY or GAMEOVER. if it is, stop all the sounds and set the background music active bool to False to allow a music track to be played once again
        if state_name == 'MAIN MENU' or state_name == 'PLAY' or state_name == 'GAMEOVER' and not continue_from_pause:
            self.audio_manager.stop_background_music()
            self.background_music_active = False

        if self.main_screen_state != 'PAUSEGAME':
            self.game_variables_updated = False # sets the game_variables_updated flag back to False so that it can be updated once again if needed
        else:
            self.game_variables_updated = True # if the main screen state is 'PAUSEGAME', keep this variable 'True' because we do not want to reupdate/reset the game mid run (since this is only a pause state) - this fixes the bug where the player has a 'lives' and 'typingtimer' reset when pausing the game and selects continue.
        
        self.main_screen_state = str(state_name) # changing the main screen state of the game

        if continue_from_pause: # in the "CONTINUE" check within the "PAUSEGAME" main screen state, we want to avoid using the fade out transition below so we call this "change_state" function with "continue_from_pause=True" to ignore the fade transition code below
            return
            
        if self.main_screen_state != 'PAUSEGAME':
            self.fade_out_transition()
            return True # having this function return True so that i can call this function within an if statement to call "continue" (ignore the remaining code in the main game loop after this function is called) - THIS IS MAINLY FOR THE FADE IN TRANSITION (if the player pauses the game, we dont want to do the fade transition and we still want the current code within the game loop to continue running. this is because the player is still playing the current run even though it is exiting the "PLAY" state)

    def update_game_variables(self, reset_game_modifiers=False):
        if reset_game_modifiers:
            self.pre_game_select_menu.modifier_selection = [] # reset the game_modifiers list within the class game back to BLANK
            self.game.game_modifiers = [] # reset the game_modifiers list within the class game back to BLANK

        # this continuosly updates the "game_modifiers" variable within the game class. we want this continuosly calling here so that whatever the user selects, it will be sent to the game class to enable the corresponding game modifier.
        self.game.game_modifiers = self.pre_game_select_menu.modifier_selection
        # print(self.game.game_modifiers)
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
                        self.background_music_active = True # setting the background music active bool to True so the audio does not repeatedly get called to play
                    
                    # when we go back into the main menu screen, reset all the game modifiers so that it is blank when the user goes back into the pre game select menu
                    self.update_game_variables(reset_game_modifiers=True)
                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------------------------

                    # repeatedly getting the updated screen state from the main menu if it changes through the player input
                    self.main_menu_screen_state = self.main_menu.main_menu_screen_state

                    # ----- PRE GAME SELECT CHECK ------------
                    # if the main_menu_screen_state in ui.py becomes 'PRE GAME SELECT', change the main_screen_state variable within THIS file to change the state to PRE GAME SELECT (otherwise, handle the other states within the mainmenu in the main menu class)
                    if self.main_menu_screen_state == 'PRE GAME SELECT':
                        if self.change_states('PRE GAME SELECT'): # before changing the main_screen_state, call this function to set the main_menu_screen_state from main menu back to its original default value (MAIN MENU) - a reset
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

                    # fade in transition (we want this to be at the very end of the match case because since we are passing "self.display_surface", we want the transition to be called after the current screen for the state has been visually updated)
                    self.fade_in_transition(self.display_surface)

                case 'PLAY':
                    # checking if background music is not currently playing. if not, then play the assigned track for that state.
                    if not self.background_music_active:
                        self.audio_manager.play_background_music('in_game_track', self.background_music_volume)
                        self.background_music_active = True # setting the background music active bool to True so the audio does not repeatedly get called to play
                    # this function updates the game variables to ensure that the game modifiers that are selected or unselected are on/off accordingly when the game begins
                    self.update_game_variables()
                    # self.game_modifiers = self.pre_game_select_menu.get_modifier_selection()
                    # print(self.game_modifiers)
                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------

                    # ------- GAME OVER CHECK ----------
                    # TWO STATES FOR GAME OVER
                    #
                    # ------- ONE: when the player runs out of lives --------------
                    #
                    # repeatedly getting the updated out_of_lives bool value from the game screen (if it goes from False to True when the player loses all their lives)
                    self.game_over_out_of_lives_check = self.game.out_of_lives
                    if self.game_over_out_of_lives_check:
                        self.game_over_menu.fetch_score_value(self.game.score) # fetches the current score of the player
                        self.game_over_menu.fetch_game_modifiers(self.game.game_modifiers) # fetches the current game modifiers that was being used by the player during this run
                        self.game_over_menu.fetch_highest_combo_value(self.game.highest_combo_value) # fetches the highest combo of the run
                        self.game_over_menu.out_of_lives_game_over() # this function sets the out of lives text before the game over text is displayed
                        self.audio_manager.play_sound_effect('game_over_sound', self.sound_volume)
                        if self.change_states('GAMEOVER'):
                            continue

                    # ----- TWO: when the player runs out of time --------------
                    #
                    # repeatedly getting the updated out_of_time bool value from the game screen (if it goes from False to True when the player does not type the current word on time)
                    self.game_over_out_of_time_check = self.game.out_of_time
                    if self.game_over_out_of_time_check:
                        self.game_over_menu.fetch_score_value(self.game.score) # fetches the current score of the player
                        self.game_over_menu.fetch_game_modifiers(self.game.game_modifiers) # fetches the current game modifiers that was being used by the player during this run
                        self.game_over_menu.fetch_highest_combo_value(self.game.highest_combo_value) # fetches the highest combo of the run
                        self.game_over_menu.out_of_time_game_over() # this function sets the out of time text before the game over text is displayed
                        self.audio_manager.play_sound_effect('game_over_sound', self.sound_volume)
                        if self.change_states('GAMEOVER'):
                            continue

                    # ------------------------------------------------------------------------------------------------------------

                    # ------- PAUSE GAME CHECK ------------
                    # repeatedly getting the updated pause_game bool value from the game screen (if it goes from False to True when the player presses the ESCAPE key)
                    self.pause_game = self.game.pause_game
                    if self.pause_game: # checks if the player paused the game (this bool is handled within game.py under the typing_input function)
                        if self.change_states('PAUSEGAME'): # before changing the main_screen_state, call this function to set the boolean back to its original default value (False) - a reset
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
                        
                    # self.game.all_sprites.draw(self.display_surface)
                    self.game.draw_game()
                    self.game.game_logic()

                    # fade in transition (we want this to be at the very end of the match case because since we are passing "self.display_surface", we want the transition to be called after the current screen for the state has been visually updated)
                    self.fade_in_transition(self.display_surface)
            
                case 'PRE GAME SELECT':
                    # this function updates the game variables to ensure that the game modifiers that are selected or unselected are on/off accordingly when the game begins
                    # self.update_game_variables()

                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------------------------

                    # repeatedly getting the updated screen state from the main menu if it changes through the player input
                    self.pre_game_select_menu_screen_state = self.pre_game_select_menu.pre_game_select_menu_screen_state

                    # -------------- MAIN MENU CHECK ------------------
                    # if the pre_game_select_menu_screen_state in ui.py becomes 'MAIN MENU', change the main_screen_state variable within THIS file to change the state to MAIN MENU (otherwise, handle the other states within the ui.py file)
                    if self.pre_game_select_menu_screen_state == 'MAIN MENU':
                        self.game.reset_game(self.display_surface, self.audio_manager) # going to the main menu will restart the game
                        if self.change_states('MAIN MENU'): # before changing the main_screen_state, call this function to reset the game_over menu's screen state back to its original default value ("") - a reset
                            continue

                    # ----- PLAY CHECK ------------
                    # if the main_menu_screen_state in ui.py becomes 'PLAY', change the main_screen_state variable within THIS file to change the state to PLAY (otherwise, handle the other states within the mainmenu in the main menu class)
                    if self.pre_game_select_menu_screen_state == 'PLAY':
                        if self.change_states('PLAY'): # before changing the main_screen_state, call this function to set the main_menu_screen_state from main menu back to its original default value (MAIN MENU) - a reset
                            continue

                    # ------ BACK CHECK -----------
                    # if self.main_menu_screen_state == 'QUIT':
                    #     self.running = False

                    # dt
                    dt = self.clock.tick(60)
            
                    # event loop
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            self.running = False

                    # pre game select visual
                    self.pre_game_select_menu.update()

                    # fade in transition (we want this to be at the very end of the match case because since we are passing "self.display_surface", we want the transition to be called after the current screen for the state has been visually updated)
                    self.fade_in_transition(self.display_surface)

                case 'PAUSEGAME':
                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------------------------

                    # repeatedly getting the updated screen state from the paused game menu if it changes through the player input
                    self.pause_menu_screen_state = self.pause_game_menu.pause_menu_screen_state

                    # ---------- MAIN MENU CHECK -------------
                    # if the pause_menu_screen_state in ui.py becomes 'MAIN MENU', change the main_screen_state variable within THIS file to change the state to MAIN MENU (otherwise, handle the other states within the ui.py file)
                    if self.pause_menu_screen_state == 'MAIN MENU':
                        self.game.reset_game(self.display_surface, self.audio_manager) # going to the main menu will restart the game
                        if self.change_states('MAIN MENU'): # before changing the main_screen_state, call this function to reset the pause menu's screen state back to its original default value ("") - a reset
                            continue

                    # ---------- RESTART CHECK -------------
                    if self.pause_menu_screen_state == 'RESTART':
                        self.game.reset_game(self.display_surface, self.audio_manager)
                        if self.change_states('PLAY'): # before changing the main_screen_state, call this function to reset the pause menu's screen state back to its original default value ("") - a reset
                            continue

                    # ---------- CONTINUE CHECK ------------
                    if self.pause_menu_screen_state == 'CONTINUE':
                        if self.change_states('PLAY', continue_from_pause=True): # before changing the main_screen_state, call this function to reset the pause menu's screen state back to its original default value ("") - a reset
                            continue

                    # event loop
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            self.running = False

                    # main menu visual
                    self.pause_game_menu.update()

                    # fade in transition (we want this to be at the very end of the match case because since we are passing "self.display_surface", we want the transition to be called after the current screen for the state has been visually updated)
                    self.fade_in_transition(self.display_surface)

                case 'GAMEOVER':
                    # ---------------- GETTING UPDATED SCREEN STATE VALUES ------------------------------------------

                    # repeatedly getting the updated screen state from the game_over game menu if it changes through the player input
                    self.game_over_menu_screen_state = self.game_over_menu.game_over_menu_screen_state

                    # -------------- MAIN MENU CHECK ------------------
                    # if the game_over_menu_screen_state in ui.py becomes 'MAIN MENU', change the main_screen_state variable within THIS file to change the state to MAIN MENU (otherwise, handle the other states within the ui.py file)
                    if self.game_over_menu_screen_state == 'MAIN MENU':
                        self.game.reset_game(self.display_surface, self.audio_manager) # going to the main menu will restart the game
                        if self.change_states('MAIN MENU'): # before changing the main_screen_state, call this function to reset the game_over menu's screen state back to its original default value ("") - a reset
                            continue

                    # -------------- TRY AGAIN CHECK -------------------
                    if self.game_over_menu_screen_state == 'TRY AGAIN':
                        self.game.reset_game(self.display_surface, self.audio_manager)
                        if self.change_states('PLAY'): # before changing the main_screen_state, call this function to reset the game_over menu's screen state back to its original default value ("") - a reset
                            continue
                    
                    # dt
                    dt = self.clock.tick(60)
            
                    # event loop
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            self.running = False

                    # main menu visual
                    self.game_over_menu.update()

                    # fade in transition (we want this to be at the very end of the match case because since we are passing "self.display_surface", we want the transition to be called after the current screen for the state has been visually updated)
                    self.fade_in_transition(self.display_surface)

            pygame.display.update()

        pygame.quit()

# if __name__ == '__main__':
#     main = Main()
#     main.run()